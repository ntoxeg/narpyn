#!/bin/bash
set -ex

# Build the C executable
cd ona
./build.sh
cd ..

# Copy the executable to the package
cp ona/NAR narpyn/ona/NAR/NARexe
