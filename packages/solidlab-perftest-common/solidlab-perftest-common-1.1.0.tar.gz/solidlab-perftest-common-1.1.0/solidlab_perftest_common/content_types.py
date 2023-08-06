from enum import Enum
from typing import Any, Type

from solidlab_perftest_common.agent_command import (
    AgentCommand,
    AgentStatus,
    AgentCommandResult,
)


class SolidLabContentType(Enum):
    AGENT_COMMAND = "application/vnd.imecilabt.solidlab.agent.command+json;version=1"
    AGENT_STATUS = "application/vnd.imecilabt.solidlab.agent.status+json;version=1"
    AGENT_COMMAND_RESULT = (
        "application/vnd.imecilabt.solidlab.agent.commandres+json;version=1"
    )

    TEXT = "text/plain"
    JSON = "application/json"

    # def from_type(self, t: Type) -> 'SolidLabContentType':
    #     pass  # hard to implement with support for subclasses, as "t is AgentCommand" ignores subclasses
    #  (can be implemented anyway, when actually needed)

    def matches_type(self, obj: Any) -> bool:
        if isinstance(obj, AgentCommand):
            return self == SolidLabContentType.AGENT_COMMAND
        if isinstance(obj, AgentStatus):
            return self == SolidLabContentType.AGENT_STATUS
        if isinstance(obj, AgentCommandResult):
            return self == SolidLabContentType.AGENT_COMMAND_RESULT
        raise ValueError(f"obj {obj!r} of type {type(obj)!r} does not match {self!r}")
