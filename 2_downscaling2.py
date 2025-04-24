# -*- coding: UTF-8 -*-
import arcpy
import os

# Set the working environment
arcpy.env.workspace = r"your path"
arcpy.env.overwriteOutput = True

# Define the input TIF folder and the vector Shapefile path
input_folder = r"your path"
vector_shp = r"your path.shp"
output_folder = r"your path"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get the list of input TIF files
tif_files = arcpy.ListRasters("*", "TIF")
for tif_file in tif_files:
    print(tif_files)
# Debug: Check the file list
if not tif_files:
    print("No TIF files found. Please check the file path and workspace settings.")
else:
    print("The following TIF files were found:")
    for tif in tif_files:
        print(tif)

# Loop through each TIF file for processing
for input_tif in tif_files:
    input_tif_path = os.path.join(input_folder, input_tif)

    # Perform raster calculator operations
    # 1. Use SetNull
    setnull_expression = "SetNull(\"{}\" < 0, \"{}\")".format(input_tif_path, input_tif_path)
    setnull_result = os.path.join(output_folder, "setnull_" + input_tif)
    arcpy.gp.RasterCalculator_sa(setnull_expression, setnull_result)

    # 2. Use FocalStatistics and Con
    focal_mean_expression = "Con(IsNull(\"{}\"), FocalStatistics(\"{}\", NbrRectangle(10,10, 'CELL'), 'MEAN'), \"{}\")".format(setnull_result, setnull_result, setnull_result)
    focal_mean_result = os.path.join(output_folder, "focal_mean_" + input_tif)
    arcpy.gp.RasterCalculator_sa(focal_mean_expression, focal_mean_result)

    # 3. Extract by mask
    extract_by_mask_result = os.path.join(output_folder, input_tif)
    arcpy.gp.ExtractByMask_sa(focal_mean_result, vector_shp, extract_by_mask_result)

    print("Processing completed for:", input_tif)

print("All processing completed. Results are saved in:", output_folder)
