import argparse
import re
from pathlib import Path
from typing import List

import sqlalchemy as sa
from tqdm import tqdm

from . import tables
from .containers import create_container_from_db, remove_docker_container
from .systemd import (
    SYSTEMD_FILE_PREFIX,
    create_scheduled_service_from_db,
    remove_service,
)
from .utils import get_engine, logger, systemd_dir


def create_tables():
    """Create any tables that do not currently exist in the database."""
    with get_engine().begin() as conn:
        for table in (
            tables.timer_config_table,
            tables.container_env_table,
            tables.tasks_table,
            tables.task_runs_table,
            tables.task_run_errors_table,
        ):
            logger.info(f"Checking table: {table.name}")
            table.create(conn, checkfirst=True)


def get_tasks_systemd_files() -> List[Path]:
    """Get all systemd files from existing tasks."""
    return list(systemd_dir.glob(f"{SYSTEMD_FILE_PREFIX}*"))


def get_file_task_name(file: Path):
    """Extract task name from a systemd file."""
    return re.sub(f"^{SYSTEMD_FILE_PREFIX}", "", file.stem)


def get_existing_task_names() -> List[str]:
    """Get names of all tasks that have been created."""
    return [get_file_task_name(f) for f in get_tasks_systemd_files()]


def get_scheduled_names():
    """Get names of all scheduled tasks."""
    with get_engine().begin() as conn:
        scheduled_names = set(
            conn.execute(
                sa.select(tables.timer_config_table.c.name.distinct())
            ).scalars()
        )
    return scheduled_names


def remove_deleted_tasks():
    """Remove files from tasks that have been delted from the database."""
    scheduled_names = get_scheduled_names()
    for file in get_tasks_systemd_files():
        if (name := get_file_task_name(file)) not in scheduled_names:
            logger.info(f"Removing files from deleted task: {name}")
            remove_service(file)
            remove_docker_container(name)


def create_scheduled_task(name: str):
    create_container_from_db(name)
    create_scheduled_service_from_db(name)


def create_new_scheduled_tasks():
    scheduled_names = get_scheduled_names()
    names_to_create = scheduled_names.difference(get_existing_task_names())
    logger.info(f"Creating {len(names_to_create)} new scheduled task(s).")
    for name in tqdm(names_to_create):
        create_scheduled_task(name)


def recreate_scheduled_tasks():
    names_to_recreate = get_existing_task_names()
    logger.info(f"Recreating {len(names_to_recreate)} scheduled task(s).")
    for name in tqdm(names_to_recreate):
        create_scheduled_task(name)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--create-tables",
        action="store_true",
        help="Create any tables that do not currently exist in the database.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove files from tasks that have been delted from the database.",
    )
    parser.add_argument(
        "--create",
        type=str,
        nargs="*",
        help="Create a container + systemd files for a speified task(s), or all new tasks if no names are specified.",
    )
    parser.add_argument(
        "--recreate",
        type=str,
        nargs="*",
        help="Recreate container + systemd files for a speified task(s), or all existing tasks if no names are specified. Use this after a task's configuration is edited in the database.",
    )
    args = parser.parse_args()

    if args.create_tables:
        create_tables()

    if args.clean:
        remove_deleted_tasks()

    if args.create is not None:
        if not len(args.create):
            create_new_scheduled_tasks()
        else:
            for name in args.create:
                create_scheduled_task(name)

    if args.recreate is not None:
        if not len(args.recreate):
            recreate_scheduled_tasks()
        else:
            for name in args.create:
                create_scheduled_task(name)
