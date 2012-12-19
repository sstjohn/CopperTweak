#!/bin/sh

for f in `find . -name '*.pyc'`; do
	rm $f
done

tmpfile=`tempfile`.tar

tarball=`basename $PWD`.tar.gz

tar cf $tmpfile .
gzip $tmpfile
mv $tmpfile.gz ../$tarball
