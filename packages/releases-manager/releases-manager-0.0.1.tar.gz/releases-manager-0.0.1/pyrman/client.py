from typing import List

from pyrman.models import Package, Release
from pyrman.pypi.client import PYPI_DEFAULT_URL, PyPIClient

REPOSITORY_DEFAULT_URL = PYPI_DEFAULT_URL


class ReleaseManagerClient:
    def __new__(cls, repository_url: str = REPOSITORY_DEFAULT_URL):
        if "pypi.org" in repository_url:
            return PyPIClient(repository_url)
        else:
            raise ValueError("Can't guess repository type from url...")

    def authenticate(self, username: str, password: str):
        raise NotImplementedError

    def get_packages(self) -> List[Package]:
        raise NotImplementedError

    def remove_release(self, package_name: str, release_version: str):
        raise NotImplementedError

    def set_credentials(self, username: str, password: str):
        raise NotImplementedError

    def list_releases(self, package: str) -> List[Release]:
        raise NotImplementedError
