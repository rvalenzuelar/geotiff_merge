#
# Examples of gdal methods taken
# from http://www.gdal.org/gdal_tutorial.html
#

import gdal
from gdalconst import *
import struct
import numpy as np

# Opening a File
#------------------------
filename='ASTGTM2_N37W123_dem.tif'
dataset = gdal.Open( filename, GA_ReadOnly )

# Getting Dataset Information
#------------------------------------------

inputDriver= dataset.GetDriver().LongName
xsize=dataset.RasterXSize
ysize=dataset.RasterYSize
nbands=dataset.RasterCount
inputProjection=dataset.GetProjection()
geotransform = dataset.GetGeoTransform()

# for i in range(6):
# 	print geotransform[i]
# print ''
# Note:
# geotransform[0] = top left longitude
# geotransform[1] = longitude resolution
# geotransform[2] = rotation
# geotransform[3] = top left latitude
# geotransform[4] = rotation
# geotransform[5] = latitude resolution (negative value)

corner_topL=np.array([geotransform[3],geotransform[0]])
corner_topR=np.array([geotransform[3],geotransform[0]+geotransform[1]*xsize])
corner_lowL=np.array([geotransform[3]+geotransform[5]*ysize,geotransform[0]])
corner_lowR=np.array([geotransform[3]+geotransform[5]*ysize,geotransform[0]+geotransform[1]*xsize])

# print corner_topL
# print corner_topR
# print corner_lowL
# print corner_lowR


# Fetching a Raster Band
#---------------------------------------
band = dataset.GetRasterBand(1)

bandType=gdal.GetDataTypeName(band.DataType)
# print 'Band Type=',bandType

bandMin = band.GetMinimum()
bandMax = band.GetMaximum()

# Reading Raster
#------------------------
r_xoff=0
r_yoff=0
r_xsize=xsize
r_ysize=1
r_buf_xsize=xsize
r_buf_ysize=1

# myraster=np.array([])
for i in range(xsize):
	scanline = band.ReadRaster( r_xoff, r_yoff, r_xsize, r_ysize, r_buf_xsize, r_buf_ysize, GDT_Int16 )
	gline = np.asarray(struct.unpack('H' * band.XSize, scanline))
	if i==0:
		myraster=gline
	else:
		myraster=np.vstack((myraster,gline))
print myraster

# TAKES VERY LONG !!!

# print gline
# print len(scanline)

# Determine method supported for creating file
#----------------------------------------------------------------
# format = "GTiff"
# driver = gdal.GetDriverByName( format )
# metadata = driver.GetMetadata()
# if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == 'YES':
# 	print 'Driver %s supports Create() method.' % format
# if metadata.has_key(gdal.DCAP_CREATECOPY) and metadata[gdal.DCAP_CREATECOPY] == 'YES':
# 	print 'Driver %s supports CreateCopy() method.' % format
# print ''

