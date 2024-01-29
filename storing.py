from datetime import datetime
import os
import sqlite3
from typing import List
from dataclasses import dataclass


@dataclass
class GpuInfo:
    pid: int
    gpu_memory: str


@dataclass
class ProcessInfo:
    pid: int
    result: str


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


def create_tables(cursor, connection) -> None:
    cursor.executescript(
        """CREATE TABLE  IF NOT EXISTS  gpu_infos (
            pid, gpu_memory, host_id, timestamp
        );
        CREATE TABLE IF NOT EXISTS process_infos (
            pid, pid_info, host_id, timestamp
        );"""
    )
    connection.commit()


def insert_gpu_infos(
    cursor, connection, gpu_infos: List[GpuInfo], host_id: str, time_stamp: str
) -> None:
    gpu_info_tuples = [
        (gpu_info.pid, gpu_info.gpu_memory, host_id, time_stamp)
        for gpu_info in gpu_infos
    ]

    cursor.executemany(
        """INSERT INTO gpu_infos VALUES (
            ?, ?, ?, ?
        );""",
        gpu_info_tuples,
    )
    connection.commit()


def insert_process_infos(
    cursor, connection, process_infos: List[ProcessInfo], host_id: str, time_stamp: str
) -> None:
    process_info_tuples = [
        (pid, pid_info, host_id, time_stamp) for pid, pid_info in process_infos
    ]

    cursor.executemany(
        """INSERT INTO process_infos VALUES (
            ?, ?, ?, ?
        );""",
        process_info_tuples,
    )
    connection.commit()


def store_as_sqlite(
    gpu_infos: List[GpuInfo],
    process_infos: List[ProcessInfo],
    host_id: str,
    target_dir: str,
) -> None:
    os.makedirs(target_dir, exist_ok=True)

    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db_path = f"{target_dir}/gpu_monitor.db"
    existed_beforehand = os.path.exists(db_path)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    if not existed_beforehand:
        create_tables(cursor, connection)

    insert_gpu_infos(cursor, connection, gpu_infos, host_id, time_stamp)
    insert_process_infos(cursor, connection, process_infos, host_id, time_stamp)

    cursor.close()
    connection.close()
