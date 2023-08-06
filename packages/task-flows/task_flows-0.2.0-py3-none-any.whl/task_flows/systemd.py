from pathlib import Path
from subprocess import run
from textwrap import dedent

import sqlalchemy as sa

from .tables import timer_config_table
from .utils import get_engine, logger, systemd_dir

SYSTEMD_FILE_PREFIX = "task_flow_"


def create_scheduled_service_from_db(task_name: str):
    """Install and enable a systemd service and timer.

    Args:
        task_name (str): Name of task service should be created for.
    """
    with get_engine().begin() as conn:
        timer_kwargs = conn.execute(
            sa.select(timer_config_table.c.keyword, timer_config_table.c.value).where(
                timer_config_table.c.task_name == task_name
            )
        ).fetchall()
        if timer_kwargs is None:
            raise ValueError(f"No timer configuration found for {task_name}")
        timer_kwargs = list(timer_kwargs)

    systemd_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{SYSTEMD_FILE_PREFIX}name"

    timer_file = systemd_dir.joinpath(f"{stem}.timer")
    timer_file.write_text(
        "\n".join(
            [
                "[Unit]",
                f"Description=Timer for script {task_name}",
                "[Timer]",
                *[f"{k}={v}" for k, v in timer_kwargs],
                "Persistent=true",
                "[Install]",
                "WantedBy=timers.target",
            ]
        )
    )
    logger.info(f"Installed Systemd timer for {task_name}: {timer_file}")

    # timer_kwargs has to be a list of tuples (not dict), b/c there can be duplicate keys.
    service_file = systemd_dir.joinpath(f"{stem}.service")
    service_file.write_text(
        dedent(
            f"""
            [Unit]
            Description=script -- {task_name}
            After=network.target
            
            [Service]
            Type=simple
            ExecStart=docker start {task_name}
            
            # not needed if only using timer.
            [Install]
            WantedBy=multi-user.target
            """
        )
    )
    logger.info(f"Installed Systemd service for '{task_name}': {service_file}")

    logger.info("Reloading systemd services.")
    # make sure updated service is recognized.
    run(["systemctl", "--user", "daemon-reload"])

    logger.info(f"Enabling timer: {timer_file.task_name}")
    run(["systemctl", "--user", "enable", "--now", timer_file.task_name])


def remove_service(service_file: Path):
    run(["systemctl", "--user", "stop", service_file.stem])
    run(["systemctl", "--user", "disable", service_file.stem])
    run(["systemctl", "--user", "daemon-reload"])
    run(["systemctl", "--user", "reset-failed"])
    service_file.unlink()
