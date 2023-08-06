import enum
from datetime import timedelta, datetime
from typing import Optional, Union, List, Dict, Any

from pydantic import BaseModel


class AgentCommandType(enum.Enum):
    SET_CSS_CONFIG = "SET_CSS_CONFIG"
    EXEC_BASH = "EXEC_BASH"
    START_SERVICE = "START_SERVICE"
    STOP_SERVICE = "STOP_SERVICE"


class AgentCommandResultStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    TIMEOUT = "TIMEOUT"


class AgentStatus(BaseModel):
    id: int
    machineId: str
    last_active: datetime
    active: bool


class AgentCommand(BaseModel):
    id: int
    testFragmentId: int
    name: str  # hrn of the command, ignored by agent, but useful to inform users
    type: AgentCommandType
    # data:
    #   CSS config filename, or bash commands array, or service name. Type depends on AgentCommandType.
    #   (Dict[str, Any] is not used yet, but might be in the future)
    data: Union[str, List[str], Dict[str, Any]]
    timeout_s: float


class AgentCommandResult(BaseModel):
    commandId: int
    status: AgentCommandResultStatus

    # output of command, all optional
    return_value: Optional[int] = None
    error_msg: Optional[str] = None
    trace: Optional[str] = None
    debug_msg: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
