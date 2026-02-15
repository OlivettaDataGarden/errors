import "/Users/maartenderuyter/Documents/dg-development/dg_justfile/Justfile"

# Local vars:
IS_PACKAGE := "true"
COMMIT_PREFIX := "DGEM"
REPO_NAME := "errors"


tox:
    uv run tox
