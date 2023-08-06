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
```

### Run fetcher pipelines

```bash
# Replace PROVIDER_SLUG by the real value:
dbnomics-fetchers -v run --provider-slug PROVIDER_SLUG

# To run a pipeline for each fetcher:
dbnomics-fetchers -v list --slug | xargs -I {} dbnomics-fetchers -v run --provider-slug {}
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
