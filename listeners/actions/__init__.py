from slack_bolt.app.async_app import AsyncApp
from .sample_action import sample_action_callback
from .sample_action import save_config_callback


async def register(app: AsyncApp):
    app.action("sample_action_id")(sample_action_callback)
    app.action("save_config_id", middleware=[app.process_user_config])(save_config_callback)
