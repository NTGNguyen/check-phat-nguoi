# Setup

## Run check-phat-nguoi

```sh
just
```

## Export schemas

```sh
just s
```

## Build web

```sh
just w
```

# Test on production with python 3.10

```sh
uv python install 3.10
uv venv .venv-3.10 -p 3.10
.venv/Scripts/activate # or "source .venv/bin/active" on Linux
pip install -e . -r ./requirements.txt
check-phat-nguoi
```

???+note
Can export var env `VIRTUAL_ENV=.venv-3.10`
