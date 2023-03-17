from slack_bolt.app.async_app import AsyncApp
from .sample_command import sample_command_callback


async def register(app: AsyncApp):
    app.command("/sample-command")(sample_command_callback)
