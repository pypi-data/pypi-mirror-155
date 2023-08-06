class Configuration:
    def __init__(
        self,
        username,
        password,
        vault_id=None,
        host="https://api.sandbox.verygoodvault.com",
        configuration_host="https://api.sandbox.verygoodsecurity.com",
        service_account_name=None,
        service_account_password=None,
    ):
        self.username = username
        self.password = password
        self.vault_id = vault_id
        self.host = host
        self.configuration_host = configuration_host
        self.service_account_name = service_account_name
        self.service_account_password = service_account_password


def config(*args, **kwargs):
    return Configuration(*args, **kwargs)
