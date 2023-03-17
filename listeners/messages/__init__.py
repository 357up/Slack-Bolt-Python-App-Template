import re

from slack_bolt.app.async_app import AsyncApp
from .sample_message import sample_message_callback


# To receive messages from a channel or dm your app must be a member!
async def register(app: AsyncApp):
    app.message(re.compile("(hi|hello|hey)"))(sample_message_callback)
