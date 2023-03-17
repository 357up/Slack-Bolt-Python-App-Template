from logging import Logger


async def app_home_opened_callback(client, event, logger: Logger, context):
    # ignore the app_home_opened event for anything but the Home tab
    if event["tab"] != "home":
        return
    try:
        jira_api_key = (
            context["user_config"]["jira_api_key"] if context["user_config"]["jira_api_key"] else "Enter your Jira API key"
        )
        cron_spec = context["user_config"]["cron_spec"] if context["user_config"]["cron_spec"] else "0 9,17 * * 1-5"
        await client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "callback_id": "reminder_setup_modal",
                "title": {"type": "plain_text", "text": "Set Reminder Schedule", "emoji": True},
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "jira_api_key",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "jira_api_key_input",
                            "placeholder": {"type": "plain_text", "text": jira_api_key[0:147] + "..."},
                        },
                        "label": {"type": "plain_text", "text": "Jira API Key", "emoji": True},
                    },
                    {
                        "type": "input",
                        "block_id": "cron_spec",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "cron_spec_input",
                            "placeholder": {"type": "plain_text", "text": cron_spec},
                        },
                        "label": {"type": "plain_text", "text": "Cron Spec", "emoji": True},
                        "hint": {
                            "type": "plain_text",
                            "text": "e.g. '0 9,17 * * 1-5' will send reminders on 09:00 and 17:00, Monday through Friday",
                        },
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Save", "emoji": True},
                                "action_id": "save_config_id",
                            },
                        ],
                    },
                ],
            },
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
