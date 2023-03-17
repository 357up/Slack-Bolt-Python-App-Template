from listeners import actions
from listeners import commands
from listeners import events
from listeners import messages
from listeners import shortcuts
from listeners import views


async def register_listeners(app):
    await actions.register(app)
    await commands.register(app)
    await events.register(app)
    await messages.register(app)
    await shortcuts.register(app)
    await views.register(app)
