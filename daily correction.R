#install.packages('raster')
#install.packages('tidyverse')
#install.packages('sf')
#install.packages('gstat')
library(raster)
library(tidyverse)
library(sf)
library(gstat)

# This script is used to process daily GPM correction (TIF + station TXT)

train_shp <- st_read('training data.shp') # Path to training data
train_ids <- train_shp$StationId 


# GPM Correction -------------------------------------------------------------------
process_fun <- function(x){
  keys <- x %>% basename()
  
  obs_key <- str_sub(keys, 1, 6) # Extract the first 6 characters as date info
  
  obs_path <- paste0('the path of station TXT', obs_key, '.txt') 
  
  mon_key <- str_sub(keys,5,6) %>% as.integer() 
  day_key <- str_sub(keys,7,8) %>% as.integer()
  
  df <- read_csv(obs_path) %>% filter(Mon==mon_key,Day==day_key) # Filter observation data for the matching date
  df <- df %>% mutate(PRE_Time_2020=ifelse(PRE_Time_2020>9999,NA,PRE_Time_2020)) %>% drop_na(PRE_Time_2020)
  
  df_shp <- df %>% st_as_sf(coords=c("Lon","Lat"),crs=4326)
  
  rs <- raster(x) 
  # Extract station values and proceed
  df_shp['GPM'] <- raster::extract(rs,df_shp)
  shp_used <- df_shp  %>% filter(!is.na(GPM)) # Keep only valid (non-NA) values
  shp_used <- st_transform(shp_used,crs(rs)) # Ensure same coordinate system between points and raster
  
  shp_used <- shp_used %>% mutate(p = PRE_Time_2020 - GPM) # Geographical difference method
  shp_used <- shp_used %>% filter(StationId %in% train_ids) # Use only training stations for correction
  gs <- gstat(formula=p~1, locations=shp_used %>% as('Spatial'), nmax=10) # IDW interpolation
  
  p_rs <- interpolate(rs, gs) # Interpolation
  # plot(p_rs)
  p_rs <- mask(p_rs, rs)
  # plot(p_rs)
  # Save the interpolated raster
  
  
  re <- max(p_rs+rs,0) # Geographical difference method
  out_name <- paste0("the path of output TIF/",keys,'.tif')  # Output path
  writeRaster(re,out_name)
  return(TRUE) 
}

fs <- list.files('the path of input TIF/',pattern = '.tif$',full.names = T) # Input directory

for (i in fs) {
  process_fun(i)
}
