#
# Examples of gdal methods taken
# from http://www.gdal.org/gdal_tutorial.html
#

import gdal
from gdalconst import *
import struct

# Opening a File
#------------------------
filename='ASTGTM2_N37W123_dem.tif'
dataset = gdal.Open( filename, GA_ReadOnly )

# Getting Dataset Information
#------------------------------------------
print ''

print 'Driver: ', dataset.GetDriver().ShortName,'/', dataset.GetDriver().LongName

print 'Size is ',dataset.RasterXSize,'x',dataset.RasterYSize, 'x',dataset.RasterCount

print 'Projection is ',dataset.GetProjection()

geotransform = dataset.GetGeoTransform()

if not geotransform is None:
	print 'Origin = (',geotransform[0], ',',geotransform[3],')'
	print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'
	print ''

# Note:
# GeoTransform[0] /* top left x */
# GeoTransform[1] /* w-e pixel resolution */
# GeoTransform[2] /* 0 */
# GeoTransform[3] /* top left y */
# GeoTransform[4] /* 0 */
# GeoTransform[5] /* n-s pixel resolution (negative value) */

# Fetching a Raster Band
#---------------------------------------
# band = dataset.GetRasterBand(1)

# print 'Band Type=',gdal.GetDataTypeName(band.DataType)

# min = band.GetMinimum()
# max = band.GetMaximum()
# if min is None or max is None:
# 	(min,max) = band.ComputeRasterMinMax(1)

# print 'Min=%.3f, Max=%.3f' % (min,max)

# if band.GetOverviewCount() > 0:
# 	print 'Band has ', band.GetOverviewCount(), ' overviews.'

# if not band.GetRasterColorTable() is None:
# 	print 'Band has a color table with ', \
# 	band.GetRasterColorTable().GetCount(), ' entries.'

# Reading Raster
#------------------------
# scanline = band.ReadRaster( 0, 0, band.XSize, 1, band.XSize, 1, GDT_Float32 )
# tuple_of_floats = struct.unpack('f' * band.XSize, scanline)

# print len(tuple_of_floats)

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

