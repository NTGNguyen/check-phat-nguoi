# Welcome to CheckPhatNguoi

## Usage

1. Install Requirements

```sh
python -m venv .venv
.venv/Scripts/activate # or "source .venv/bin/active" on Linux
pip install -e -r requirements.txt
```

2. Dev

```sh
uv sync # no need uv venv

.venv/Scripts/activate # or "source .venv/bin/active" on Linux

# uv can detect env with "uv run", not need active venv
uv run pre-commit install

uv run check-phat-nguoi
uv run generate-schemas
uv run generate-config-schema
```

Test on production with python 3.10

```
uv python install 3.10
uv venv .venv-3.10 -p 3.10
uv pip install -e . -r ./requirements.txt
uv run check-phat-nguoi
```

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
