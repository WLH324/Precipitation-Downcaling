# Precipitation-Downcaling
All the scripts are post-processing steps following the downscaling operation using MGWR 2.2 software, and should be executed sequentially according to their file names.
The script "1_CSV interpolation" performs interpolation of the coefficients and residuals obtained from the MGWR output to the target resolution, facilitating the generation of high-resolution precipitation results in subsequent steps.
The script "2_downscaling1" performs operations on the above coefficients and residuals to obtain high-resolution precipitation data. In this script, the coefficients need to be placed in a separate folder, and the high-resolution .tif data should be placed in another folder.
The script "2_downscaling2" is used to check the downscaling results and ensure that the precipitation values are greater than or equal to 0.
At this point, we have obtained high-resolution monthly precipitation data.
The script "3_Calculate daily proportion" is used to compute the ratio of each original daily-scale data value to the corresponding monthly-scale data. After completing this operation, a mask extraction should be applied to the result.
The script "4_resampling" is used to resample the original ratio data to the target resolution.
The script "5_downscaling daily" is used to calculate high-resolution daily-scale data using high-resolution ratio data and high-resolution monthly-scale data. 
At this point, the downscaling results are completed.
The script "daily correction" is use to improve the accuracy of downscaled daily data.
