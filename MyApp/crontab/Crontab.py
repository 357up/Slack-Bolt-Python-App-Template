import aiocron
from time import ctime
from typing import Dict, Optional  # noqa: F401

from slack_bolt.app.async_app import AsyncApp


class MyAppCrontab:
    def __init__(self, app: AsyncApp):
        self.app = app
        self.jobs: Dict[str, aiocron.Cron] = {}

    async def start(self, *args):
        self.jobs: Dict[str, aiocron.Cron] = {}
        self.app.logger.debug("Starting crontab")
        attime = aiocron.crontab(
            "* * * * * */15",
            func=lambda: self.app.logger.debug(f"Crontab active. Next check: {ctime(attime.croniter.get_next(float))}"),
        )

    async def stop(self, *args):
        raise NotImplementedError

    def schedule_notification_for_user(self, user_id: str, spec: str):
        job = aiocron.crontab(spec, func=self.app.send_notification, args=(user_id, spec), start=True)
        self.jobs[user_id] = job

    def unschedule_notification_for_user(self, user_id: str):
        if user_id in self.jobs:
            self.jobs[user_id].stop()
            del self.jobs[user_id]

    def verify(self) -> bool:
        raise NotImplementedError
