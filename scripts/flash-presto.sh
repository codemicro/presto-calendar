#!/usr/bin/env bash

set -xeu

uvx mpremote fs rm -rf ':/' || true
uvx mpremote fs cp -r src/presto/* :/
uvx mpremote reset