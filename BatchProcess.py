# Auto batch process for Agisoft Photoscan
# @ H.GONG 2017/02/22

import PhotoScan
import os,re,sys

# get the photo (.JPG) list in specified folder
def getPhotoList(root_path, photoList):
	pattern = '.JPG$'
	for root, dirs, files in os.walk(root_path):
		for name in files:
			if re.search(pattern,name):
				cur_path = os.path.join(root, name)
				#print (cur_path)
				photoList.append(cur_path)
			
def photoscanProcess(root_path):				
	#PhotoScan.app.messageBox('hello world! \n')
	PhotoScan.app.console.clear()

	## construct the document class
	doc = PhotoScan.app.document

	## save project
	#doc.open("M:/Photoscan/practise.psx")
	psxfile = root_path + 'practise.psx'
	doc.save( psxfile )
	print ('>> Saved to: ' + psxfile)

	## point to current chunk
	#chunk = doc.chunk

	## add a new chunk
	chunk = doc.addChunk()

	## set coordinate system
	# - PhotoScan.CoordinateSystem("EPSG::4612") -->  JGD2000
	chunk.crs = PhotoScan.CoordinateSystem("EPSG::4612")

	################################################################################################
	### get photo list ###
	photoList = []
	getPhotoList(root_path, photoList)
	#print (photoList)
	
	################################################################################################
	### add photos ###
	# addPhotos(filenames[, progress])
	# - filenames(list of string) – A list of file paths.
	chunk.addPhotos(photoList)
	
	################################################################################################
	### align photos ###
	## Perform image matching for the chunk frame.
	# matchPhotos(accuracy=HighAccuracy, preselection=NoPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=4000[, progress])
	# - Alignment accuracy in [HighestAccuracy, HighAccuracy, MediumAccuracy, LowAccuracy, LowestAccuracy]
	# - Image pair preselection in [ReferencePreselection, GenericPreselection, NoPreselection]
	chunk.matchPhotos(accuracy=PhotoScan.LowAccuracy, preselection=PhotoScan.ReferencePreselection, filter_mask=False, keypoint_limit=0, tiepoint_limit=0)
	chunk.alignCameras()

	################################################################################################
	### build dense cloud ###
	## Generate depth maps for the chunk.
	# buildDenseCloud(quality=MediumQuality, filter=AggressiveFiltering[, cameras], keep_depth=False, reuse_depth=False[, progress])
	# - Dense point cloud quality in [UltraQuality, HighQuality, MediumQuality, LowQuality, LowestQuality]
	# - Depth filtering mode in [AggressiveFiltering, ModerateFiltering, MildFiltering, NoFiltering]
	chunk.buildDenseCloud(quality=PhotoScan.LowQuality, filter=PhotoScan.AggressiveFiltering)

	################################################################################################
	### build mesh ###
	## Generate model for the chunk frame.
	# buildModel(surface=Arbitrary, interpolation=EnabledInterpolation, face_count=MediumFaceCount[, source ][, classes][, progress])
	# - Surface type in [Arbitrary, HeightField]
	# - Interpolation mode in [EnabledInterpolation, DisabledInterpolation, Extrapolated]
	# - Face count in [HighFaceCount, MediumFaceCount, LowFaceCount]
	# - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
	chunk.buildModel(surface=PhotoScan.HeightField, interpolation=PhotoScan.EnabledInterpolation, face_count=PhotoScan.HighFaceCount)
	
	################################################################################################
	### build texture (optional) ###
	## Generate uv mapping for the model.
	# buildUV(mapping=GenericMapping, count=1[, camera ][, progress])
	# - UV mapping mode in [GenericMapping, OrthophotoMapping, AdaptiveOrthophotoMapping, SphericalMapping, CameraMapping]
	#chunk.buildUV(mapping=PhotoScan.AdaptiveOrthophotoMapping)
	## Generate texture for the chunk.
	# buildTexture(blending=MosaicBlending, color_correction=False, size=2048[, cameras][, progress])
	# - Blending mode in [AverageBlending, MosaicBlending, MinBlending, MaxBlending, DisabledBlending]
	#chunk.buildTexture(blending=PhotoScan.MosaicBlending, color_correction=True, size=30000)

	################################################################################################
	## save the project before build the DEM and Ortho images
	doc.save()

	################################################################################################
	### build DEM (before build dem, you need to save the project into psx) ###
	## Build elevation model for the chunk.
	# buildDem(source=DenseCloudData, interpolation=EnabledInterpolation[, projection ][, region ][, classes][, progress])
	# - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
	chunk.buildDem(source=PhotoScan.DenseCloudData, interpolation=PhotoScan.EnabledInterpolation, projection=chunk.crs)

	################################################################################################
	## Build orthomosaic for the chunk.
	# buildOrthomosaic(surface=ElevationData, blending=MosaicBlending, color_correction=False[, projection ][, region ][, dx ][, dy ][, progress])
	# - Data source in [PointCloudData, DenseCloudData, ModelData, ElevationData]
	# - Blending mode in [AverageBlending, MosaicBlending, MinBlending, MaxBlending, DisabledBlending]
	chunk.buildOrthomosaic(surface=PhotoScan.ModelData, blending=PhotoScan.MosaicBlending, color_correction=True, projection=chunk.crs)
	
	################################################################################################
	## auto classify ground points (optional)
	#chunk.dense_cloud.classifyGroundPoints()
	#chunk.buildDem(source=PhotoScan.DenseCloudData, classes=[2])
	
	################################################################################################
	doc.save()

# main
folder = "M:/Photoscan/Photos/"
photoscanProcess(folder)









