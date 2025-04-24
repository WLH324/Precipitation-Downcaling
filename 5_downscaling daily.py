# -*- coding: UTF-8 -*-
import os
import arcpy
from arcpy import env
from arcpy.sa import *


# Define the paths for daily data, monthly data, and output results folder
daily_data_folder = r'your path'  # Replace with the path of your daily data folder, ratio data
monthly_data_folder = r'your path'  # Replace with the path of your monthly data folder, downscaled monthly data
output_folder = r'your path'  # Replace with the path of your output results folder

# Set workspace
arcpy.env.workspace = daily_data_folder
arcpy.env.overwriteOutput = True

# Get the list of daily data files
daily_files = arcpy.ListRasters("*_Percentage.tif", "TIF")
print(daily_files)

# Set workspace back to default
arcpy.env.workspace = monthly_data_folder

# Get the list of monthly data files
monthly_files = arcpy.ListRasters("*", "TIF")
print(monthly_files)

# Set workspace back to default
arcpy.env.workspace = r'your path'  # Set back to the default workspace path

# Iterate through daily data files
for daily_file in daily_files:
    # Parse the date information from the daily data filename, such as '20220104'
    year_month_day = daily_file.split('_')[0]

    # Extract the year and month, for example extracting '202201' from '20220104'
    year_month = year_month_day[:6]

    # Find the corresponding monthly data file
    matching_monthly_file = [file for file in monthly_files if file.startswith(year_month)]

    if matching_monthly_file:
        matching_monthly_file = matching_monthly_file[0]  # If a matching monthly data file is found, take the first one

        # Construct the full file paths
        daily_rainfall_file = os.path.join(daily_data_folder, daily_file)
        monthly_rainfall_file = os.path.join(monthly_data_folder, matching_monthly_file)

        expression = "\"{}\" * \"{}\"".format(daily_rainfall_file, monthly_rainfall_file)
        output_filename = "{}.tif".format(year_month_day)

        output_file = os.path.join(output_folder, output_filename)

        # Use the raster calculator for computation
        arcpy.gp.RasterCalculator_sa(expression, output_file)
