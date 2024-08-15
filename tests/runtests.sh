#! /bin/bash

dname=$(dirname ${0})

echo $dname
echo $@

pushd $dname

python -m unittest -c -v $@

r=$?

popd

exit $r

