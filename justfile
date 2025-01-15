default: run-check-phat-nguoi

alias s := gen-schemas
alias w := web-dev
alias wb := build-web
alias p := precommit-run-all
alias re := restore-dev-env
alias rpe := restore-production-env

restore-production-env:
  [ -d '.venv' ] || uv sync --frozen --no-dev

restore-dev-env:
  [ -d '.venv' ] || (uv sync --frozen --all-groups && uv run pre-commit install)

run-check-phat-nguoi: restore-dev-env
  uv run check-phat-nguoi --frozen

gen-schemas: restore-dev-env
  uv run generate-schemas --frozen

web-dev: restore-dev-env
  rm ./site/ -rf || true
  uv run mkdocs serve

build-web: restore-dev-env
  rm ./site/ -rf || true
  uv run mkdocs build
  rm ./site/schemas/ -rf || true
  mkdir ./site/schemas/ -p
  uv run generate-schemas --frozen
  cp ./schemas/* ./site/schemas
  uv run generate-schema-doc --config-file jsfh-conf.yaml ./site/schemas/ ./site/schemas/

clean: restore-dev-env
  uvx cleanpy@0.5.1 .

precommit-run-all: restore-dev-env
  uvx run pre-commit run -a
