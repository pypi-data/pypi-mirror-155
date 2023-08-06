import os


class HiddenLayerConfig(object):
    def __init__(self, env: os._Environ):
        self.env = env

    def customer_id(self) -> str:
        """Customer ID can be set via HL_CUSTOMER_ID environment variable

        :return: customer id
        """
        return self.env.get("HL_CUSTOMER_ID", None)

    def api_url(self) -> str:
        """Publisher URL can be set via HL_PUBLISHER_URL environment variable

        :return: publisher url
        """
        return self.env.get("HL_API_URL", None)

    def api_version(self) -> int:
        """Publisher URL can be set via HL_PUBLISHER_URL environment variable

        :return: publisher url
        """
        version = self.env.get("HL_API_VERSION", None)
        return int(version) if version else version

    def token(self) -> str:
        """Publisher API token can be set via HL_API_TOKEN environment variable

        :return: publisher api token
        """
        return self.env.get("HL_API_TOKEN", None)


config = HiddenLayerConfig(os.environ)
