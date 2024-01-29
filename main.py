#!/usr/bin/env pyhton3

import psutil, os

from data_types import GpuInfo, ProcessInfo
from helper import fetch_gpu_infos, fetch_process_info, get_host_name
from storing import store_as_sqlite


if __name__ == "__main__":
    # We expect a list of hostnames that can be SSH'ed into from the account running this script.
    # for convenience, sconfigure shortcut names in the .ssh/config file.
    hosts = os.environ.get("HOSTS")
    for host_id in hosts.split(" "):
        gpu_infos = fetch_gpu_infos(host_id)
        process_infos = [
            fetch_process_info(host_id, pid=gpu_info.pid) for gpu_info in gpu_infos
        ]
        store_as_sqlite(gpu_infos, process_infos, host_id=host_id, target_dir="tmp")
