#! /bin/bash

FILE=download.list

python tv.py

if [[ -s $FILE ]] ; then
    #echo "$FILE has data."
    python torrent9.py
fi ;

./clean.sh
