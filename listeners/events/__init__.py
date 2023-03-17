from slack_bolt.app.async_app import AsyncApp
from .app_home_opened import app_home_opened_callback


async def register(app: AsyncApp):
    app.event("app_home_opened", middleware=[app.get_user_config])(app_home_opened_callback)
