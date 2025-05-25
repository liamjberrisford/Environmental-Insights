#!/usr/bin/env bash
set -e

# 1) Make your code importable
export PYTHONPATH="$PWD"

# 2) Base output directory
BASE_OUT="book/docs/api"

# 3) Ensure all of the output dirs exist
mkdir -p \
  "$BASE_OUT/environmental_insights"

# 4) A helper function to render one file
render() {
  local file=$1
  local subdir=$2    # e.g. "environmental_insights" or "tests/integration"
  # skip __init__.py
  if [[ "$(basename "$file")" == "__init__.py" ]]; then
    return
  fi
  # build module name: replace "/" with ".", strip .py
  local mod="${file%.py}"
  mod="${mod//\//.}"
  # basename for output filename
  local name="$(basename "$mod")"
  # render
  poetry run pydoc-markdown -I . -m "$mod" \
    > "$BASE_OUT/$subdir/${name}.md"
  echo "☑  $BASE_OUT/$subdir/${name}.md"
}

# 5) Loop through each group

# environmental_insights/
for f in environmental_insights/*.py; do
  render "$f" "environmental_insights"
done

# tests/integration/
for f in tests/integration/*.py; do
  render "$f" "tests/integration"
done

# tests/unit/
for f in tests/unit/*.py; do
  render "$f" "tests/unit"
done
