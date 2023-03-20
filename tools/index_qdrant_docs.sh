#!/usr/bin/env bash

set -e

PROJECT_ROOT="$(pwd)/$(dirname "$0")/../"

cd $(mktemp -d)

git clone https://github.com/qdrant/docs.git
cd docs

LATEST_VERSION=$(ls -1 qdrant/ | sort -V | tail -n 1)

DOCS_DIR="$(pwd)/qdrant/${LATEST_VERSION}/"

cd ${PROJECT_ROOT}

python -m markdown_search.index --docs-dir ${DOCS_DIR} --url-prefix 'https://qdrant.tech/documentation/'

