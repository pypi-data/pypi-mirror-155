import json
import uuid
from string import Template

import requests
import vgscli.auth
import vgscli.routes
import vgscli.vaults_api
from vgscli.auth import token_util

import vgs.exceptions
from vgs.configuration import Configuration
from vgscli.errors import RouteNotValidError

ROUTE_TEMPLATE = """
data:
  - attributes:
      destination_override_endpoint: '*'
      entries:
        - classifiers: {}
          config:
            condition: AND
            rules:
              - expression:
                  field: PathInfo
                  operator: equals
                  type: string
                  values:
                    - /post
              - expression:
                  field: QueryString
                  operator: equals
                  type: string
                  values:
                    - function_name=${name}
          id: ${route_id}
          operation: REDACT
          operations:
            - - name: github.com/verygoodsecurity/common/compute/larky/http/Process
                parameters:
                  script: |-
                    ${definition}
          phase: REQUEST
          public_token_generator: UUID
          targets:
            - body
          token_manager: PERSISTENT
          transformer: JSON_PATH
          transformer_config:
            - none
      host_endpoint: echo\.apps\.verygood\.systems
      port: 80
      protocol: http
      source_endpoint: '*'
      tags:
        name: ${name}
    id: ${route_id}
    type: rule_chain
version: 1
"""


class Functions:
    def __init__(self, config: Configuration):
        self.config = config
        self.environment = (
            "dev" if config.configuration_host == "https://api.verygoodsecurity.io" else "prod"
        )

    def create(self, name, language, definition):
        if not (self.config.service_account_name and self.config.service_account_password):
            raise vgs.exceptions.FunctionsApiException(
                "Functions API configuration is not complete. "
                "Please set 'service_account_name' and 'service_account_password' to use functions CRUD API."
            )
        if not name:
            raise vgs.exceptions.FunctionsApiException("Function name is required")
        if language != "Larky":
            raise vgs.exceptions.FunctionsApiException(
                "Unsupported function type. Supported types: Larky"
            )
        vgscli.auth.client_credentials_login(
            None,
            self.config.service_account_name,
            self.config.service_account_password,
            self.environment,
        )
        vgscli.auth.handshake(None, self.environment)

        route_id = self._function_id(name)

        route_definition = Template(ROUTE_TEMPLATE).substitute(
            name=name, definition=definition, route_id=route_id
        )
        self._create_route(route_definition)

    @staticmethod
    def _function_id(name):
        return uuid.uuid5(
            uuid.NAMESPACE_URL, f"https://echo.apps.verygood.systems/post?function_name={name}"
        )

    def _create_route(self, route_definition):
        auth_token = token_util.get_access_token()
        routes_api = vgscli.vaults_api.create_api(
            None, self.config.vault_id, self.environment, auth_token
        )
        try:
            vgscli.routes.sync_all_routes(routes_api, route_definition)
        except RouteNotValidError as routeError:
            raise vgs.exceptions.FunctionsApiException(routeError.message)

    def invoke(self, name, data):
        if not (self.config.username and self.config.password):
            raise vgs.exceptions.FunctionsApiException(
                "Functions API configuration is not complete. "
                "Please set access credentials ('username' and 'password') to use functions invocation API."
            )
        if not self.config.vault_id:
            raise vgs.exceptions.FunctionsApiException(
                "Functions API configuration is not complete. "
                "Please set 'vault_id' to use functions invocation API."
            )
        username = self.config.username
        password = self.config.password
        vault_id = self.config.vault_id
        domain = "io" if self.environment == "dev" else "com"
        proxy = f"https://{username}:{password}@{vault_id}.sandbox.verygoodproxy.{domain}:8443"
        headers = {
            "User-Agent": "vgs-api-client/0.0.1-dev202206161125/python",
            "Content-Type": "application/json",
        }
        response = requests.post(
            f"https://echo.apps.verygood.systems/post?function_name={name}",
            proxies={"https": proxy},
            data=data,
            headers=headers,
            verify=False,
        )
        if response.status_code != 200:
            raise vgs.FunctionsApiException(
                f"Failed to invoke function '{name}'. Reason: {response.content}"
            )
        return json.loads(response.content)["data"]
