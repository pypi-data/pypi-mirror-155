"""Top-level package for pysourcesinfo."""

__author__ = """redacted"""
__email__ = 'noreply@local.io'
__version__ = '0.1.0'

from dataclasses import dataclass

@dataclass
class Project:
    path: str = '/app'

@dataclass
class Secrets:
    path: str = '/secrets.yml'

from . import Project
from . import Secrets

class pysourcesinfo:
    def __init__(self):
        self.fetch

    def fetch(self, src='/app', secrets='/secrets.yml'):
        """Fetching project sources metadata."""
        self.project = Project(src)
        self.secrets = Secrets(secrets)