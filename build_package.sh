#!/bin/bash
set -ex

# Build the C executable
cd ona
./build.sh
cd ..

# Build the Python package
hatch build
