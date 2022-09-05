import os
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any

import yaml

from api.schemas.website_names import WebsiteNames


# Implementation of env variable parsing in yaml files.
# Allows to write ${ENV_VARIABLE} to load it in yaml config
path_matcher = re.compile(r'\$\{([^}^{]+)\}')

def path_constructor(loader, node):
  """Extract the matched value, expand env variable, and replace the match"""
  value = node.value
  match = path_matcher.match(value)
  env_var = match.group()[2:-1]
  return os.environ.get(env_var) + value[match.end():]

yaml.add_implicit_resolver('!path', regexp=path_matcher, first=None, Loader=yaml.SafeLoader)
yaml.add_constructor('!path', constructor=path_constructor, Loader=yaml.SafeLoader)


# Global dict configs
HTTP_REQ_CONFIGS: dict[WebsiteNames, Any] = {}


@dataclass
class RequestConfig:
    """Config class for http request data."""

    base_url: str
    raw_cookie: str = ''
    headers: dict = field(default_factory=dict)
    body: dict = field(default_factory=dict)
    q: dict = field(default_factory=dict)

    @property
    def q_base_url(self) -> str | None:
        """Return the base url formated with its request parameters if there are any."""
        if not self.q:
            return None
        q_str = '&'.join((k + '=' + str(v) for k, v in self.q.items()))
        return f'{self.base_url}?{q_str}'

    def to_dict(self):
        """d"""
        return asdict(self)


def load_configs() -> None:
    """Load http requests configs file into global conf object."""
    conf_file = (Path(__file__).parent / 'scrape_config.yml').resolve()

    if not os.path.exists(conf_file):
        raise FileNotFoundError(f'File {conf_file} not found')

    try:
        with open(conf_file, 'r', encoding='utf-8') as yml_file:
            yml_conf = yaml.safe_load(yml_file.read())
    except IOError as err:
        raise IOError(err)

    HTTP_REQ_CONFIGS.update(yml_conf)


def get_request_config(name: WebsiteNames) -> RequestConfig:
    """Get the associated config of a scraper from its name."""
    return RequestConfig(**HTTP_REQ_CONFIGS[name])
