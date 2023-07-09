#!/bin/bash
set -ex

# Build the C executable
./build_ona.sh

# Build the Python package
hatch -v build
