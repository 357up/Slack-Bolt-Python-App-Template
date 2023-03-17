from slack_bolt.app.async_app import AsyncApp
import os
from json import dumps, loads
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from typing import Optional
from aiohttp import web
from croniter import croniter

from listeners import register_listeners

from ..crontab import MyAppCrontab as Crontab


class MyAppExtensions(AsyncApp):
    socket_mode_client: Optional[SocketModeClient] = None
    botID = None
    appUsers = {}
    appUserConfig = {}
    dataPath = (
        os.path.abspath(os.environ.get("APP_DATA_DIR"))
        if os.environ.get("APP_DATA_DIR")
        else os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
    )

    async def register_callback_listeners(self, *args):
        await register_listeners(self)

    async def start_socket_mode(self, _web_app: web.Application):
        handler = AsyncSocketModeHandler(self, os.environ["SLACK_APP_TOKEN"], ping_interval=30)
        await handler.connect_async()
        self.socket_mode_client
        self.socket_mode_client = handler.client

    async def shutdown_socket_mode(self, _web_app: web.Application):
        self.socket_mode_client
        await self.socket_mode_client.close()

    async def healthcheck(self, _req: web.Request):
        if self.socket_mode_client is not None and await self.socket_mode_client.is_connected():
            return web.Response(status=200, text="OK")
        return web.Response(status=503, text="The Socket Mode client is inactive")

    async def register_healthcheck_endpoint(self, web_app: web.Application):
        web_app.add_routes([web.get("/health", self.healthcheck)])

    async def start_crontab(self, *args):
        self.crontab = Crontab(self)
        await self.crontab.start()

    def save_user_config(self):
        json_object = dumps(self.appUserConfig, indent=4)
        with open(os.path.join(self.dataPath, "config.json"), "w") as outfile:
            outfile.write(json_object)

    async def send_notification(self, user_id: str, spec: str):
        await self.client.chat_postMessage(
            channel=user_id, text=f"Hello <@{user_id}>! You have a scheduled punch clock reminder at {spec}."
        )

    async def process_user_config(self, ack, body, next, *argv):
        def validate_config(config: dict):
            # TODO: Validate `jira_api_key`
            if croniter.is_valid(config["cron_spec"]) and config["jira_api_key"]:
                return True
            return False

        def get_config_values(body):
            user_id = body.get("user")["id"]
            user_name = body.get("user")["name"]
            jira_api_key = body.get("view")["state"]["values"]["jira_api_key"]["jira_api_key_input"]["value"]
            cron_spec = body.get("view")["state"]["values"]["cron_spec"]["cron_spec_input"]["value"]
            config = {"user_name": user_name, "jira_api_key": jira_api_key, "cron_spec": cron_spec}
            if validate_config(config):
                return user_id, config
            return user_id, None

        await ack()

        user_id, user_config = get_config_values(body)
        if user_config is not None:
            self.appUserConfig[user_id] = user_config
            self.save_user_config()
            await next()
        else:
            raise ValueError(f"User {user_id} provided invalid config. Configuration was not saved.")

    async def get_user_config(self, ack, next, context, *argv):
        user_id = context["user_id"]
        user_config = self.appUserConfig[user_id] if user_id in self.appUserConfig else None
        if user_config is not None:
            context["user_config"] = user_config
            await next()
        else:
            await ack()

    async def load_user_config(self, *args):
        with open(os.path.join(self.dataPath, "config.json"), "r") as infile:
            contents = infile.read()
        self.appUserConfig = loads(contents)

    async def schedule_notification_for_users(self, *args):
        for user in self.appUsers:
            if user in self.appUserConfig:
                self.crontab.schedule_notification_for_user(user, self.appUserConfig[user]["cron_spec"])

    async def query_users(self, *args):
        bot = await self.client.auth_test()
        bot_bot_id = bot.data.get("bot_id")
        bot_user_id = bot.data.get("user_id")
        assert bot_user_id is not None and bot_bot_id is not None
        self.botID = bot_bot_id
        appChannels = await self.client.users_conversations()
        appChannels = appChannels.data.get("channels")
        for channel in appChannels:
            channelUsers = await self.client.conversations_members(channel=channel["id"])
            channelUsers = channelUsers.data.get("members")
            for user in channelUsers:
                if user not in self.appUsers and user != bot_user_id:
                    userData = await self.client.users_info(user=user)
                    userData = userData.data.get("user")
                    if userData is not None and userData.get("deleted") is False:
                        self.appUsers[user] = userData
        if len(self.appUsers) == 0:
            self.appUsers[bot_user_id] = bot.data

        json_object = dumps(self.appUsers, indent=4)
        with open(os.path.join(self.dataPath, "users.json"), "w") as outfile:
            outfile.write(json_object)
