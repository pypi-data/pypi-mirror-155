# DBnomics fetcher ops

Manage DBnomics fetchers.

## Usage

### Install

```bash
pip install dbnomics-fetcher-ops
```

### Configure a fetcher

Configure:

- GitLab private token: use `--gitlab-private-token` option or `GITLAB_PRIVATE_TOKEN` environment variable. The private token can be a [personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html). It must have the `api` scope.

Run:

```bash
dbnomics-fetchers -v configure scsmich --dry-run
# If everything seems OK, remove the --dry-run flag:
dbnomics-fetchers -v configure scsmich
```

### List fetchers

```bash
dbnomics-fetchers -v list
dbnomics-fetchers -v list --slug --no-legacy-pipeline
```

## Development

This repository uses [Poetry](https://python-poetry.org/).

```bash
# git clone repo or fork
cd dbnomics-fetcher-ops
poetry install
cp .env.example .env
```

Run commands with:

```bash
poetry run dbnomics-fetchers COMMAND
```

To use ipdb:

```bash
poetry shell
# Find venv dir with "which python"
ipdb3 /path/to/venv/bin/dbnomics-fetchers ...
```
