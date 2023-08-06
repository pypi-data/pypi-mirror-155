# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mailersend',
 'mailersend.activity',
 'mailersend.analytics',
 'mailersend.base',
 'mailersend.domains',
 'mailersend.emails',
 'mailersend.inbound_routing',
 'mailersend.messages',
 'mailersend.recipients',
 'mailersend.scheduled_messages',
 'mailersend.sms_activity',
 'mailersend.sms_sending',
 'mailersend.templates',
 'mailersend.tokens',
 'mailersend.utils',
 'mailersend.webhooks']

package_data = \
{'': ['*']}

install_requires = \
['pre-commit>=2.12.1,<3.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'mailersend',
    'version': '0.3.2',
    'description': 'The official MailerSend Python SDK',
    'long_description': None,
    'author': 'Igor Hrček',
    'author_email': 'igor@mailerlite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
