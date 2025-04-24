# This script performs interpolation (e.g., IDW, Kriging) directly on MGWR output CSV files
# -*- coding: UTF-8 -*-
import arcpy
from arcpy.sa import *
import os

# Input folder path containing multiple CSV files
csv_folder = r'your path'

# Output folder path for raster data
output_folder = r'your path'

# Path to the vector boundary shapefile
shp_file = r'your path.shp'


# List of column names of interest
interested_columns = ['mgwr_residual', 'beta_Intercept', 'beta_NDVI', 'beta_Wind_D',
                      'beta_Slope', 'beta_Slope_Correction',
                      'beta_Aspect_Correction', 'beta_Aspect', 'beta_DEM']  # Replace with your own column names

# Set working environment
arcpy.env.workspace = csv_folder

# Get list of CSV files
csv_files = arcpy.ListFiles("*.csv")

# Loop through each CSV file
for csv_file in csv_files:
    # Create point feature class from CSV
    arcpy.MakeXYEventLayer_management(csv_file, "x_coor", "y_coor", "EventLayer")

    # Use vector boundary file as the interpolation extent
    arcpy.env.extent = shp_file

    # Loop through each column of interest
    for column in interested_columns:
        # Create raster using IDW interpolation method
        out_idw = Idw("EventLayer", column, 0.002080995)

        # Construct the output raster file name
        base_name = os.path.splitext(os.path.basename(csv_file))[0]
        output_raster = os.path.join(output_folder, "{}_Raster.tif".format(column))

        # Save the generated raster
        out_idw.save(output_raster)


