import asynctest
from asynctest.mock import patch
from asynctest.mock import MagicMock
from asynctest.mock import call
from charlesbot.slack.slack_message import SlackMessage


class TestStringFunctions(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot_pagerduty_escalations.pagerdutyescalations.PagerdutyEscalations.load_config')  # NOQA
        self.addCleanup(patcher1.stop)
        self.mock_load_config = patcher1.start()

        self.slack_message = SlackMessage(type="message",
                                          user="U2147483697",
                                          channel="C2147483705",
                                          text="This is a dummy message")

        from charlesbot_pagerduty_escalations.pagerdutyescalations import PagerdutyEscalations  # NOQA
        self.pd = PagerdutyEscalations()
        self.pd.slack.send_channel_message = MagicMock()

    @asynctest.ignore_loop
    def test_help_msg_two_entries(self):
        help_msg = self.pd.get_help_message()
        self.assertEqual(help_msg.count('\n'), 1)

    def test_print_service_empty_list(self):
        self.pd.pd_service_mappings = {}
        yield from self.pd.print_service_list(self.slack_message)
        expected_call = call("C2147483705", "```\n\n```")
        self.pd.slack.send_channel_message.assert_has_calls([expected_call])

    def test_print_service_one_item(self):
        self.pd.pd_service_mappings = {
            "service1": "key1"
        }
        yield from self.pd.print_service_list(self.slack_message)
        expected_call = call("C2147483705", "```\nservice1\n```")
        self.pd.slack.send_channel_message.assert_has_calls([expected_call])

    def test_print_service_two_items(self):
        self.pd.pd_service_mappings = {
            "service1": "key1",
            "service2": "key2"
        }
        yield from self.pd.print_service_list(self.slack_message)
        expected_call = call("C2147483705", "```\nservice1\nservice2\n```")
        self.pd.slack.send_channel_message.assert_has_calls([expected_call])

    def test_print_service_two_items_sorted(self):
        self.pd.pd_service_mappings = {
            "service2": "key1",
            "service1": "key2"
        }
        yield from self.pd.print_service_list(self.slack_message)
        expected_call = call("C2147483705", "```\nservice1\nservice2\n```")
        self.pd.slack.send_channel_message.assert_has_calls([expected_call])

    @asynctest.ignore_loop
    def test_get_trigger_payload_no_custom_message(self):
        expected_output = {
            "service_key": "key1",
            "event_type": "trigger",
            "description": "Service escalation for website (triggered by marvin)",  # NOQA
            "incident_key": "website-service-escalation",
            "client": "charlesbot",
        }
        received_output = self.pd.get_trigger_payload(
            service_key="key1",
            service_name="website",
            escalating_user="marvin"
        )
        self.assertEqual(received_output, expected_output)

    @asynctest.ignore_loop
    def test_get_trigger_payload_with_custom_message(self):
        expected_output = {
            "service_key": "key1",
            "event_type": "trigger",
            "description": "Service escalation for website (triggered by marvin) -- halp plz",  # NOQA
            "incident_key": "website-service-escalation",
            "client": "charlesbot",
        }
        received_output = self.pd.get_trigger_payload(
            service_key="key1",
            service_name="website",
            escalating_user="marvin",
            custom_message="halp plz"
        )
        self.assertEqual(received_output, expected_output)
