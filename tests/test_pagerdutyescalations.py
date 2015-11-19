import asynctest
from asynctest.mock import patch
from asynctest.mock import call
from charlesbot.slack.slack_message import SlackMessage


class TestPagerdutyEscalations(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot_pagerduty_escalations.pagerdutyescalations.PagerdutyEscalations.load_config')  # NOQA
        self.addCleanup(patcher1.stop)
        self.mock_load_config = patcher1.start()

        patcher2 = patch('charlesbot_pagerduty_escalations.pagerdutyescalations.PagerdutyEscalations.print_service_list')  # NOQA
        self.addCleanup(patcher2.stop)
        self.mock_print_service_list = patcher2.start()

        patcher3 = patch('charlesbot_pagerduty_escalations.pagerdutyescalations.PagerdutyEscalations.trigger_escalation_incident')  # NOQA
        self.addCleanup(patcher3.stop)
        self.mock_trigger_escalation_incident = patcher3.start()

        from charlesbot_pagerduty_escalations.pagerdutyescalations import PagerdutyEscalations  # NOQA
        self.pd = PagerdutyEscalations()

    def test_process_message_non_slack_message(self):
        message = "!lassie services this is my message to you ooh ooh"
        yield from self.pd.process_message(message)
        self.assertEqual(self.mock_print_service_list.mock_calls, [])
        self.assertEqual(self.mock_trigger_escalation_incident.mock_calls, [])

    def test_process_message_non_lassie_message(self):
        message = SlackMessage(type="message",
                               user="U2147483697",
                               channel="C2147483705",
                               text="This is my message to you ooh ooh")
        yield from self.pd.process_message(message)
        self.assertEqual(self.mock_print_service_list.mock_calls, [])
        self.assertEqual(self.mock_trigger_escalation_incident.mock_calls, [])

    def test_process_message_invalid_lassie_message(self):
        message = SlackMessage(type="message",
                               user="U2147483697",
                               channel="C2147483705",
                               text="!lassie")
        yield from self.pd.process_message(message)
        self.assertEqual(self.mock_print_service_list.mock_calls, [])
        self.assertEqual(self.mock_trigger_escalation_incident.mock_calls, [])

    def test_process_message_services_message_one(self):
        message = SlackMessage(type="message",
                               user="U2147483697",
                               channel="C2147483705",
                               text="!lassie services")
        yield from self.pd.process_message(message)
        expected_call = call(message)
        self.assertEqual(self.mock_print_service_list.mock_calls,
                         [expected_call])
        self.assertEqual(self.mock_trigger_escalation_incident.mock_calls, [])

    def test_process_message_services_message_two(self):
        message = SlackMessage(type="message",
                               user="U2147483697",
                               channel="C2147483705",
                               text="!lassie services some filler we ignore")
        yield from self.pd.process_message(message)
        expected_call = call(message)
        self.assertEqual(self.mock_print_service_list.mock_calls,
                         [expected_call])
        self.assertEqual(self.mock_trigger_escalation_incident.mock_calls, [])

    def test_process_message_escalate_one(self):
        message = SlackMessage(type="message",
                               user="U2147483697",
                               channel="C2147483705",
                               text="!lassie website")
        yield from self.pd.process_message(message)
        expected_call = call("website", message)
        self.assertEqual(self.mock_print_service_list.mock_calls, [])
        self.assertEqual(self.mock_trigger_escalation_incident.mock_calls,
                         [expected_call])

    def test_process_message_escalate_two(self):
        message = SlackMessage(type="message",
                               user="U2147483697",
                               channel="C2147483705",
                               text="!lassie website halp plz")
        yield from self.pd.process_message(message)
        expected_call = call("website halp plz", message)
        self.assertEqual(self.mock_print_service_list.mock_calls, [])
        self.assertEqual(self.mock_trigger_escalation_incident.mock_calls,
                         [expected_call])
