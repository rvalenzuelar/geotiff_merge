#
# Extends a geotiff DTM file with flat terrain (e.g. ocean)
# (inspired in http://www.gdal.org/gdal_tutorial.html)
#
# Raul Valenzuela
# April, 2015
#


import gdal
from gdalconst import *
import subprocess
import numpy as np
import sys

def Usage():
	print 'Usage:\n' 
	print '$ python extend_geotiff2.py [-d direction] [-l length] [-f input_file]\n'
	print 'direction:'
	print '\tW:  west'
	print '\tS :  south'
	print '\tSW :  south-west'
	print 'length:'
	print '\tlength in degrees for extension'
	print 'input_file:'
	print '\tname of geotiff file to extend\n'

def main():

	# Handle Input Options
	#------------------------------------
	extend_direction=''
	extend_len=''
	filename=''

	i=1
	if len(sys.argv)==1:
		Usage()
		sys.exit()
	else:
		while i < len(sys.argv):
			arg=sys.argv[i]
			if arg=='-d':
				i=i+1
				extend_direction=sys.argv[i]
			elif arg=='-l':
				i=i+1
				extend_len=float(sys.argv[i]) # degrees
			elif arg=='-f':
				i=i+1
				filename=sys.argv[i]
			else:
				Usage()
			i=i+1

	if extend_direction=='' or extend_len=='' or filename=='':
		print 'Some input arguments are missing'
		Usage()
		sys.exit()

	# Opening File
	#------------------------
	dataset = gdal.Open( filename, GA_ReadOnly )

	# Getting Dataset Information
	#------------------------------------------
	inputDriver= dataset.GetDriver().LongName
	xsize=dataset.RasterXSize
	ysize=dataset.RasterYSize
	nbands=dataset.RasterCount
	inputProjection=dataset.GetProjection()

	# Get corners and resolution
	#------------------------------------------
	geotransform = dataset.GetGeoTransform()
	lon_topL = geotransform[0]
	lon_resolution = geotransform[1]
	# geotransform[2] = rotation
	lat_topL = geotransform[3] 
	# geotransform[4] = rotation
	lat_resolution = geotransform[5] # (negative value)

	corner_topL=np.array([lat_topL , lon_topL])
	corner_topR=np.array([lat_topL , lon_topL+lon_resolution*xsize])
	corner_lowL=np.array([lat_topL+lat_resolution*ysize , lon_topL])
	corner_lowR=np.array([lat_topL+lat_resolution*ysize , lon_topL+lon_resolution*xsize])

	# Creates flat array
	#-------------------------------
	if extend_direction=='W':
		print '\n Extending to West in %2.1f degrees\n' % extend_len
		x_ncells=int(extend_len/lon_resolution)
		y_ncells=ysize
		ext_lon_topL = lon_topL - extend_len
		ext_lat_topL = lat_topL
	elif extend_direction=='S':
		print '\n Extending to South in %2.1f degrees\n' % extend_len
		x_ncells=xsize
		y_ncells=int(extend_len/-lat_resolution)
		ext_lon_topL = corner_lowL[1]
		ext_lat_topL = corner_lowL[0]	
	elif extend_direction=='SW':	
		print '\n Extending to South and West in %2.1f degrees\n' % extend_len
		x_ncells=xsize+int(extend_len/lon_resolution)
		y_ncells=ysize+int(extend_len/-lat_resolution)
		ext_lon_topL = lon_topL - extend_len
		ext_lat_topL = lat_topL
	else:
		print '\n Argument is W, S, or SW'

	flat=np.zeros((y_ncells , x_ncells), dtype=np.int16)
	ext_lon_resolution = lon_resolution
	ext_lat_resolution = lat_resolution 

	# Saves flat array to a geotiff file
	#------------------------------------------------
	format = "GTiff"
	dst_filename='extension.tif'
	driver = gdal.GetDriverByName( format )
	nbands=1

	dst_ds = driver.Create( 	dst_filename, 
								x_ncells, 
								y_ncells, 
								nbands, 
								gdal.GDT_Int16 )

	dst_ds.SetGeoTransform( [ 	ext_lon_topL, 
									ext_lon_resolution, 
									0, 
									ext_lat_topL, 
									0, 
									ext_lat_resolution ] )

	dst_ds.SetProjection( inputProjection)
	dst_ds.GetRasterBand(1).WriteArray( flat )
	dst_ds.FlushCache()  # Write to disk.

	# Merge flat geotiff with DTM geotiff
	#-----------------------------------------------------
	extended_filename=filename[:-4]+'_extended.tif'

	subprocess.call(["gdal_merge.py","-o",extended_filename,"-q","-v","extension.tif",filename])
	subprocess.call(["rm",dst_filename])

	print '\nExtended DTM file saved as '+extended_filename+'\n'

# Call main function
if __name__ == '__main__':
	main()