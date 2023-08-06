from typing import List

from pyrman.models import Package, Release
from pyrman.pypi import parsers
from pyrman.pypi.session import PyPISession

PYPI_DEFAULT_URL = "https://pypi.org"


class PyPIClient:
    def __init__(self, pypi_url: str = PYPI_DEFAULT_URL):
        self.session = PyPISession(pypi_url)

    def authenticate(self, username: str, password: str):
        self.session.authenticate(username, password)

    def set_credentials(self, username: str, password: str):
        self.session.set_credentials(username, password)

    def get_packages(self) -> List[Package]:
        response = self.session.get("/manage/projects/")
        response.raise_for_status()
        return parsers.parse_packages(response.text)

    def get_package_management_token(self, package_name: str):
        response = self.session.get(f"/manage/project/{package_name}/releases/")
        response.raise_for_status()
        return parsers.parse_csrf_token(response.text)

    def remove_release(self, package_name: str, release_version: str):
        management_csrf_token = self.get_package_management_token(package_name)
        response = self.session.post(
            f"/manage/project/{package_name}/release/{release_version}/",
            data={"confirm_delete_version": release_version, "csrf_token": management_csrf_token,},
        )
        if response.status_code == 404:
            management_url = self.session.absolute_url(f"/manage/project/{package_name}/releases")
            raise ValueError(
                f"Release {release_version} of package {package_name} not found on PyPI. ({management_url})"
            )
        response.raise_for_status()

    def list_releases(self, package: str) -> List[Release]:
        response = self.session.get(f"/manage/project/{package}/releases/")
        response.raise_for_status()
        return parsers.parse_releases(response.text)
