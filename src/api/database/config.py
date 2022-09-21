import os
from dataclasses import dataclass, field, asdict


@dataclass
class DBConfigs:

    url: str = os.environ.get('SQLALCHEMY_DB_URL')
    connect_args: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.connect_args['check_same_thread'] = 'sqlite' not in self.url

    def to_dict(self):
        return asdict(self)
