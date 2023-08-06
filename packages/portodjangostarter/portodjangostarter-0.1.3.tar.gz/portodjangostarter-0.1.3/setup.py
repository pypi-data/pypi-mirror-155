# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portodjangostarter',
 'portodjangostarter._app_template.migrations',
 'portodjangostarter._app_template.models',
 'portodjangostarter._app_template.tests',
 'portodjangostarter.management',
 'portodjangostarter.management.commands']

package_data = \
{'': ['*'],
 'portodjangostarter': ['_app_template/*',
                        '_app_template/actions/*',
                        '_app_template/tasks/*',
                        '_app_template/ui/api/controllers/*',
                        '_app_template/ui/api/routes/*',
                        '_app_template/ui/api/transformers/*']}

setup_kwargs = {
    'name': 'portodjangostarter',
    'version': '0.1.3',
    'description': 'With portodjangostarter we can start porto containers in django project',
    'long_description': "# Porto container starter\n\nThis package uses to start a porto container\n\nYou can install this package very simple\n\n## Installation\n\n\n```bash\n  pip install portodjangostarter\n```\n\n#### Add package to installed apps\n\n```python\n  INSTALLED_APPS = [\n    ...\n    'django.contrib.staticfiles',\n    'portodjangostarter',\n    ...\n]\n```\n\n### And use it for happy 🚀\n```python\n   python manage.py startcontainer {{app_name}}\n```\n\n",
    'author': 'BakdauletBolat',
    'author_email': 'bakosh21345@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BakdauletBolat/portodjangostarter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
