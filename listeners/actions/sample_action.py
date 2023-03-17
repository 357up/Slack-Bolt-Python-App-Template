from logging import Logger

from slack_bolt import Ack, Say
from slack_sdk import WebClient


async def sample_action_callback(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        await ack()
        await client.views_update(
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            view={
                "type": "modal",
                "callback_id": "sample_view_id",
                "title": {
                    "type": "plain_text",
                    "text": "Update modal title",
                },
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Nice! You updated the modal! 🎉",
                        },
                    },
                    {
                        "type": "image",
                        "image_url": "https://media.giphy.com/media/SVZGEcYt7brkFUyU90/giphy.gif",
                        "alt_text": "Yay! The modal was updated",
                    },
                    {
                        "type": "input",
                        "block_id": "input_block_id",
                        "label": {
                            "type": "plain_text",
                            "text": "What are your hopes and dreams?",
                        },
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "sample_input_id",
                            "multiline": True,
                        },
                    },
                    {
                        "block_id": "select_channel_block_id",
                        "type": "input",
                        "label": {
                            "type": "plain_text",
                            "text": "Select a channel to message the result to",
                        },
                        "element": {
                            "type": "conversations_select",
                            "action_id": "sample_dropdown_id",
                            "response_url_enabled": True,
                        },
                    },
                ],
            },
        )
    except Exception as e:
        logger.error(e)


async def save_config_callback(ack: Ack, client: WebClient, body: dict, logger: Logger, action: dict, say: Say):
    """
    Sample response:
    {
        'type': 'block_actions',
        'user': {
            'id': '13GFQV3YU',
            'username': 'tunelis.eirashtvs',
            'name': 'tunelis.eirashtvs',
            'team_id': '4N1T6HPA1'},
        'api_app_id': 'B0190TD4DRA',
        'token': '4IShjNf0KWIpcvZJBsxFavHG',
        'container': {
            'type': 'view',
            'view_id': 'G30SPVR47S4'},
        'trigger_id': '9.3924.2147349b56583bc0561dc30791fa5c1274d80171c6c2853cb91',
        'team': {
            'id': '4N1T6HPA1',
            'domain': 'niwueebu'},
        'enterprise': None,
        'is_enterprise_install': False,
        'view': {
            'id': 'G30SPVR47S4',
            'team_id': '4N1T6HPA1',
            'type': 'home',
            'blocks': [
                {
                    'type': 'input',
                    'block_id': 'jira_api_key',
                    'label': {
                        'type': 'plain_text',
                        'text': 'Jira API Key',
                        'emoji': True},
                    'optional': False,
                    'dispatch_action': False,
                    'element': {
                        'type': 'plain_text_input',
                        'action_id': 'jira_api_key_input',
                        'placeholder': {
                            'type': 'plain_text',
                            'text': 'Enter your Jira API key',
                            'emoji': True},
                        'dispatch_action_config': {
                            'trigger_actions_on': [
                                'on_enter_pressed']}
                    }
                },
                {
                    'type': 'input',
                    'block_id': 'cron_spec',
                    'label': {
                        'type': 'plain_text',
                        'text': 'Cron Spec',
                        'emoji': True},
                    'hint': {
                        'type': 'plain_text',
                        'text':
                            "For example, '0 9-17 * * 1-5' will send reminders every hour between 9am and 5pm on weekdays",
                        'emoji': True},
                    'optional': False,
                    'dispatch_action': False,
                    'element': {
                        'type': 'plain_text_input',
                        'action_id': 'cron_spec_input',
                        'placeholder': {
                            'type': 'plain_text',
                            'text': 'Enter a cron spec for reminder notifications',
                            'emoji': True},
                        'dispatch_action_config': {
                            'trigger_actions_on': [
                                'on_enter_pressed']}
                    }
                },
                {
                    'type': 'actions',
                    'block_id': 'bKEda',
                    'elements': [
                        {
                            'type': 'button',
                            'action_id': 'save_config_id',
                            'text': {
                                'type': 'plain_text',
                                'text': 'Save',
                                'emoji': True
                            }
                        }
                    ]
                }
            ],
            'private_metadata': '',
            'callback_id': 'reminder_setup_modal',
            'state': {
                'values': {
                    'jira_api_key': {
                        'jira_api_key_input': {
                            'type': 'plain_text_input',
                            'value': 'test'
                        }
                    },
                    'cron_spec': {
                        'cron_spec_input': {
                            'type': 'plain_text_input',
                            'value': 'test'
                        }
                    }
                }
            },
            'hash': '1678195138.BlxSW16t',
            'title': {
                'type': 'plain_text',
                'text': 'View Title',
                'emoji': True
            },
            'clear_on_close': False,
            'notify_on_close': False,
            'close': None,
            'submit': None,
            'previous_view_id': None,
            'root_view_id': 'G30SPVR47S4',
            'app_id': 'B0190TD4DRA',
            'external_id': '',
            'app_installed_team_id': '4N1T6HPA1',
            'bot_id': 'KT0UGG4QRYB'
        },
        'actions': [
            {
                'action_id': 'N3tg',
                'block_id': 'bKEda',
                'text': {
                    'type': 'plain_text',
                    'text': 'Save',
                    'emoji': True
                },
                'type': 'button',
                'action_ts': '1678195493.927961'
            }
        ]
    }
    """
    try:
        await ack()
        # Save config details
        user_id = body.get("user")["id"]
        user_name = body.get("user")["name"]
        jira_api_key = body.get("view")["state"]["values"]["jira_api_key"]["jira_api_key_input"]["value"]
        cron_spec = body.get("view")["state"]["values"]["cron_spec"]["cron_spec_input"]["value"]
        assert (
            jira_api_key and cron_spec
        ), f"{user_name} performed an save config action but it failed. Jira API key and cron spec are required"
        logger.info(f"{user_name} performed an save config action.")
        logger.debug(f"User ID: {user_id}, jira API key: `{jira_api_key}`, Cron spec: `{cron_spec}`")
        say.channel = user_id
        await say(f"Thanks {user_name}! I've saved your config details.")
    except Exception as e:
        logger.error(e)
