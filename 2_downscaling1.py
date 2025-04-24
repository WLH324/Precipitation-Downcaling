# -*- coding: UTF-8 -*-
import arcpy
from arcpy import env
from arcpy.sa import *
import os

# Allow overwriting existing raster data
arcpy.env.overwriteOutput = True

# Root directory for beta files
beta_root_folder = r"your path"

# Root directory for other datasets
other_data_root_folder = r"your path"

# Output folder for the new result rasters
result_folder = r"your path"
if not os.path.exists(result_folder):
    os.makedirs(result_folder)  # Create the result folder if it doesn't exist

# Paths for DEM, Aspect, and Slope data (these are static and do not vary over time)
DEM_clip = Raster(os.path.join(other_data_root_folder, "DEM", "DEM.tif"))
Aspect_clip = Raster(os.path.join(other_data_root_folder, "Aspect", "Aspect.tif"))
Slope_clip = Raster(os.path.join(other_data_root_folder, "Slope", "Slope.tif"))

# Loop through all subfolders under the beta folder (each subfolder represents a time point)
for folder_name in os.listdir(beta_root_folder):
    folder_path = os.path.join(beta_root_folder, folder_name)
    if os.path.isdir(folder_path):
        # Parse year and month from folder name
        year_month = folder_name  # Assuming folder name is in the format of year and month

        # Construct paths for time-specific datasets
        monthly_Aspect_Correction_path = os.path.join(other_data_root_folder, "Aspect_Correction",
                                                      year_month + "_Monthly_Aspect_Correction.tif")
        Max_NDVI_clip_path = os.path.join(other_data_root_folder, "NDVI", year_month + ".tif")  # NDVI file name
        monthly_Slope_Correction_path = os.path.join(other_data_root_folder, "Slope_Correction",
                                                     year_month + "_Monthly_Slope_Correction.tif")
        monthly_Wind_D_path = os.path.join(other_data_root_folder, "Wind_D", year_month + "_Monthly_Wind_D.tif")
        # monthly_Average_LST_path = os.path.join(other_data_root_folder, "LST", year_month + "_Monthly_Average_LST.tif")
        # monthly_MOD05_path = os.path.join(other_data_root_folder, "MOD05", year_month + "_Monthly_MOD05.tif")
        # Make sure the tif file names match exactly

        # Read beta raster data
        beta_Aspect_Correction = Raster(os.path.join(folder_path, "beta_Aspect_Correction_Raster.tif"))
        beta_Aspect = Raster(os.path.join(folder_path, "beta_Aspect_Raster.tif"))
        beta_DEM = Raster(os.path.join(folder_path, "beta_DEM_Raster.tif"))
        beta_Intercept = Raster(os.path.join(folder_path, "beta_Intercept_Raster.tif"))
        beta_NDVI = Raster(os.path.join(folder_path, "beta_NDVI_Raster.tif"))
        beta_Slope_Correction = Raster(os.path.join(folder_path, "beta_Slope_Correction_Raster.tif"))
        beta_Slope = Raster(os.path.join(folder_path, "beta_Slope_Raster.tif"))
        beta_Wind_D = Raster(os.path.join(folder_path, "beta_Wind_D_Raster.tif"))
        mgwr_residual = Raster(os.path.join(folder_path, "mgwr_residual_Raster.tif"))
        # y_residual = Raster(os.path.join(folder_path, "y_residual_Raster.tif"))
        # beta_LST = Raster(os.path.join(folder_path, "beta_LST_Raster.tif"))
        # beta_MOD05 = Raster(os.path.join(folder_path, "beta_MOD05_Raster.tif"))

        # Read monthly datasets
        Monthly_Aspect_Correction = Raster(monthly_Aspect_Correction_path)
        # Monthly_Average_LST = Raster(monthly_Average_LST_path)
        # Monthly_MOD05 = Raster(monthly_MOD05_path)
        Max_NDVI_clip = Raster(Max_NDVI_clip_path)
        Monthly_Slope_Correction = Raster(monthly_Slope_Correction_path)
        Monthly_Wind_D = Raster(monthly_Wind_D_path)

        # Perform raster calculation
        result = (beta_Aspect_Correction * Monthly_Aspect_Correction) + \
                 (beta_Aspect * Aspect_clip) + \
                 (beta_DEM * DEM_clip) + \
                 beta_Intercept + \
                 (beta_NDVI * Max_NDVI_clip) + \
                 (beta_Slope_Correction * Monthly_Slope_Correction) + \
                 (beta_Slope * Slope_clip) + \
                 (beta_Wind_D * Monthly_Wind_D) + \
                 mgwr_residual

        # Save the result using the year and month as the filename in the output folder
        result_path = os.path.join(result_folder, "{0}.tif".format(year_month))
        result.save(result_path)

        print("Calculation completed and saved to: {}".format(result_path))
