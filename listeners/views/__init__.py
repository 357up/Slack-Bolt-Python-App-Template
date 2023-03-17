from slack_bolt.app.async_app import AsyncApp
from .sample_view import sample_view_callback


async def register(app: AsyncApp):
    app.view("sample_view_id")(sample_view_callback)
