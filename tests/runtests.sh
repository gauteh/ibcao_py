#! /bin/bash

dname=$(dirname ${0})

python -m unittest discover -s $dname -v $@

