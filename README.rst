=====================
Pagerduty Escalations
=====================

.. image:: https://img.shields.io/travis/freshbooks/charlesbot-pagerduty-escalations/master.svg?style=flat-square
    :target: https://travis-ci.org/freshbooks/charlesbot-pagerduty-escalations
    :alt: Travis CI
.. image:: https://img.shields.io/coveralls/freshbooks/charlesbot-pagerduty-escalations/master.svg?style=flat-square
    :target: https://coveralls.io/github/freshbooks/charlesbot-pagerduty-escalations?branch=master
    :alt: Code Coverage
.. image:: https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square
    :target: LICENSE.txt
    :alt: Software License

A Charlesbot__ plugin to create an incident in Pagerduty and assign it to a
specific service.

__ https://github.com/marvinpinto/charlesbot


How does this work
------------------

This plugin adds the following two ``!help`` targets:

.. code:: text

    !lassie <service> [optional message] - Triggers a Pagerduty incident and assigns it to that service
    !lassie services - Lists all the available Pagerduty services

Creating an escalation event triggers an incident in Pagerduty and assigns it
to the specified service. Using a Slack__ interface that people are already
comfortable with, this could be a very useful and efficient way of getting the
attention of the right people during an emergency.

__ https://slack.com


Installation
------------

.. code:: bash

    pip install charlesbot-pagerduty-escalations

Instructions for how to run Charlesbot are over at https://github.com/marvinpinto/charlesbot!


Configuration
-------------

First off, create one or more services in Pagerduty of type Generic API. This
plugin makes use of a service's **Integration Key** to trigger escalation
events.

In your Charlesbot ``config.yaml``, enable this plugin by adding the following
entry to the ``main`` section:

.. code:: yaml

    main:
      enabled_plugins:
        - 'charlesbot_pagerduty_escalations.pagerdutyescalations.PagerdutyEscalations'

Then add a ``pdescalations`` dictionary block that looks something like:

.. code:: yaml

    pdescalations:
      service_mappings:
        service_one_name: 's1_pd_key'
        service_two_name: 's2_pd_key'

The name that you assign your service will be the name that shows up when a
person issues the ``!lassie services`` command. The corresponding key here is
the **Integration Key** associated with that service (in Pagerduty).

Sample config file
~~~~~~~~~~~~~~~~~~

.. code:: yaml

    main:
      slackbot_token: 'xoxb-1234'
      enabled_plugins:
        - 'charlesbot_pagerduty_escalations.pagerdutyescalations.PagerdutyEscalations'

    pdescalations:
      service_mappings:
        service_one_name: 's1_pd_key'
        service_two_name: 's2_pd_key'


License
-------
See the LICENSE.txt__ file for license rights and limitations (MIT).

__ ./LICENSE.txt
