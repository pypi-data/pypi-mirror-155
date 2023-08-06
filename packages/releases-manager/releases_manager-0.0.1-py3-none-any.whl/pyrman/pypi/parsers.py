from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from pyrman.models import Package, Release


def parse_datetime(d: str):
    return datetime.strptime(d, "%Y-%m-%dT%H:%M:%S+%f")


def parse_packages(html: str) -> List[Package]:
    soup = BeautifulSoup(html, "html.parser")
    package_snippets = soup.select(".package-snippet")
    packages = []
    for package_snippet in package_snippets:
        packages.append(
            Package(
                title=package_snippet.select_one(".package-snippet__title").text.split("\n")[0],
                description=package_snippet.select_one(".package-snippet__description").text.strip(),
                last_released=parse_datetime(package_snippet.select_one("time[datetime]").get("datetime")),
                package_url=package_snippet.select_one(".button:not(.button--primary)").get("href"),
                releases_url=package_snippet.select_one(".button.button--primary").get("href"),
            )
        )
    return packages


def parse_csrf_token(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    csrf_input = soup.select_one("input[name=csrf_token]")
    return csrf_input.get("value")


def parse_releases(html: str) -> List[Release]:
    soup = BeautifulSoup(html, "html.parser")
    release_rows = soup.select(".table--releases tr")

    releases = []
    for row in release_rows:
        try:
            releases.append(
                Release(
                    version=row.select_one("th").text.strip(),
                    release_date=parse_datetime(row.select_one("time").get("datetime")),
                )
            )
        except AttributeError:
            pass
    return releases
