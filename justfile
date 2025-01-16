default: run-check-phat-nguoi

alias s := gen-schemas
alias w := web-dev
alias wb := build-web
alias p := precommit-run-all
alias re := restore-dev-env
alias rpe := restore-production-env

restore-production-env:
  [ -d '.venv' ] || uv sync --no-dev --frozen

restore-dev-env:
  [ -d '.venv' ] || (uv sync --all-groups --frozen && uv run pre-commit install)

run-check-phat-nguoi: restore-dev-env
  uv run --no-dev --frozen cpn-cli

gen-schemas: restore-dev-env
  uv run --no-dev --frozen cpn-generate-schemas

web-dev: restore-dev-env
  rm ./site/ -rf || true
  uv run --group build-website --frozen mkdocs serve

build-web: restore-dev-env
  rm ./site/ -rf || true
  uv run --group build-website --frozen mkdocs build
  rm ./site/schemas/ -rf || true
  mkdir ./site/schemas/ -p
  uv run --group build-website --frozen generate-schemas
  cp ./schemas/* ./site/schemas
  uv run --group build-website --frozen generate-schema-doc --config-file jsfh-conf.yaml ./site/schemas/ ./site/schemas/

clean: restore-dev-env
  uvx cleanpy@0.5.1 .

precommit-run-all: restore-dev-env
  uv run --frozen --only-dev pre-commit run -a
