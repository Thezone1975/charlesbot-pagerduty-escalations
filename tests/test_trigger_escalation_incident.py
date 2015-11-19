import asynctest
from asynctest.mock import patch
from asynctest.mock import MagicMock
from asynctest.mock import call
from charlesbot.slack.slack_message import SlackMessage


class TestTriggerEscalationIncident(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot_pagerduty_escalations.pagerdutyescalations.PagerdutyEscalations.load_config')  # NOQA
        self.addCleanup(patcher1.stop)
        self.mock_load_config = patcher1.start()

        patcher2 = patch('charlesbot_pagerduty_escalations.pagerdutyescalations.SlackUser')  # NOQA
        self.addCleanup(patcher2.stop)
        self.mock_slack_user = patcher2.start()

        patcher3 = patch('charlesbot_pagerduty_escalations.pagerdutyescalations.http_post_request')  # NOQA
        self.addCleanup(patcher3.stop)
        self.mock_http_post_request = patcher3.start()

        patcher4 = patch('charlesbot_pagerduty_escalations.pagerdutyescalations.PagerdutyEscalations.get_trigger_payload')  # NOQA
        self.addCleanup(patcher4.stop)
        self.mock_get_trigger_payload = patcher4.start()

        self.slack_message = SlackMessage(type="message",
                                          user="U2147483697",
                                          channel="C2147483705",
                                          text="This is a dummy message")

        from charlesbot_pagerduty_escalations.pagerdutyescalations import PagerdutyEscalations  # NOQA
        self.pd = PagerdutyEscalations()
        self.pd.slack = MagicMock()
        self.pd.slack.send_channel_message = MagicMock()
        self.pd.pd_service_mappings = {
            "service1": "pd_key_1"
        }

    def test_service_key_not_found_no_message(self):
        yield from self.pd.trigger_escalation_incident("website",
                                                       self.slack_message)
        expected_call = call(
            "C2147483705",
            "Could not find key for service 'website', check that the service exists in the config file!"  # NOQA
        )
        self.pd.slack.send_channel_message.assert_has_calls([expected_call])
        self.assertEqual(len(self.mock_slack_user.mock_calls), 0)
        self.assertEqual(len(self.mock_http_post_request.mock_calls), 0)

    def test_service_key_not_found_with_message(self):
        yield from self.pd.trigger_escalation_incident("website halp plz",
                                                       self.slack_message)
        expected_call = call(
            "C2147483705",
            "Could not find key for service 'website', check that the service exists in the config file!"  # NOQA
        )
        self.pd.slack.send_channel_message.assert_has_calls([expected_call])
        self.assertEqual(len(self.mock_slack_user.mock_calls), 0)
        self.assertEqual(len(self.mock_http_post_request.mock_calls), 0)

    def test_failed_http_post(self):
        self.mock_http_post_request.side_effect = [False]
        self.mock_get_trigger_payload.return_value = {
            "payload": "test payload"
        }

        yield from self.pd.trigger_escalation_incident("service1",
                                                       self.slack_message)
        expected_slack_user_call = call(self.pd.slack, "U2147483697")
        self.mock_slack_user.assert_has_calls([expected_slack_user_call])

        expected_http_post_call = call(
            url="https://events.pagerduty.com/generic/2010-04-15/create_event.json",  # NOQA
            payload='{"payload": "test payload"}'
        )
        self.mock_http_post_request.assert_has_calls([expected_http_post_call])

        expected_send_channel_message_call = call(
            "C2147483705",
            "Could not escalate incident for service1. Check the logs for details."  # NOQA
        )
        self.pd.slack.send_channel_message.assert_has_calls(
            [expected_send_channel_message_call]
        )
        self.assertEqual(len(self.pd.slack.send_channel_message.mock_calls), 2)

    def test_successful_http_post(self):
        self.mock_http_post_request.side_effect = [True]
        self.mock_get_trigger_payload.return_value = {
            "payload": "test payload"
        }

        yield from self.pd.trigger_escalation_incident("service1",
                                                       self.slack_message)
        expected_slack_user_call = call(self.pd.slack, "U2147483697")
        self.mock_slack_user.assert_has_calls([expected_slack_user_call])

        expected_http_post_call = call(
            url="https://events.pagerduty.com/generic/2010-04-15/create_event.json",  # NOQA
            payload='{"payload": "test payload"}'
        )
        self.mock_http_post_request.assert_has_calls([expected_http_post_call])

        expected_send_channel_message_call = call(
            "C2147483705",
            "Successfully escalated this service1 incident!"  # NOQA
        )
        self.pd.slack.send_channel_message.assert_has_calls(
            [expected_send_channel_message_call]
        )
        self.assertEqual(len(self.pd.slack.send_channel_message.mock_calls), 2)
