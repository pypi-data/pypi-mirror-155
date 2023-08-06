# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyramid_heroku', 'pyramid_heroku.tests']

package_data = \
{'': ['*']}

install_requires = \
['expandvars', 'pyramid>=1.7', 'requests']

setup_kwargs = {
    'name': 'pyramid-heroku',
    'version': '0.9.1',
    'description': 'A bunch of helpers for successfully running Pyramid on Heroku.',
    'long_description': 'pyramid_heroku\n==============\n\nIntroduction\n------------\n\npyramid_heroku is a collection of tweens and helpers to successfully run `Pyramid <http://www.trypyramid.com/>`_ on `Heroku <https://heroku.com/>`_\n\nIt provides the following:\n\n* ``ClientAddr`` tween that sets real user\'s IP to ``request.client_addr``\n* ``Host`` tween that sets `request.host` to proxied `X-Forwarded-Host` header (note: potential security risk)\n* ``HerokuappAccess`` tween that denies access to your app\'s\n  ``<app>.herokuapp.com`` domain for any non-whitelisted IPs.\n* ``migrate.py`` script for automatically running alembic migrations on\n  deploy.\n* ``maintenance.py`` script for controlling Heroku maintenance mode.\n\n\nInstallation\n------------\n\nJust do\n\n``pip install pyramid_heroku``\n\nor\n\n``easy_install pyramid_heroku``\n\n\nCompatibility\n-------------\n\npyramid_heroku runs with pyramid>=1.7 and python>=3.6.\nOther versions might also work.\n\n\nDocumentation\n-------------\n\nUsage example for tweens::\n\n    def main(global_config, **settings):$ cat .heroku/release.sh\n        config = Configurator(settings=settings)\n        config.include(\'pyramid_heroku.client_addr\')\n        config.include(\'pyramid_heroku.herokuapp_access\')\n        return config.make_wsgi_app()\n\nThe ``pyramid_heroku.herokuapp_access`` tween depends on\n``pyramid_heroku.client_addr`` tween and it requires you to list whitelisted IPs\nin the ``pyramid_heroku.herokuapp_whitelist`` setting.\n\nThe ``pyramid_heroku.client_addr`` tween sets request.client_addr to an IP we\ncan trust. It handles IP spoofing via ``X-Forwarded-For`` headers and\nignores Cloudflare\'s IPs when using Cloudflare reverse proxy.\n\n\nUsage example for automatic alembic migration script::\n\n    $ cat .heroku/release.sh\n    #!/usr/bin/env bash\n\n    set -e\n\n    echo "Running migrations"\n    python -m pyramid_heroku.migrate my_app etc/production.ini\n\n    echo "DONE!"\n\nFor migration script to work, you need to set the ``MIGRATE_API_SECRET_HEROKU``\nenv var in Heroku. This allows the migration script to use the Heroku API.\n\n\nBefore running DB migration, the script will enable `Heroku maintenance mode <https://devcenter.heroku.com/articles/maintenance-mode>`_\nif the app is not already in maintenance mode. After the migration, maintenance mode will\nbe disabled only if it was enabled by the migration script.\n\nMaintenance mode can also be enabled/disabled using the ``pyramid_heroku.maintenance`` script.\n\nUsage example for enabling the Heroku maintenance mode::\n\n    python -m pyramid_heroku.maintenance on my_app etc/production.ini\n\n\nIf you use structlog, add the following configuration setting to your INI file to enable structlog-like logging::\n\n    pyramid_heroku.structlog = true\n\n\nSee tests for more examples.\n\n\n\nReleasing\n---------\n\n#. Update CHANGES.rst.\n#. Update pyproject.toml version.\n#. Run ``poetry check``.\n#. Run ``poetry publish --build``.\n\n\nWe\'re hiring!\n-------------\n\nAt Niteo we regularly contribute back to the Open Source community. If you do too, we\'d like to invite you to `join our team\n<https://niteo.co/careers/>`_!\n',
    'author': 'Niteo',
    'author_email': 'info@niteo.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/teamniteo/pyramid_heroku',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
