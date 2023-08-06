from functools import cache
from pprint import pformat

import docker
import sqlalchemy as sa
from docker.models.containers import Container

from .tables import container_env_table, tasks_table
from .utils import get_engine, logger


@cache
def get_docker_client():
    return docker.DockerClient(base_url="unix:///var/run/docker.sock")


def remove_docker_container(name: str, warn_on_error: bool = True):
    try:
        get_docker_client().containers.get(name).remove()
        logger.info(f"Removed existing container: {name}")
    except docker.errors.NotFound:
        if warn_on_error:
            logger.error(
                f"Could not remove docker container '{name}'. Container not found."
            )


def create_container_from_db(name: str) -> Container:
    """Use configuration stored in the database to create a Docker container for running a script.

    Args:
        name (str): Name of container/service in database.

    Returns:
        Container: The created container.
    """
    # remove any existing container with this name.
    remove_docker_container(name, warn_on_error=False)
    # get container info from the database.
    with get_engine().begin() as conn:
        container_cfg = conn.execute(
            sa.select(tasks_table.c.image, tasks_table.c.command).where(
                tasks_table.c.name == name
            )
        ).scalar()
        if container_cfg is None:
            raise ValueError(
                f"No container named '{name}' found in table {tasks_table.name}"
            )
        image_name, command = container_cfg
        command = command.split() if " " in command else command
        # get environmental variables for this container.
        container_env = conn.execute(
            sa.select(
                container_env_table.c.variable,
                container_env_table.c.value
                # variables with 'default' name are applied everything.
            ).where(container_env_table.c.name.in_(["default", name]))
        ).fetchall()
        container_env = dict(container_env) if container_env is not None else {}
    # create the container.
    kwargs = {
        "image": image_name,
        "name": name,
        "network_mode": "host",
        "detach": True,
        "environment": container_env,
        "command": command,
    }
    logger.info(f"Creating Docker container for {name}:\n{pformat(kwargs)}")
    return get_docker_client().containers.create(**kwargs)
