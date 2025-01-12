# Setup

Requirements:

- [uv](https://github.com/astral-sh/uv)
- [just](https://github.com/casey/just)

## Run check-phat-nguoi

```sh
just
```

## Export schemas

```sh
just s
```

## Dev web

```sh
just w
```

## Build web

```sh
just wb
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
