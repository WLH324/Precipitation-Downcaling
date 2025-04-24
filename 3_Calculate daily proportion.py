import os
import numpy as np
import rasterio

# Folder paths for daily and monthly precipitation data
daily_data_folder = r' the path of Original daily data'  # Replace with the path to your daily data folder
monthly_data_folder = r'the path of Original monthly data'  # Replace with the path to your monthly data folder
output_folder = r'the path of interpolation'  # Replace with the path to your output folder

# Get list of daily and monthly raster files
daily_files = [filename for filename in os.listdir(daily_data_folder) if filename.endswith('.tif')]
monthly_files = [filename for filename in os.listdir(monthly_data_folder) if filename.endswith('Monthly_Rainfall.tif')]
print(daily_files)
print(monthly_files)

# Iterate through daily data files
for daily_file in daily_files:
    # Parse year and month from daily filename, e.g., '20220101.tif' -> '202201'
    year_month = daily_file[:6]

    # Find the corresponding monthly file
    matching_monthly_file = [file for file in monthly_files if year_month in file]

    if matching_monthly_file:
        matching_monthly_file = matching_monthly_file[0]  # Use the first match if found

        # Construct full file paths
        daily_rainfall_file = os.path.join(daily_data_folder, daily_file)
        monthly_rainfall_file = os.path.join(monthly_data_folder, matching_monthly_file)

        # Read and process daily and corresponding monthly data
        with rasterio.open(daily_rainfall_file) as daily_src, rasterio.open(monthly_rainfall_file) as monthly_src:
            daily_data = daily_src.read(1)
            monthly_data = monthly_src.read(1)

            # Calculate the proportion of daily rainfall to monthly total rainfall
            rainfall_percentage = np.divide(daily_data, monthly_data, out=np.zeros_like(daily_data),
                                            where=monthly_data != 0)

            # Create output filename based on daily filename
            output_filename = f"{daily_file[:-4]}_Percentage.tif"  # Remove '.tif' and append '_Percentage.tif'
            output_file = os.path.join(output_folder, output_filename)  # Replace with your output folder path

            # Write result to a new raster file
            with rasterio.open(
                    output_file,
                    'w',
                    driver='GTiff',
                    height=daily_src.height,
                    width=daily_src.width,
                    count=1,
                    dtype=rasterio.float32,
                    crs=daily_src.crs,
                    transform=daily_src.transform,
            ) as dst:
                dst.write(rainfall_percentage, 1)
