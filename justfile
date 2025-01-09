default: run-check-phat-nguoi

alias s := gen-schemas
alias w := web-dev
alias wb := build-web
alias p := precommit-run-all

restore-dependencies:
  [ -d '.venv' ] || uv sync --frozen --all-groups

run-check-phat-nguoi: restore-dependencies
  uv run check-phat-nguoi --frozen

gen-schemas: restore-dependencies
  uv run generate-schemas --frozen

gen-config-schema: restore-dependencies
  uv run gen-config-schema --frozen

web-dev: restore-dependencies
  rm ./site/ -rf
  uv run mkdocs serve

build-web-mkdocs: restore-dependencies
  rm ./site/ -rf
  uv run mkdocs build

build-web-schemas: restore-dependencies gen-schemas
  rm ./site/schemas/ -rf
  mkdir ./site/schemas/ -p
  uv run generate-schema-doc --config-file jsfh-conf.yaml ./schemas/ ./site/schemas/

build-web: restore-dependencies build-web-mkdocs build-web-schemas

clean: restore-dependencies
  uvx cleanpy@0.5.1 .

precommit-run-all: restore-dependencies
  uvx run pre-commit run -a
