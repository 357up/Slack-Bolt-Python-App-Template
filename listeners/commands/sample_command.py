from slack_bolt import Ack, Respond
from logging import Logger


async def sample_command_callback(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        await ack()
        await respond(f"Responding to the sample command! Your command was: {command['text']}")
    except Exception as e:
        logger.error(e)
