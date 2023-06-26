#!/bin/bash

# Build the C executable
cd ona
./build.sh
cd ..

# Build the Python package
python3 -m build
