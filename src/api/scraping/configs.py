import os
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any

import yaml

from api.schemas import WebsiteNames


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
        q_url = None
        if self.q:
            q_str = '&'.join((k + '=' + v for k, v in self.q.items()))
            q_url = f'{self.base_url}?{q_str}'
        return q_url

    def to_dict(self):
        """d"""
        return asdict(self)


def load_configs() -> dict:
    """Load http requests configs."""
    conf_file = (Path(__file__).parent / 'scrape_config.yml').resolve()

    if not os.path.exists(conf_file):
        raise FileNotFoundError(f'File {conf_file} not found')

    try:
        with open(conf_file, 'r', encoding='utf-8') as yml_file:
            yml_conf = yaml.safe_load(yml_file.read())
    except IOError as err:
        raise IOError(err)

    return yml_conf


HTTP_REQ_CONFIGS: dict[WebsiteNames, Any] = load_configs()


def get_request_config(name: WebsiteNames) -> RequestConfig:
    """Get the associated config of a scraper from its name."""
    return RequestConfig(**HTTP_REQ_CONFIGS[name])
