# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_outbox_pattern',
 'django_outbox_pattern.management',
 'django_outbox_pattern.management.commands',
 'django_outbox_pattern.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2', 'stomp.py>=8.0.1,<9']

setup_kwargs = {
    'name': 'django-outbox-pattern',
    'version': '0.1.0',
    'description': 'A Django app to make it easier to use the transactional outbox pattern',
    'long_description': '\n# Django outbox pattern\n[![Build Status](https://dev.azure.com/juntos-somos-mais-loyalty/python/_apis/build/status/juntossomosmais.django-outbox-pattern?branchName=azure-pipelines)](https://dev.azure.com/juntos-somos-mais-loyalty/python/_build/latest?definitionId=307&branchName=azure-pipelines)\n[![Maintainability Rating](http://https://sonarcloud.io/api/project_badges/measure?project=juntossomosmais_django-outbox-pattern&metric=sqale_rating)](http://https://sonarcloud.io/dashboard?id=juntossomosmais_django-outbox-pattern)\n[![Coverage](http://https://sonarcloud.io/api/project_badges/measure?project=juntossomosmais_django-outbox-pattern&metric=coverage)](http://https://sonarcloud.io/dashboard?id=juntossomosmais_django-outbox-pattern)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/ambv/black)\n[![Downloads](https://pepy.tech/badge/django-outbox-pattern)](https://pepy.tech/project/django-outbox-pattern)\n[![Downloads](https://pepy.tech/badge/django-outbox-pattern/month)](https://pepy.tech/project/django-outbox-pattern/month)\n[![Downloads](https://pepy.tech/badge/django-outbox-pattern/week)](https://pepy.tech/project/django-outbox-pattern/week)\n[![PyPI version](https://badge.fury.io/py/django-outbox-pattern.svg)](https://badge.fury.io/py/django-outbox-pattern)\n[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/juntossomosmais/django-outbox-pattern/blob/master/LICENSE)\n\nMaking Transactional Outbox easy\n\n## Installation\n\nInstall django-outbox-pattern with pip\n\n```bash\n  pip install django-outbox-pattern\n```\n\nAdd to settings\n\n```python\n    # settings.py\n\n    INSTALLED_APPS = [\n        ...\n        "django_outbox_pattern",\n        ...\n    ]\n\n    DJANGO_OUTBOX_PATTERN = {\n      "DEFAULT_STOMP_HOST_AND_PORTS": [("127.0.0.1", 61613)],\n      "DEFAULT_STOMP_USERNAME": "guest",\n      "DEFAULT_STOMP_PASSCODE": "guest",\n    }\n\n```\n\n## Usage/Examples\n\nThe `publish` decorator adds the outbox table to the model. `\npublish` accepts three parameters, the `destination` which is required,\nfields which the default are all the `fields` of the model and `serializer` which by default adds the id in the message to be sent.\n`fields` and `serializer` are mutually exclusive.\n\n__Only destination__\n\n```python\nfrom django.db import models\nfrom django_outbox_pattern.decorators import publish\n\n\n@publish(destination=\'/topic/my_route_key\')\nclass MyModel(models.Model):\n    field_one = models.CharField(max_length=100)\n    field_two = models.CharField(max_length=100)\n```\n\nThis generates the following data to be sent.\n\n```python\nproducer.send(destination=\'/topic/my_route_key.v1\', body=\'{"id": 1, "field_one": "Field One", "field_two": "Field Two"}\')\n```\n\n__With fields__\n\n```python\nfrom django.db import models\nfrom django_outbox_pattern.decorators import publish\n\n\n@publish(destination=\'/topic/my_route_key\', fields=["field_one"])\nclass MyModel(models.Model):\n    field_one = models.CharField(max_length=100)\n    field_two = models.CharField(max_length=100)\n```\n\nThis generates the following data to be sent.\n\n```python\nproducer.send(destination=\'/topic/my_route_key.v1\', body=\'{"id": 1, "field_one": "Field One"}\')\n```\n\n__With serializer__\n\n```python\nfrom django.db import models\nfrom django_outbox_pattern.decorators import publish\n\n\n@publish(destination=\'/topic/my_route_key\', serializer=\'my_serializer\')\nclass MyModel(models.Model):\n    field_one = models.CharField(max_length=100)\n    field_two = models.CharField(max_length=100)\n\n    def my_serializer(self):\n        return {\n            "id": self.id,\n            "one": self.field_one,\n            "two": self.field_two\n        }\n```\n\nThis generates the following data to be sent.\n\n```python\nproducer.send(destination=\'/topic/my_route_key.v1\', body=\'{"id": 1, "one": "Field One", "two": "Field Two"}\')\n```\n## Publish/Subscribe commands\n\nTo send the messages added to the outbox table it is necessary to start the producer.\n\n```python\npython manage.py publish\n```\n\nDjango outbox pattern also provides a consumer that can be used to receive outgoing messages.\n\n\n```python\n# callbacks.py\n\n# Create a function that receives an instance of django_outbox_pattern.payloads.Payload\n\ndef callback(payload):\n    try:\n        # Do anything\n        payload.ack()\n    except Exception:\n        # nack is automatically called in case of errors, but you might want to handle the error in another way\n        payload.nack()\n```\n\n```python\npython manage.py subscribe \'dotted.path.to.callbacks.callback` \'/topic/my_route_key.v1\'\n```\n\n## Settings\n',
    'author': 'Hugo Brilhante',
    'author_email': 'hugobrilhante@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/juntossomosmais/django-outbox-pattern',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
