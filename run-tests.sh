#!/bin/bash
# Script to run tests in Docker

set -e

echo "Running tests in Docker..."

docker compose run --rm test pytest "${@:-tests/}"


