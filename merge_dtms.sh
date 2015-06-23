 #!/bin/bash

FILE1=~/Geotiff/ASTGTM2_N39W124_dem.tif
FILE2=~/Geotiff/ASTGTM2_N38W124_dem.tif
FILE3=~/Geotiff/ASTGTM2_N39W123_dem.tif
FILE4=~/Geotiff/ASTGTM2_N38W123_dem.tif

OUTFILENAME=merged_dem_38-39_123-124.tif

# gdal_merge.py is installed in ~/miniconda/bin/gdal_merge.py
gdal_merge.py -o $OUTFILENAME -q -v $FILE1 $FILE2 $FILE3 $FILE4


