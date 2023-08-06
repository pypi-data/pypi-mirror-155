"""Defines session object used to authenticate through Sonar API"""
import requests


class SonarSession(requests.Session):
    """session object used to authenticate through Sonar API"""

    def __init__(self, sonar_url: str, sonar_token: str = None):
        super().__init__()
        self.sonar_url = sonar_url
        self.sonar_token = sonar_token

    def absolute_path(self, path: str):
        """Convert potentially relative URL to absolute URL"""
        if path.startswith("http"):
            return path
        return self.sonar_url.rstrip("/") + "/" + path.lstrip("/")

    def request(
        self, method: str, url: str, **options
    ):  # pylint: disable=arguments-differ
        """Override session.request to provide authentication and absolute URLs"""
        if self.sonar_token is not None and options.get("auth") is None:
            options["auth"] = (self.sonar_token, "")
        return super().request(method, self.absolute_path(url), **options)
