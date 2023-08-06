"""Main module."""

from dataclasses import dataclass

@dataclass
class Project:
    path: str = '/app'

@dataclass
class Secrets:
    path: str = '/secrets.yml'

class pysourcesinfo:
    def __init__(self):
        self.fetch

    def fetch(self, sources='/app', secrets='/secrets.yml'):
        """Fetching project sources metadata."""
        self.sources = Project(sources)
        self.secrets = Secrets(secrets)
        print(self.sources.path)
        print(self.secrets.path)