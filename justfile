default: run-check-phat-nguoi

alias s := gen-schemas
alias w := web-dev
alias wb := build-web
alias p := precommit-run-all

restore-env:
  [ -d '.venv' ] || (uv sync --frozen --all-groups && uv run pre-commit install)

run-check-phat-nguoi: restore-env
  uv run check-phat-nguoi --frozen

gen-schemas: restore-env
  uv run generate-schemas --frozen

gen-config-schema: restore-env
  uv run gen-config-schema --frozen

web-dev: restore-env
  rm ./site/ -rf || true
  uv run mkdocs serve

build-web-mkdocs: restore-env
  rm ./site/ -rf || true
  uv run mkdocs build

build-web-schemas: restore-env
  rm ./site/schemas/ -rf || true
  mkdir ./site/schemas/ -p
  just gen-schemas
  uv run generate-schema-doc --config-file jsfh-conf.yaml ./schemas/ ./site/schemas/

build-web: restore-env
  just build-web-mkdocs
  just build-web-schemas

clean: restore-env
  uvx cleanpy@0.5.1 .

precommit-run-all: restore-env
  uvx run pre-commit run -a
