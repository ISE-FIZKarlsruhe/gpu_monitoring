from datetime import datetime
import subprocess
from typing import List

from data_types import GpuInfo, ProcessInfo


def fetch_gpu_infos(host_id: str) -> List[GpuInfo]:
    smi_result = fetch_smi_result(host_id)
    smi_data = parse_smi_result(smi_result)
    return smi_data


def get_host_name() -> str:
    result = subprocess.run(
        ["hostname"],
        stdout=subprocess.PIPE,
    )
    result = result.stdout.decode("utf-8").strip()
    return result


def fetch_smi_result(host_id: str) -> str:
    result = subprocess.run(
        [
            "ssh",
            host_id,
            "nvidia-smi",
            "--query-compute-apps=pid,used_memory",
            "--format=csv",
        ],
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


def fetch_process_info(host_id: str, pid: int) -> ProcessInfo:
    result = subprocess.run(
        [
            "ssh",
            host_id,
            "ps",
            "-o",
            "%mem=,%cpu=,user=,stat=,bsdstart=,bsdtime=,cmd=",
            "-p",
            str(pid),
        ],
        stdout=subprocess.PIPE,
    )
    result = result.stdout.decode("utf-8")
    return pid, result
