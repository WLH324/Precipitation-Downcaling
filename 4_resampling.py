# -*- coding: UTF-8 -*-
import arcpy
import os

# Set workspace path
arcpy.env.workspace = r"your path"  # Replace with your folder path
output_folder = r"your path"  # Replace with your output folder path

# Get all raster data in the workspace
raster_list = arcpy.ListRasters()

# Select target raster data (assuming there is a raster named target_raster.tif)
target_raster = r"the path of target raster data.tif"  # Replace with your target raster data name, preferably on the desktop

# Get the row and column size of the target raster data
desc = arcpy.Describe(target_raster)
target_cell_size = desc.meanCellWidth  # Get the row size of the target raster data

# Iterate through all raster data in the folder
for raster in raster_list:
    # Construct the output file path
    output_raster = os.path.join(output_folder, "{}.tif".format(os.path.splitext(raster)[0]))

    # Perform resampling
    arcpy.ProjectRaster_management(
        in_raster=raster,
        out_raster=output_raster,
        out_coor_system=desc.spatialReference,  # Use the coordinate system of the target raster data
        resampling_type="BILINEAR",  # Use bilinear interpolation
        cell_size=target_cell_size  # Resample using the row and column size of the target raster data
    )

    print("{} resampling completed.".format(raster))
