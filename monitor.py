#!/usr/bin/env pyhton3

import psutil

from data_types import GpuInfo, ProcessInfo
from helper import fetch_gpu_infos, fetch_process_info, get_host_name
from storing import store_as_csv, store_as_sqlite


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

    # store_as_csv(gpu_infos, process_infos, host_id=host_id, target_dir="tmp")
    store_as_sqlite(gpu_infos, process_infos, host_id=host_id, target_dir="tmp")
