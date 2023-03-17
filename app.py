import os
import logging

from dotenv import load_dotenv

from aiohttp import web

from MyApp import MyAppExtensions as App


# Initialization
load_dotenv()

logger = logging.basicConfig(level=logging.DEBUG)

app = App(signing_secret=os.environ["SLACK_SIGNING_SECRET"], token=os.environ.get("SLACK_BOT_TOKEN"), logger=logger)

web_app = app.web_app()

# Start Bolt app
if __name__ == "__main__":
    web_app.on_startup.append(app.register_callback_listeners)
    web_app.on_startup.append(app.register_healthcheck_endpoint)
    web_app.on_startup.append(app.start_socket_mode)
    web_app.on_startup.append(app.query_users)
    web_app.on_startup.append(app.load_user_config)
    web_app.on_startup.append(app.start_crontab)
    web_app.on_startup.append(app.schedule_notification_for_users)

    # web_app.on_shutdown.append(crontab.stop)
    web_app.on_shutdown.append(app.shutdown_socket_mode)

    web.run_app(app=web_app, port=os.environ.get("APP_PORT") if os.environ.get("APP_PORT") else 8080)
