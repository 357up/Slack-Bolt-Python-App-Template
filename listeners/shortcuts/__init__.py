from slack_bolt.app.async_app import AsyncApp
from .sample_shortcut import sample_shortcut_callback


async def register(app: AsyncApp):
    app.shortcut("sample_shortcut_id")(sample_shortcut_callback)
