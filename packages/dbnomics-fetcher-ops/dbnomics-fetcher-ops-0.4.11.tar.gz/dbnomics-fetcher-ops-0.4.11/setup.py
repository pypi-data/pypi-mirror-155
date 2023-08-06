# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbnomics_fetcher_ops',
 'dbnomics_fetcher_ops.commands',
 'dbnomics_fetcher_ops.services']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=21.0.0,<22.0.0',
 'daiquiri>=3.0.1,<4.0.0',
 'dbnomics-solr>=1.1.2,<2.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-gitlab>=2.4.0,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'typer>=0.4.1,<0.5.0',
 'validators>=0.20.0,<0.21.0',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['dbnomics-fetchers = dbnomics_fetcher_ops.cli:main']}

setup_kwargs = {
    'name': 'dbnomics-fetcher-ops',
    'version': '0.4.11',
    'description': 'Manage DBnomics fetchers',
    'long_description': '# DBnomics fetcher ops\n\nManage DBnomics fetchers.\n\n## Usage\n\n### Install\n\n```bash\npip install dbnomics-fetcher-ops\n```\n\n### Configure a fetcher\n\nConfigure:\n\n- GitLab private token: use `--gitlab-private-token` option or `GITLAB_PRIVATE_TOKEN` environment variable. The private token can be a [personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html). It must have the `api` scope.\n\nRun:\n\n```bash\ndbnomics-fetchers -v configure scsmich --dry-run\n# If everything seems OK, remove the --dry-run flag:\ndbnomics-fetchers -v configure scsmich\n```\n\n### List fetchers\n\n```bash\ndbnomics-fetchers -v list\n```\n\n### Run fetcher pipelines\n\n```bash\n# Replace PROVIDER_SLUG by the real value:\ndbnomics-fetchers -v run --provider-slug PROVIDER_SLUG\n\n# To run a pipeline for each fetcher:\ndbnomics-fetchers -v list --slug | xargs -I {} dbnomics-fetchers -v run --provider-slug {}\n```\n\n## Development\n\nThis repository uses [Poetry](https://python-poetry.org/).\n\n```bash\n# git clone repo or fork\ncd dbnomics-fetcher-ops\npoetry install\ncp .env.example .env\n```\n\nRun commands with:\n\n```bash\npoetry run dbnomics-fetchers COMMAND\n```\n\nTo use ipdb:\n\n```bash\npoetry shell\n# Find venv dir with "which python"\nipdb3 /path/to/venv/bin/dbnomics-fetchers ...\n```\n',
    'author': 'Christophe Benz',
    'author_email': 'christophe.benz@nomics.world',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
