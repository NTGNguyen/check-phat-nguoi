```sh
uv sync # no need uv venv

.venv/Scripts/activate # or "source .venv/bin/active" on Linux

# uv can detect env with "uv run", not need active venv
pre-commit install

check-phat-nguoi
generate-schemas
generate-config-schema
```

> [!NOTE]
>
> if no activating venv, you must prepend `uv run` before commands

# Test on production with python 3.10

```sh
uv python install 3.10
uv venv .venv-3.10 -p 3.10
.venv/Scripts/activate # or "source .venv/bin/active" on Linux
pip install -e . -r ./requirements.txt
check-phat-nguoi
```

> [!NOTE]
>
> Can export var env `VIRTUAL_ENV=.venv-3.10`
