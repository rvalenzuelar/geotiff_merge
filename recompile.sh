#!/bin/bash

# Bash script to compile the navigation correction code
#
# Raul Valenzuela

rm aster2txt 

# for home
# CLIB="-L/usr/lib -lgeotiff -ltiff -L/usr/local/lib"

# for work
CLIB="-lgeotiff -ltiff"

CINC="-I/usr/include/geotiff"

gcc -o aster2txt aster2txt.c $CLIB $CINC

