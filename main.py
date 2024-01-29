import os, time

from data_types import GpuInfo, ProcessInfo
from helper import fetch_gpu_infos, fetch_process_info, get_host_name
from storing import store_as_sqlite
from typing import List

import logging

if os.environ.get("DEBUG") == "1":
    logging.basicConfig(level=logging.DEBUG)


def main(hosts: List[str]) -> None:
    for host_id in hosts.split(" "):
        logging.debug(f"Fetching GPU data from {host_id}")
        gpu_infos = fetch_gpu_infos(host_id)
        logging.debug(f"Fetching process data from {host_id}")
        process_infos = [
            fetch_process_info(host_id, pid=gpu_info.pid) for gpu_info in gpu_infos
        ]
        store_as_sqlite(gpu_infos, process_infos, host_id=host_id, target_dir="tmp")


if __name__ == "__main__":
    # We expect a list of hostnames that can be SSH'ed into from the account running this script.
    # for convenience, sconfigure shortcut names in the .ssh/config file.
    hosts = os.environ.get("HOSTS")
    main(hosts)
    while True:
        logging.debug("Sleeping for 25 seconds before next run.")
        time.sleep(25)
        main(hosts)
        # In a cronjob, the minimum interval is 1 minute, but we want to run this job every 30 seconds.
        # That's why we use this trick to get sub-minute intervals.
