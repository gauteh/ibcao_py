#! /bin/bash

dname=$(dirname ${0})

pushd $dirname

python -m unittest discover -s $dname $@

popd

