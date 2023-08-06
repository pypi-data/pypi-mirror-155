import re

import requests

from pyrman.pypi import parsers

ABSOLUTE_URL_PATTERN = re.compile(r"^https?://")

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "authority": "pypi.org",
    "origin": "https://pypi.org",
}


class PyPISession(requests.Session):
    def __init__(self, base_url: str):
        super().__init__()
        self.headers.update(DEFAULT_HEADERS)
        self.base_url = base_url.rstrip("/")
        #
        self.username = None
        self.password = None
        self.is_authenticated = False

    def absolute_url(self, url: str):
        if ABSOLUTE_URL_PATTERN.match(url):
            return url
        return self.base_url + "/" + url.lstrip("/")

    def request(self, method: str, url: str, **options):
        # authenticate if needed
        if not self.is_authenticated and not "/account/login/" in url:
            self.authenticate(self.username, self.password)
        return super().request(method, self.absolute_url(url), **options)

    def get_login_csrf_token(self) -> str:
        response = self.get("/account/login/")
        response.raise_for_status()
        return parsers.parse_csrf_token(response.text)

    def set_credentials(self, username: str, password: str):
        self.username = username
        self.password = password

    def authenticate(self, username: str, password: str):
        csrf_token = self.get_login_csrf_token()
        response = self.post(
            "/account/login/",
            headers={"referer": f"{self.base_url}/account/login/",},
            data={"csrf_token": csrf_token, "username": username, "password": password,},
            allow_redirects=False,
        )
        response.raise_for_status()

        redirect = response.headers.get("location")
        if not redirect or "/account/login/" in redirect:
            raise ValueError("Failed to authenticate")
