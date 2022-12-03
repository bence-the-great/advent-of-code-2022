#!/bin/bash

directory_name="day${1}"

if [ -d "${directory_name}" ]; then
    echo "${directory_name} exists."
    exit 1
else
    mkdir "${directory_name}"
    cp ./skeleton/solve.py "${directory_name}/"
    cp ./skeleton/inputs.py "${directory_name}/"
fi
