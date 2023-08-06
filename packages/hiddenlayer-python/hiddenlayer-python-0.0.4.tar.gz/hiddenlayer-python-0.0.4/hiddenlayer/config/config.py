import os


class HiddenLayerConfig(object):
    def __init__(self, env: os._Environ):
        self.env = env

    def api_host(self) -> str:
        """HiddenLayer API host can be set via HL_API_HOST environment variable

        :return: api host
        """
        return self.env.get("HL_API_HOST", None)

    def api_proto(self) -> str:
        """HiddenLayer API proto be set via HL_API_PROTO environment variable

        :return: api proto
        """
        return self.env.get("HL_API_PROTO", None)

    def api_version(self) -> int:
        """HiddenLayer API version can be set via HL_API_VERSION environment variable

        :return: publisher url
        """
        version = self.env.get("HL_API_VERSION", None)
        return int(version) if version else version

    def token(self) -> str:
        """HiddenLayer API token can be set via HL_API_TOKEN environment variable

        :return: publisher api token
        """
        return self.env.get("HL_API_TOKEN", None)


config = HiddenLayerConfig(os.environ)
