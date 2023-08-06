import re
from pathlib import Path
from typing import List

import sqlalchemy as sa
from click.core import Group
from tqdm import tqdm

from . import tables
from .containers import create_container_from_db, remove_docker_container
from .systemd import (
    SYSTEMD_FILE_PREFIX,
    create_scheduled_service_from_db,
    remove_service,
)
from .utils import get_engine, logger, systemd_dir


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
                sa.select(tables.timer_config_table.c.task_name.distinct())
            ).scalars()
        )
    return scheduled_names


cli = Group("task-flows", chain=True)


@cli.command()
def check_tables():
    """Create any tables that do not currently exist in the database."""
    with get_engine().begin() as conn:
        for table in (
            tables.timer_config_table,
            tables.container_env_table,
            tables.tasks_table,
            tables.task_runs_table,
            tables.task_run_errors_table,
        ):
            logger.info(f"Checking table: {table.task_name}")
            table.create(conn, checkfirst=True)


@cli.command()
def clean():
    """Remove files from tasks that have been deleted from the database."""
    scheduled_names = get_scheduled_names()
    for file in get_tasks_systemd_files():
        if (task_name := get_file_task_name(file)) not in scheduled_names:
            logger.info(f"Removing files from deleted task: {task_name}")
            remove_service(file)
            remove_docker_container(task_name)


@cli.command()
@cli.argument("task_name")
def create_task(task_name: str):
    """Create (or recreate) a scheduled task using configuration from the database.

    Args:
        name (str): Name of the task, as specified in the database.
    """
    create_container_from_db(task_name)
    create_scheduled_service_from_db(task_name)


@cli.command()
@cli.option("--recreate_existing", "-r", is_flag=True)
def create_all_tasks(recreate_existing: bool = False):
    """Create scheduled tasks for all tasks configurations in the database.

    Args:
        recreate_existing (bool, optional): Recreate already existing tasks. Defaults to False.
    """
    names_to_create = get_scheduled_names()
    if not recreate_existing:
        existing_task_names = get_existing_task_names()
        logger.info(
            f"Ignoring {len(existing_task_names)} existing tasks (not recreating)."
        )
        names_to_create.difference_update(existing_task_names)
    logger.info(f"Creating {len(names_to_create)} scheduled task(s).")
    for task_name in tqdm(names_to_create):
        create_task(task_name)
