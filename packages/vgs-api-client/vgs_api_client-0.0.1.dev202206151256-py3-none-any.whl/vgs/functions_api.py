import json
from string import Template

import requests
import vgscli.auth
import vgscli.routes
import vgscli.vaults_api
from vgscli.auth import token_util

import vgs.exceptions
from vgs.configuration import Configuration

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
          id: fe1da605-898c-4b4b-a386-b56fe643759b
          operation: REDACT
          operations:
            - name: github.com/verygoodsecurity/common/compute/LarkyHttp
              parameters:
                script: >-
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
        name: echo.apps.verygood.systems-${name}
        source: RouteContainer
    id: c49386ef-cd14-4450-bd53-a497a4187f28
    type: rule_chain
version: 1
"""


class Functions:
    def __init__(self, config: Configuration):
        self.config = config
        self.environment = (
            "dev" if config.configuration_host == "https://api.verygoodsecurity.io" else "prod"
        )
        vgscli.auth.client_credentials_login(
            None, config.service_account_name, config.service_account_password, self.environment
        )

    def create(self, name, language, definition):
        if not name:
            raise vgs.exceptions.FunctionsApiException("Function name is required")
        if language != "Larky":
            raise vgs.exceptions.FunctionsApiException(
                "Unsupported function type. Supported types: Larky"
            )
        route_definition = Template(ROUTE_TEMPLATE).substitute(name=name, definition=definition)
        vgscli.auth.handshake(None, self.environment)
        self.create_route(route_definition)

    def create_route(self, route_definition):
        auth_token = token_util.get_access_token()
        routes_api = vgscli.vaults_api.create_api(
            None, self.config.vault_id, self.environment, auth_token
        )
        vgscli.routes.sync_all_routes(routes_api, route_definition)

    def invoke(self, name, data):
        username = self.config.username
        password = self.config.password
        vault_id = self.config.vault_id
        domain = "io" if self.environment == "dev" else "com"
        proxy = f"https://{username}:{password}@{vault_id}.sandbox.verygoodproxy.{domain}:8443"
        headers = {"User-Agent": "FunctionsAPI-python", "Content-Type": "application/json"}
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
