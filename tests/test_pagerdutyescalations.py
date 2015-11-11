import asynctest
from charlesbot_pagerduty_escalations.pagerdutyescalations import PagerdutyEscalations

class TestPagerdutyEscalations(asynctest.TestCase):

    def setUp(self):
        test_plug = PagerdutyEscalations()  # NOQA

    def tearDown(self):
        pass

    @asynctest.ignore_loop
    def test_something(self):
        pass
