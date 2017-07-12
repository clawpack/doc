#!/bin/bash

VERSIONS="_build/html/master `ls -d _build/html/v5*`"

for dir in $VERSIONS
do
    echo copying _build/html/galleries.html to $dir/galleries.html
    cp _build/html/galleries.html $dir/galleries.html
done
