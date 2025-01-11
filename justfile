default: run-check-phat-nguoi

alias s := gen-schemas
alias w := web-dev
alias wb := build-web
alias p := precommit-run-all

restore-env:
  [ -d '.venv' ] || uv sync --frozen --all-groups && uv run pre-commit install

run-check-phat-nguoi: restore-env
  uv run check-phat-nguoi --frozen

gen-schemas: restore-env
  uv run generate-schemas --frozen

gen-config-schema: restore-env
  uv run gen-config-schema --frozen

web-dev: restore-env
  rm ./site/ -rf
  uv run mkdocs serve

build-web-mkdocs: restore-env
  rm ./site/ -rf
  uv run mkdocs build

build-web-schemas: restore-env gen-schemas
  rm ./site/schemas/ -rf
  mkdir ./site/schemas/ -p
  uv run generate-schema-doc --config-file jsfh-conf.yaml ./schemas/ ./site/schemas/

build-web: restore-env
  just build-web-mkdocs
  just build-web-schemas

clean: restore-env
  uvx cleanpy@0.5.1 .

precommit-run-all: restore-env
  uvx run pre-commit run -a
