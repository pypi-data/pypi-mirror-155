# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_sentry']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0,<5.0', 'sentry-sdk>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'dj-sentry',
    'version': '0.2.0',
    'description': 'A Django app to initialize Sentry client for your Django applications',
    'long_description': '# Dj_sentry\n\nThis Django application intialize [Sentry SDK](https://docs.sentry.io/platforms/python/) to your Django application.\n\n## How to install\n\nYou can install this packaging by using:\n\n```bash\npip install dj_sentry\n```\n\nAlternatively, if you use a package manager, for example Poetry, you can use:\n\n```bash\npoetry add dj_sentry\n```\n\n## How to configure\n\nIn your `settings`files, add the following settings to configure the Sentry SDK according with your needs:\n\n| Setting                      | Type                | Description |\n|------------------------------|---------------------|-------------|\n| `SENTRY_DSN`                 | `str` **mandatory** | [Sentry project DSN](https://docs.sentry.io/product/sentry-basics/dsn-explainer/). |\n| `SENTRY_ENVIRONMENT`         | `str` **mandatory** | Environment where the application is running (for example: *production*, *pre-production*, *staging*) |\n| `SENTRY_APP_PACKAGE_NAME`    | `str` *optional*    | Package name of your application¹. |\n| `SENTRY_EXTRA_INTEGRATIONS`  | `list` *optional*   | List of [Sentry integrations](https://docs.sentry.io/platforms/python/configuration/integrations/) you want to use (in addition of the Django integration already set-up)  |\n| `SENTRY_EXTRA_OPTS`          | `dict` *optional*   | Dict with additionnal settings for configuring the Sentry client. See [Sentry client configuration](https://docs.sentry.io/platforms/python/configuration/) |\n\n¹: We use [`pkg_resources`](https://setuptools.pypa.io/en/latest/pkg_resources.html) from Setuptools to get the package version of your application and send it on every events. This setting is optional but **highly** recommended.\n\nBy default, the setting [`traces_sample_rate`](https://docs.sentry.io/platforms/python/configuration/options/#traces-sample-rate) [`send_default_pii`](https://docs.sentry.io/platforms/python/configuration/options/#send-default-pii) have the following default values\n\n| Setting                      | Value                                     |\n|------------------------------|-------------------------------------------|\n| `traces_sample_rate`         | `0` (no tracing samples sent to Sentry)   |\n| `send_default_pii`           | `True` (send user information in events)  |\n\nYou can change de values of those settings by using the `SENTRY_EXTRA_OPTS` setting. For example, to disable the setting that send user informations:\n\n```python\nSENTRY_EXTRA_OPTS = {\n    "send_default_pii": False,  # Do not send user information in Sentry events\n}\n```\n\nHere\'s an example of valid configuration:\n\n```python\nfrom sentry_sdk.integrations.redis import RedisIntegration\nfrom company_cms.utils.sentry import before_send_filter\n\n# Your Django configuration ...\n\nSENTRY_DSN = "https://<token>@sentry.company.com/<project_id>"\nSENTRY_ENVIRONMENT = "production"\nSENTRY_APP_PACKAGE_NAME = "company_cms"\nSENTRY_EXTRA_INTEGRATIONS = [RedisIntegration()]  # Add Redis integration to Sentry SDK\nSENTRY_EXTRA_OPTS = {\n    "before_send": before_send_filter,  # Do some events filtering before sending them (see: https://docs.sentry.io/platforms/python/configuration/filtering/)\n}\n\n# Your Django configuration ...\n```\n\n## License\n\nThis project is released under [BSD-3 Clause](LICENSE.md).\n',
    'author': 'Michael Vieira',
    'author_email': 'dev@mvieira.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/themimitoof/dj_sentry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
