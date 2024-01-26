#!/usr/bin/env pyhton3

from datetime import datetime
import os
import psutil
from typing import List, Tuple

from data_types import GpuInfo, ProcessInfo
from helper import fetch_gpu_infos, fetch_process_info, get_host_name


def store_as_csv(
    gpu_infos: List[GpuInfo],
    process_infos: List[ProcessInfo],
    host_id: str,
    target_dir: str,
) -> None:
    os.makedirs(target_dir, exist_ok=True)

    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert gpu data
    gpu_target_path = f"{target_dir}/gpu_infos.csv"
    existed_beforehand = os.path.exists(gpu_target_path)

    with open(gpu_target_path, "a") as target_file:
        if not existed_beforehand:
            target_file.write("pid, gpu memory, host id, timestamp\n")

        for gpu_info in gpu_infos:
            line = f"{gpu_info.pid}, {gpu_info.gpu_memory}, {host_id}, {time_stamp}\n"
            target_file.write(line)

    # Insert process data
    process_target_path = f"{target_dir}/process_infos.csv"
    existed_beforehand = os.path.exists(process_target_path)

    with open(process_target_path, "a") as target_file:
        if not existed_beforehand:
            target_file.write(
                "pid, name, startup command, created at, status, owner, owner id, cpu percentage (interval=1s), memory percentage (rss), host id, timestamp\n"
            )

        for process_info in process_infos:
            line = f"{process_info.pid}, {process_info.name}, {process_info.cmd}, {process_info.created_at}, {process_info.status}, {process_info.owner}, {process_info.owner_id}, {process_info.cpu_percentage}, {process_info.memory_percentage}, {host_id}, {time_stamp}\n"
            target_file.write(line)


if __name__ == "__main__":
    host_id = get_host_name()

    gpu_infos = fetch_gpu_infos()

    process_infos = []
    for gpu_info in gpu_infos:
        try:
            process_info = fetch_process_info(pid=gpu_info.pid)
            process_infos.append(process_info)
        except (
            psutil.NoSuchProcess
        ):  # Process has vanished before its information has been read.
            pass

    store_as_csv(
        gpu_infos,
        process_infos,
        host_id=host_id,
        target_dir="tmp"
    )
