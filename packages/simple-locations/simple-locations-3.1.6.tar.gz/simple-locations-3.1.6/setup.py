# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_locations',
 'simple_locations.management',
 'simple_locations.management.commands',
 'simple_locations.migrations']

package_data = \
{'': ['*'],
 'simple_locations': ['fixtures/*',
                      'locale/fr/LC_MESSAGES/*',
                      'static/css/*',
                      'static/images/*',
                      'static/javascripts/*',
                      'static/uni_form/*',
                      'templates/simple_locations/*',
                      'templates/simple_locations/admin/*']}

install_requires = \
['django-geojson>=3.2.1,<4.0.0', 'django-mptt>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'simple-locations',
    'version': '3.1.6',
    'description': "The common location package for Catalpa's projects",
    'long_description': '# simple_locations\n\nThe common location package used for catalpa\'s projects. A hierarchical tree of geographical locations supporting location type and GIS data.\n\n## Admin\n\nThe admin site is set up to use Modeltranslations (if available in the parent app)\n\nFor modeltranslations, please remember to run `sync_translation_fields` in order to get `name_en`, `name_tet` etc. fields.\n\n## Environment\n\nThis is intended to be compatible with:\n\n- Django 3.1, 3.2, 4.0\n- Python 3.7, 3.8, 3.9\n\n```sh\ngh repo clone catalpainternational/simple_locations\ncd simple_locations\npython -m venv env\n. env/bin/activate\npip install pip-tools\npip-sync requirements.txt dev.txt\npre-commit install\n```\n\n### Pre Commit\n\nIf `pre-commit` is installed your code will be checked before commit.\nThis includes\n\n- black\n- flake8\n- isort\n- mypy\n\nThe same checks are run on push. See `pytest.yaml` for details on the checks being run.\n\n### New Release\n\nFor a new release, change the `version` property in pyproject.toml and push a git tag with the version number\nFor instance at time of writing the version is `3.1.4` with the tag `v3.1.4`\n\nSee `build.yaml` for details on release tagging\n## Changelog\n\n- Version 3.1.4\n  - Migrating JSON views from openly\n\n- Version 3.1.3\n  - Added `intersects_area` function\n\n- Version 3.1.2\n  - Uses psycopg2-binary for development environment\n\n- Version 3.1.1\n  - Added "border" fields\n  - Added a model for "projected" areas in EPSG:3857\n  - Added commands for border generation and\n  - `./manage.py` and associated project code\n\n- Version 3.0.1\n\n  - Poetry for dependency + packaging\n  - Releases are automated by pushing a `vx.x.x` tag to github\n\n- Version 3.0 (not on pypi)\n\n  - Code style changes (black, flake8)\n\n- Version 2.77\n\n  - first pass of updates for Python 3.8+ and Django 3.1+\n\n- Version 2.75\n\n  - add modeltranslations\n\n- Version 2.74\n\n  - fix CORS issue breaking maps in AreaAdmin\n  - typo in AreaChildrenInline\n\n- Version 2.73\n\n  - add an inline showing children to the Area admin\n  - make the `geom` field optional\n\n- Version 2.72\n  - optionally use django_extensions\' ForeignKeyAutocompleteAdmin in admin interface\n\n\n## Manually Uploading a new version to PyPi\n\nBump `pyproject.toml`\nThen run `poetry build` and `poetry publish`\n\n```bash\npoetry build\npoetry publish\n```\n\nSee the file `build.yml` for the workflow\n',
    'author': 'Joshua Brooks',
    'author_email': 'josh@catalpa.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/catalpainternational/simple_locations',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
