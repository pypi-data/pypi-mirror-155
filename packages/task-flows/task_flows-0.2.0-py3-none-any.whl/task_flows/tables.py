from datetime import datetime

import sqlalchemy as sa


metadata = sa.MetaData(schema="task_flows")


timer_options_table = sa.Table(
    "timer_options",
    metadata,
    sa.Column("task_name", sa.String, primary_key=True),
    sa.Column("keyword", sa.String, comment="Systemd timer option name. e.g. OnCalendar, OnUnitActiveSec, OnUnitInactiveSec. See freedesktop.org/software/systemd/man/systemd.timer.html#Options"),
    sa.Column("value", sa.String, comment="String representing time(s). e.g. Mon..Fri 3:00 America/New_York. See freedesktop.org/software/systemd/man/systemd.time.html"),
)

container_config_table = sa.Table(
    "container_config",
    metadata,
    sa.Column("task_name", sa.String, primary_key=True),
    sa.Column("command", sa.String, nullable=False),
    sa.Column("network_mode", sa.String, default='host'),
    sa.Column("init", sa.Boolean, default=True),
    sa.Column("user", sa.String),
    sa.Column("mem_limit", sa.String),
    sa.Column("shm_size", sa.String),
)

container_env_table = sa.Table(
    "container_env",
    metadata,
    sa.Column("task_name", sa.String, primary_key=True),
    sa.Column("variable", sa.String, primary_key=True),
    sa.Column("value", sa.String),
)

container_volumes_table = sa.Table(
    "container_volumes",
    metadata,
    sa.Column("task_name", sa.String, primary_key=True),
    sa.Column("host_path", sa.String, primary_key=True),
    sa.Column("container_path", sa.String),
    sa.Column("allow_write", sa.Boolean, default=True),
)

container_ulimits_table = sa.Table(
    "container_ulimits",
    metadata,
    sa.Column("task_name", sa.String, primary_key=True),
    sa.Column("name", sa.String, primary_key=True),
    sa.Column("soft", sa.Integer),
    sa.Column("hard", sa.Integer),
)


task_runs_table = sa.Table(
    "task_runs",
    metadata,
    sa.Column("task_name", sa.String, primary_key=True),
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
    sa.Column("task_name", sa.String, primary_key=True),
    sa.Column(
        "time", sa.DateTime(timezone=False), default=datetime.utcnow, primary_key=True
    ),
    sa.Column("type", sa.String),
    sa.Column("message", sa.String),
)
