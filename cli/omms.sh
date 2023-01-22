#!/bin/bash

cd ..
pp=$(pwd)
export PYTHONPATH=$pp
cd cli || exit 1
echo "PWD: $(pwd)"
./omms

