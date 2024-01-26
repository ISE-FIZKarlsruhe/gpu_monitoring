from datetime import datetime
import psutil
import subprocess
from typing import List

from data_types import GpuInfo, ProcessInfo


def fetch_gpu_infos() -> List[GpuInfo]:
    smi_result = fetch_smi_result()
    smi_data = parse_smi_result(smi_result)
    return smi_data


def get_host_name() -> str:
    result = subprocess.run(
        ["hostname"],
        stdout=subprocess.PIPE,
    )
    result = result.stdout.decode("utf-8").strip()
    return result


def fetch_smi_result() -> str:
    result = subprocess.run(
        ["nvidia-smi", "--query-compute-apps=pid,used_memory", "--format=csv"],
        stdout=subprocess.PIPE,
    )
    result = result.stdout.decode("utf-8")
    return result


def parse_smi_result(smi_result: str) -> List[GpuInfo]:
    gpu_infos = []

    lines = smi_result.split("\n")

    for line in lines[1:]:  # first entry is header ("pid, used_gpu_memory [MiB]")
        entries = line.split(",")
        entries = [entry.strip() for entry in entries]

        if len(entries) != 2:  # Skip invalid lines
            continue

        pid, gpu_memory = int(entries[0]), entries[1]

        gpu_info = GpuInfo(pid=pid, gpu_memory=gpu_memory)
        gpu_infos.append(gpu_info)

    return gpu_infos


def fetch_process_info(pid: int) -> ProcessInfo:
    process = psutil.Process(pid)

    with process.oneshot():
        name = process.name()
        cmd = " ".join(process.cmdline())
        created_at = (
            datetime.fromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
        )
        status = process.status()
        owner = process.username()
        owner_id = process.uids()[0]
        cpu_percentage = process.cpu_percent(interval=1)
        memory_percentage = process.memory_percent(memtype="rss")

        process_info = ProcessInfo(
            pid=pid,
            name=name,
            cmd=cmd,
            created_at=created_at,
            status=status,
            owner=owner,
            owner_id=owner_id,
            cpu_percentage=cpu_percentage,
            memory_percentage=memory_percentage,
        )
        return process_info
