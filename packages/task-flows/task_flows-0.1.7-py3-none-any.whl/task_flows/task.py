import asyncio
import functools
import os
import sys
from datetime import datetime
from typing import Any, List, Optional

import sqlalchemy as sa
from alert_msgs import KV, FontColors, FontSize, Text, send_alert
from alert_msgs.components import AlertComponent

from .tables import task_run_errors_table, task_runs_table
from .utils import get_engine, logger


class TaskLogger:
    def __init__(
        self,
        task_name: str,
        alert_slack: bool,
        alert_email: bool,
        alert_on_start: bool,
        alert_on_error: bool,
        alert_on_finish: bool,
        required: bool,
        exit_on_complete: bool,
    ):
        self.task_name = task_name
        self.required = required
        self.exit_on_complete = exit_on_complete
        self.alert_slack = alert_slack
        self.alert_email = alert_email
        self.alert_on_start = alert_on_start
        self.alert_on_error = alert_on_error
        self.alert_on_finish = alert_on_finish
        if (
            not alert_slack
            and not alert_email
            and any([alert_on_start, alert_on_error, alert_on_finish])
        ):
            raise ValueError(
                "Can not send alerts unless `alert_slack` or `alert_email` is True."
            )
        self.engine = get_engine()
        self.errors = []
        self._task_start_recorded = False

    def record_task_start(self):
        self.start_time = datetime.utcnow()
        with self.engine.begin() as conn:
            conn.execute(
                sa.insert(task_runs_table).values(
                    {"name": self.task_name, "started": self.start_time}
                )
            )
        self._task_start_recorded = True
        if self.alert_on_start:
            self._alert_task_start()

    def record_task_error(self, error: Exception):
        self.errors.append(error)
        with self.engine.begin() as conn:
            statement = sa.insert(task_run_errors_table).values(
                {
                    "name": self.task_name,
                    "type": str(type(error)),
                    "message": str(error),
                }
            )
            conn.execute(statement)
        if self.alert_on_error:
            self._alert_task_error(error)

    def record_task_finish(
        self,
        success: bool,
        return_value: Any = None,
        retries: int = 0,
    ) -> datetime:
        if not self._task_start_recorded:
            raise RuntimeError(
                "Task finish can not be recorded unless task start is recoded first."
            )

        self.finish_time = datetime.utcnow()
        self.success = success
        self.return_value = return_value
        self.retries = retries
        self.status = "success" if success else "failed"

        with self.engine.begin() as conn:
            conn.execute(
                sa.update(task_runs_table)
                .where(
                    task_runs_table.c.name == self.task_name,
                    task_runs_table.c.started == self.start_time,
                )
                .values(
                    finished=self.finish_time,
                    retries=self.retries,
                    status=self.status,
                    return_value=self.return_value,
                )
            )

        if self.alert_on_finish:
            self._alert_task_finish()

        if self.errors and self.required:
            if self.exit_on_complete:
                sys.exit(1)
            if len(self.errors) > 1:
                raise Exception(f"Error executing task {self.task_name}: {self.errors}")
            raise type(self.errors[0])(str(self.errors[0]))
        if self.exit_on_complete:
            sys.exit(0 if success else 1)

    def _alert_task_start(self):
        msg = f"Started task {self.task_name} {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"
        components = [
            Text(
                msg,
                size=FontSize.LARGE,
                color=FontColors.IMPORTANT,
            )
        ]
        self._send_alerts(msg, components)

    def _alert_task_error(self, error: Exception):
        subject = f"Error executing task {self.task_name}: {type(error)}"
        components = [
            Text(
                f"{subject} -- {error}",
                size=FontSize.LARGE,
                color=FontColors.ERROR,
            )
        ]
        self._send_alerts(subject, components)

    def _alert_task_finish(self):
        subject = f"{self.status}: {self.task_name}"
        components = [
            Text(
                subject,
                size=FontSize.LARGE,
                color=FontColors.IMPORTANT if self.success else FontColors.ERROR,
            ),
            KV(
                {
                    "Start": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Finish": self.finish_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Return Value": self.return_value,
                }
            ),
        ]
        if self.errors:
            components.append(
                Text(
                    "ERRORS",
                    size=FontSize.LARGE,
                    color=FontColors.ERROR,
                )
            )
            for e in self.errors:
                components.append(
                    Text(
                        f"{type(e)}: {e}",
                        size=FontSize.MEDIUM,
                        color=FontColors.INFO,
                    )
                )
        self._send_alerts(subject, components)

    def _send_alerts(self, subject: str, components: List[AlertComponent]):
        for alert_type in self.alert_types:
            kwargs = {"subject": subject} if alert_type == "email" else {}
            try:
                send_alert(alert_type, components, **kwargs)
            except Exception as e:
                logger.error(f"Error sending alert: {type(e)} -- {e}")


def task(
    task_name: str,
    required: bool = False,
    retries: int = 0,
    timeout: Optional[int] = None,
    alert_slack: Optional[bool] = None,
    alert_email: Optional[bool] = None,
    alert_on_start: Optional[bool] = None,
    alert_on_error: Optional[bool] = None,
    alert_on_finish: Optional[bool] = None,
    exit_on_complete: Optional[bool] = None,
):
    """Decorator for async tasks.

    Args:
        task_name (str): Name which should be used to identify the task.
        required (bool, optional): Requited tasks will raise exceptions. Defaults to False.
        retries (int, optional): How many times the task can be retried on failure. Defaults to 0.
        timeout (Optional[int], optional): Timeout for function execution. Defaults to None.
        alert_slack (Optional[bool]): Send alerts to Slack on selected events.
        alert_email (Optional[bool]): Send email alerts on selected events.
        alert_on_start (Optional[bool]): Send alerts when task starts.
        alert_on_error (Optional[bool]): Send alert on task error,
        alert_on_finish (Optional[bool]): Send alert when task is finshed.
        exit_on_complete (bool): Exit Python interpreter with task restult status code when task is finished. Defaults to False.
    """

    def task_decorator(func):
        @functools.wraps(func)
        async def task_wrapper(*args, **kwargs):
            task_logger = TaskLogger(
                task_name=task_name,
                required=required,
                alert_slack=alert_slack or os.getenv("TASK_FLOWS_ALERT_SLACK"),
                alert_email=alert_email or os.getenv("TASK_FLOWS_ALERT_EMAIL"),
                alert_on_start=alert_on_start or os.getenv("TASK_FLOWS_ALERT_ON_START"),
                alert_on_error=alert_on_error or os.getenv("TASK_FLOWS_ALERT_ON_ERROR"),
                alert_on_finish=alert_on_finish
                or os.getenv("TASK_FLOWS_ALERT_ON_FINISH"),
                exit_on_complete=exit_on_complete,
            )
            task_logger.record_task_start()
            for i in range(retries + 1):
                try:
                    if timeout:
                        result = await asyncio.wait_for(func(*args, **kwargs), timeout)
                    else:
                        result = await func(*args, **kwargs)
                    task_logger.record_task_finish(
                        success=True, retries=i, return_value=result
                    )
                    return result
                except Exception as e:
                    logger.error(
                        f"Error executing task {task_name}. Retries remaining: {retries-i}.\n({type(e)}) -- {e}"
                    )
                    task_logger.record_task_error(e)
            task_logger.record_task_finish(success=False, retries=retries)

        return task_wrapper

    return task_decorator
