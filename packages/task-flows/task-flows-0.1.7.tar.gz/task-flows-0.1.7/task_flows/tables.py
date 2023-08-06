from datetime import datetime

import sqlalchemy as sa

metadata = sa.MetaData(schema="services")

"""The "name" column is the name of the container/service/timer/task."""

timer_config_table = sa.Table(
    "timer_config",
    metadata,
    sa.Column("name", sa.String, primary_key=True),
    sa.Column("keyword", sa.String, primary_key=True),
    sa.Column("value", sa.String),
)

container_env_table = sa.Table(
    "container_env",
    metadata,
    sa.Column("name", sa.String, primary_key=True),
    sa.Column("variable", sa.String, primary_key=True),
    sa.Column("value", sa.String),
)

tasks_table = sa.Table(
    "tasks",
    metadata,
    sa.Column("name", sa.String, primary_key=True),
    sa.Column("image", sa.String),
    sa.Column("command", sa.String),
)

task_runs_table = sa.Table(
    "task_runs",
    metadata,
    sa.Column("name", sa.String, primary_key=True),
    sa.Column(
        "started",
        sa.DateTime(timezone=False),
        default=datetime.utcnow,
        primary_key=True,
    ),
    sa.Column("finished", sa.DateTime(timezone=False)),
    sa.Column("retries", sa.Integer, default=0),
    sa.Column("status", sa.String),
    sa.Column("return_value", sa.String),
)

task_run_errors_table = sa.Table(
    "task_run_errors",
    metadata,
    sa.Column("name", sa.String, primary_key=True),
    sa.Column(
        "time", sa.DateTime(timezone=False), default=datetime.utcnow, primary_key=True
    ),
    sa.Column("type", sa.String),
    sa.Column("message", sa.String),
)
