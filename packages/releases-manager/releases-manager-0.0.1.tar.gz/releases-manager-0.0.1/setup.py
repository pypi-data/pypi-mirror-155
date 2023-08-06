from importlib.metadata import entry_points
import setuptools

def get_file_content(filename: str):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

setuptools.setup(
    name="releases-manager",
    description="Manage python published release for packages that you owns on PyPI.",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires = ["click", "requests", "bs4"],
    entry_points={
        "console_scripts": [
            "pyrman=pyrman.__main__:cli"
        ]
    },
    long_description=get_file_content("README.md"),
    long_description_content_type='text/markdown',
)
