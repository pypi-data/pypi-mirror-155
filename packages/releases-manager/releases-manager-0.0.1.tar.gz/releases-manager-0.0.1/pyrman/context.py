from dataclasses import dataclass

from pyrman.client import ReleaseManagerClient


@dataclass
class CLIContext:
    client: ReleaseManagerClient = None


context = CLIContext()
