# SPDX-FileCopyrightText: Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2


from minty import Base
from redis import Redis
from typing import Any, Dict

__version__ = "2.0.0"


class RedisInfrastructure(Base):
    def __init__(self) -> None:
        "Initialize a new Redis infrastructure factory"
        self.name = "session"

    def __call__(self, config: Dict[str, Dict[str, Any]]) -> "Redis[str]":
        "Create a new Redis connection from the specified configuration"
        redis_config = config["redis"][self.name]

        return Redis(**redis_config)
