restore:
  uv sync --frozen --all-groups

run:
  uv run check-phat-nguoi --frozen

gen-schemas:
  just gen-config-schema

gen-config-schema:
  uv run gen-config-schema --frozen

web-mkdocs:
  rm ./site/ -rf
  uv run mkdocs build

web-schemas:
  rm ./schemas_site/ -rf
  mkdir ./schemas_site
  uv run generate-schema-doc ./schemas/ ./schemas_site/

web:
  just web-mkdocs
  just web-schemas
  mkdir ./site/schemas/
  mv ./schemas_site/* ./site/schemas/
  rm ./schemas_site/ -r
