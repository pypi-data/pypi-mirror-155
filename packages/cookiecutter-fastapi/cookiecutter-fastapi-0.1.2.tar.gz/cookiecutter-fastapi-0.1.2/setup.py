# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=2.1.1,<3.0.0',
 'pytest-cookies>=0.6.1,<0.7.0',
 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'cookiecutter-fastapi',
    'version': '0.1.2',
    'description': 'Cookiecutter for fastapi projects',
    'long_description': "# Cookiecutter Fastapi\n\n[![PyPI](https://img.shields.io/pypi/v/cookiecutter-fastapi.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/cookiecutter-fastapi.svg)][status]\n[![Read the documentation at https://cookiecutter-fastapi.readthedocs.io/](https://img.shields.io/readthedocs/cookiecutter-fastapi/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![python](https://img.shields.io/pypi/pyversions/cookiecutter-fastapi)](https://github.com/Tobi-De/cookiecutter-fastapi)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/cookiecutter-fastapi/blob/master/LICENSE)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[read the docs]: https://cookiecutter-fastapi.readthedocs.io/\n[pypi_]: https://pypi.org/project/fastapi-paginator/\n[status]: https://pypi.org/project/fastapi-paginator/\n\nA [Cookiecutter](https://github.com/audreyr/cookiecutter) template for [fastapi](https://fastapi.tiangolo.com) projects, inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django).\n\n✨📚✨ [Read the full documentation][read the docs]\n\n## Features\n\n<!-- features-begin -->\n\n- [x] [fastapi-users](https://github.com/fastapi-users/fastapi-users) for users authentication and management\n- [x] [Pydantic](https://pydantic-docs.helpmanual.io/) for settings management\n- [x] Include a cli tool built with [typer](https://github.com/tiangolo/typer) to simplify project management\n- [x] [Pre-commit](https://pre-commit.com/) integration included by default\n- [x] [Tortoise-orm](https://tortoise.github.io/) and [aerich](https://github.com/tortoise/aerich) database setup by default but switchable\n- [x] Limit-offset pagination helpers included\n- [x] Run tests with unittest or [pytest](https://docs.pytest.org/en/7.1.x/)\n- [x] Sending emails using [aiosmtplib](https://aiosmtplib.readthedocs.io/en/stable/client.html) or [Amazon SES](https://aws.amazon.com/fr/ses/)\n- [x] Optional integration with [sentry](https://docs.sentry.io/platforms/python/) for error logging\n- [ ] [Docker](https://www.docker.com/) and [docker-compose](https://github.com/docker/compose) for production using [Traefik](https://github.com/traefik/traefik)\n- [x] Optional setup of HTML templates rendering using [jinja2](https://jinja.palletsprojects.com/en/3.1.x/)\n- [ ] Optional static files serving using [whitenoise](http://whitenoise.evans.io/en/stable/)\n- [x] [Procfile](https://devcenter.heroku.com/articles/procfile) for deploying to heroku\n- [ ] Optional integration with [fastapi-storages](https://github.com/Tobi-De/fastapi-storages) for media files storage\n- [x] Implement the [Health Check API patterns](https://microservices.io/patterns/observability/health-check-api.html) on your fastapi application\n- [ ] Renders fastapi projects with 100% starting test coverage\n\n### Task queues manager options\n\n - [x] [Arq](https://github.com/samuelcolvin/arq)\n - [ ] [Procrastinate](https://github.com/procrastinate-org/procrastinate)\n - [ ] [Celery](https://github.com/celery/celery)\n\n### ORM/ODM options\n\n- [x] [Tortoise ORM](https://tortoise.github.io/)\n- [x] [Beanie](https://github.com/roman-right/beanie)\n- [ ] [RedisOM](https://github.com/redis/redis-om-python)\n- [ ] [SQLModel](https://github.com/tiangolo/sqlmodel)\n\n<!-- features-end -->\n\n## Usage\n\nInstall the cookiecutter package:\n\n```shell\npip install cookiecutter black isort\n```\n\n**Note**: `Black` and `isort` are used to format your project right after it has been generated.\n\nNow run it against this repo:\n\n```shell\ncookiecutter https://github.com/Tobi-De/cookiecutter-fastapi\n```\n\nYou'll be prompted for some values. Provide them, then a fastapi project will be created for you.\n\n## Contributing\n\nContributions are very welcome. To learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Cookiecutter Fastapi_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n[file an issue]: https://github.com/tobi-de/cookiecutter-fastapi/issues\n\n<!-- github-only -->\n\n[license]: https://github.com/tobi-de/cookiecutter-fastapi/blob/main/LICENSE\n[contributor guide]: https://github.com/tobi-de/cookiecutter-fastapi/blob/main/CONTRIBUTING.md\n",
    'author': 'Tobi-De',
    'author_email': 'tobidegnon@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tobi-De/cookiecutter-fastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
