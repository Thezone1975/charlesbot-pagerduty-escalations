from charlesbot.base_plugin import BasePlugin
from charlesbot.config import configuration
from charlesbot.util.parse import parse_msg_with_prefix
from charlesbot.util.parse import does_msg_contain_prefix
from charlesbot.slack.slack_user import SlackUser
from charlesbot.slack.slack_message import SlackMessage
from charlesbot_pagerduty_escalations.http import http_post_request
import asyncio
import json


class PagerdutyEscalations(BasePlugin):

    def __init__(self):
        super().__init__("PagerdutyEscalations")
        self.load_config()

    def load_config(self):  # pragma: no cover
        config_dict = configuration.get()
        self.pd_service_mappings = config_dict['pdescalations']['service_mappings']  # NOQA

    def get_help_message(self):
        help_msg = []
        help_msg.append("!lassie <service> - Triggers a Pagerduty incident and assigns it to that service")  # NOQA
        help_msg.append("!lassie services - Lists all the available Pagerduty services")  # NOQA
        return "\n".join(help_msg)

    def get_trigger_payload(self, service_key, service_name, escalating_user):
        return {
            "service_key": service_key,
            "event_type": "trigger",
            "description": "Service escalation for %s (triggered by %s)" % (service_name, escalating_user),  # NOQA
            "incident_key": "%s-service-escalation" % service_name,
            "client": "charlesbot",
        }

    @asyncio.coroutine
    def trigger_escalation_incident(self, parsed_message, slack_message):
        """
        Trigger a service escalation for the specified service
        """
        service_name = parsed_message.strip()
        service_key = self.pd_service_mappings.get(service_name)
        if not service_key:
            error_msg = "Could not find key for service '%s', check that the service exists in the config file!" % service_name  # NOQA
            self.log.error(error_msg)
            yield from self.slack.send_channel_message(slack_message.channel,
                                                       error_msg)
            return

        slack_user = SlackUser()
        yield from slack_user.retrieve_slack_user_info(self.slack,
                                                       slack_message.user)

        payload = self.get_trigger_payload(service_key,
                                           service_name,
                                           slack_user.real_name)
        response = yield from http_post_request(
            url="https://events.pagerduty.com/generic/2010-04-15/create_event.json",  # NOQA
            payload=json.dumps(payload),
        )
        if not response:
            error_msg = "Could not escalate incident for %s. Check the logs for details." % service_name  # NOQA
            self.log.error(error_msg)
            yield from self.slack.send_channel_message(slack_message.channel,
                                                       error_msg)
            return

        success_msg = "Successfully escalated this %s incident!" % service_name
        self.log.info(success_msg)
        yield from self.slack.send_channel_message(slack_message.channel,
                                                   success_msg)

    @asyncio.coroutine
    def print_service_list(self, slack_message):
        """
        Print out a nicely formtted list of all available services (in Slack)
        """
        service_names = list(self.pd_service_mappings.keys())
        service_names.sort()
        service_msg = "\n".join(service_names)
        formatted_msg = "```\n%s\n```" % service_msg
        yield from self.slack.send_channel_message(slack_message.channel,
                                                   formatted_msg)

    @asyncio.coroutine
    def process_message(self, message):
        """
        Main method that handles all messages sent to this plugin
        """
        if not type(message) is SlackMessage:
            return
        parsed_message = parse_msg_with_prefix("!lassie", message.text)
        if not parsed_message:  # pragma: no cover
            return

        if does_msg_contain_prefix("services", parsed_message):
            yield from self.print_service_list(message)
        else:
            yield from self.trigger_escalation_incident(parsed_message,
                                                        message)
