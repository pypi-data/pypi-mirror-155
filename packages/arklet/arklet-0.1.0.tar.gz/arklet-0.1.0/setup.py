# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ark',
 'ark.management',
 'ark.management.commands',
 'ark.migrations',
 'ark_import']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['Django>=3.2,<3.3'],
 ':python_version >= "3.8"': ['Django>=3.2'],
 'environ': ['django-environ>=0.8.1,<0.9.0'],
 'postgres': ['psycopg2>=2.7,<3.0'],
 'sentry': ['sentry-sdk>=1.5.12,<2.0.0']}

entry_points = \
{'console_scripts': ['createsuperuser = server:createsuperuser',
                     'migrate = server:migrate',
                     'server = server:main']}

setup_kwargs = {
    'name': 'arklet',
    'version': '0.1.0',
    'description': 'An unassuming ARK minter, binder, and resolver',
    'long_description': '# Arklet - A basic ARK resolver\n\n![lint_python](https://github.com/internetarchive/arklet/actions/workflows/lint_python.yml/badge.svg)\n\n\n## What is an ARK?\nSee https://arks.org/\n\n## What is Arklet?\nArklet is a Python Django application for minting, binding, and resolving ARKs.\nIt is intended to follow best practices set out by https://arks.org/.\n\nTechnical design notes:\n- Django is the only required dependency.\n- Supports each Django and Python version that is itself supported by the maintainers (Python 3.7-3.10, Django 3.2.x-4.0.x).\n    - Tests are run against the upcoming versions of Python and Django as well. \n- This repo can be run as a standalone service \n- ...or the ark package can be installed as a reusable app in other Django projects. \n    - If using the included arklet/settings.py file django-environ is also required.\n- Arklet is database agnostic.\n\nArklet is developed with poetry, pytest, black, tox, and more.\n\n## Running\n\n### Locally with Postgres\n\nCreate the default `.env` file in the project\'s root directory\n\n```\n# /!\\ Set your own secret key /!\\\nARKLET_DJANGO_SECRET_KEY=[YOUR_SECRET]\n\n# For local development, set to True\nARKLET_DEBUG=True\n```\n\nThe following steps walk through running Postgres, installing with poetry, and starting\nthe app. You can omit any of the extras listed in the poetry install step if they are\nnot used in your deployment. The included arklet/settings.py file does require environ.\nYou can skip installing the development dependencies by passing `--no-dev` to poetry.\nDjango is the only required dependency.\n```\ncd path/to/project\nmkdir postgres-data\ndocker run --name arklet-postgres -v postgres-data:/var/lib/postgresql/data \\\n    -p 5432:5432 \\\n    -e POSTGRES_USER=arklet -e POSTGRES_PASSWORD=arklet \\\n    -d postgres\npoetry install --extras "postgres sentry environ"\npoetry run python manage.py migrate\npoetry run python manage.py createsuperuser\npoetry run python manage.py runserver\n```\n\n### Separate dockers\nUsing docker, we can use a [this provided](./docker/env.docker.local) config file.\n\nSee above for running PostgreSQL, and run the **Arklet** docker as follows (in *bash*):\n```\ndocker build \\\n    --target dev \\\n    -t "arklet" -f ./Dockerfile . \\\n    --build-arg ENV=DEV \\\n&& docker run --rm -it \\\n    -p 8000:8000 \\\n    --env-file=./docker/env.docker.local \\\n    -e ARKLETDEBUG="true" \\\n    --name arklet \\\n    -v `pwd`/ark:/app/ark \\\n    -v `pwd`/ark_import:/app/ark_import \\\n    -v `pwd`/arklet:/app/arklet \\\n    arklet\n```\n\n### With docker-compose\nUsing the provided `docker-compose.yml` with default settings in the [docker\nconfiguration directory](./docker) :\n\n```\ndocker-compose up\n```\n\nBy default, the folders `ark`, `ark_import` and `arklet` are mounted in the\ncontainer. Should you wish to attach a console to the `arklet` container (needed\nto create the django superuser) :\n```\n# In another shell\ndocker exec -it arklet_django /bin/bash\n# You\'re now in the docker container\n./manage.py createsuperuser\n```\n\n### First steps\nCreate your first NAAN, Key, and Shoulder in the admin:\n127.0.0.1:8000/admin\n\nAnd by the way, you now host a working ARK resolver! You can already\ntry the following ones :\n- [http://127.0.0.1:8000/ark:/13960/t5n960f7n](http://127.0.0.1:8000/ark:/13960/t5n960f7n)\n- [http://127.0.0.1:8000/ark:/67375/C0X-SPWFRSGR-N](http://127.0.0.1:8000/ark:/67375/C0X-SPWFRSGR-N)\n- [http://127.0.0.1:8000/ark:/12148/bpt6k65358454](http://127.0.0.1:8000/ark:/12148/bpt6k65358454)\n- ...\n\nHappy minting, binding, and resolving!\n\n## Configuration Options\n\nSee arklet/settings.py for the full list of options to put in your config file.\n\n## Deploying\n### With docker\nUsing the provided Dockerfile (is you wish to set a build target, use `prod`, \nbut being the default target you can skip this), provide the following values\nin your environment:\n\n- ARKLET_DJANGO_SECRET_KEY=[YOUR_SECRET]\n- ARKLET_DEBUG=False\n- ARKLET_HOST=0.0.0.0\n- ARKLET_PORT=[Port of choice]\n- ARKLET_POSTGRES_NAME=[DB NAME]\n- ARKLET_POSTGRES_USER=[DB USER]\n- ARKLET_POSTGRES_PASSWORD=[DB PASS]\n- ARKLET_POSTGRES_HOST=[DB HOST]\n- ARKLET_POSTGRES_PORT=[DB PORT]\n',
    'author': 'Alex Dempsey',
    'author_email': 'avdempsey@archive.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/internetarchive/arklet',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
