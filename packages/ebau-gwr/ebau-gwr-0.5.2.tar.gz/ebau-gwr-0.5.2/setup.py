# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ebau_gwr',
 'ebau_gwr.linker',
 'ebau_gwr.linker.migrations',
 'ebau_gwr.oidc_auth',
 'ebau_gwr.token_proxy',
 'ebau_gwr.token_proxy.management',
 'ebau_gwr.token_proxy.management.commands',
 'ebau_gwr.token_proxy.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.13,<4.0.0',
 'cryptography>=37.0.2,<38.0.0',
 'django-environ>=0.9.0,<0.10.0',
 'django-filter>=22.1,<23.0',
 'django-generic-api-permissions>=0.2.0,<0.3.0',
 'djangorestframework-jsonapi>=5.0.0,<6.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'mozilla-django-oidc>=2.0.0,<3.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'requests>=2.28.0,<3.0.0',
 'uWSGI>=2.0.20,<3.0.0']

setup_kwargs = {
    'name': 'ebau-gwr',
    'version': '0.5.2',
    'description': 'GWR synchronisation for ebau projects',
    'long_description': '# ebau-gwr\n\n[![Build Status](https://github.com/adfinis-sygroup/ebau-gwr/workflows/Tests/badge.svg)](https://github.com/adfinis-sygroup/ebau-gwr/actions?query=workflow%3ATests)\n[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/adfinis-sygroup/ebau-gwr/blob/main/pyproject.toml#L99)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/adfinis-sygroup/ebau-gwr)\n\nGWR synchronisation for ebau projects\n\n## Getting started\n\n### Installation\n\n**Requirements**\n\n- docker\n- docker-compose\n\nAfter installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/adfinis/ebau-gwr/main/docker-compose.yml) and run the following command:\n\n```bash\ndocker-compose up -d\n```\n\nYou can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).\n\n### Configuration\n\nebau-gwr is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.\nDifferent environment variable types are explained at [django-environ](https://github.com/joke2k/django-environ#supported-types).\n\n#### Common\n\nA list of configuration options which you need to set when using ebau-gwr as a\nstandalone service:\n\n- `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).\n- `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).\n- `DATABASE_ENGINE`: Database backend to use. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE). (default: django.db.backends.postgresql)\n- `DATABASE_HOST`: Host to use when connecting to database (default: localhost)\n- `DATABASE_PORT`: Port to use when connecting to database (default: 5432)\n- `DATABASE_NAME`: Name of database to use (default: ebau-gwr)\n- `DATABASE_USER`: Username to use when connecting to the database (default: ebau-gwr)\n- `DATABASE_PASSWORD`: Password to use when connecting to database\n\n##### App specific settings\n\nA list of configuration options which you need to set in any case:\n\n- `GWR_WSK_ID`: This is the ID that has been assigned to you by the BfS\n- `GWR_FERNET_KEY`: A secret key used for encrypting the passwords in housing stat credentials. Can be generated with the `generate_fernet_key` command\n\nBy default, the app will talk to the GWR production API if running with `ENV=production` (and the test API otherwise). You can overwrite this behavior by setting\n\n- `GWR_HOUSING_STAT_BASE_URI`: base uri of GWR API, e.g. `"https://www-r.housing-stat.ch/regbl/api/ech0216/2"`\n\n## Contributing\n\nLook at our [contributing guidelines](CONTRIBUTING.md) to start with your first contribution.\n\n## Maintenance\n\nA few notes for maintainers can be found [here](MAINTENANCE.md).\n',
    'author': 'Adfinis AG',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adfinis-sygroup/ebau-gwr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
