from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class GpuInfo:
    pid: int
    gpu_memory: str


@dataclass
class ProcessInfo:
    pid: int
    name: str
    cmd: str  # The command starting the process
    created_at: datetime
    status: str
    owner: str
    owner_id: int
    cpu_percentage: float
    memory_percentage: float
