import rasterio
import numpy as np
import xarray as xr

def load_geotiff(file_path):
    """
    Load a single NDVI GeoTIFF and return both the data and metadata.
    
    Parameters:
        file_path (str): Location of the GeoTIFF file.
        
    Returns:
        data (np.ndarray): NDVI values from the file.
        meta (dict): Metadata describing the GeoTIFF (projection, resolution, etc.).
    """
    # Open the GeoTIFF file safely using rasterio
    with rasterio.open(file_path) as src:
        # Read the first band
        data = src.read(1)
        # Save the file's metadata for later use
        meta = src.meta
    return data, meta

def load_multitemporal_geotiffs(file_paths):
    """
    Load a series of NDVI GeoTIFFs and combine them into a single xarray DataArray.
    
    Parameters:
        file_paths (list of str): Paths to multiple GeoTIFF files.
        
    Returns:
        xr.DataArray: NDVI data arranged with a time dimension for temporal analysis.
    """
    data_list = []
    
    # Read each GeoTIFF and collect the data
    for path in file_paths:
        data, meta = load_geotiff(path)
        data_list.append(data)
    
    # Stack all NDVI arrays along a new time axis
    stacked = np.stack(data_list, axis=0)
    
    # Convert the stacked array into an xarray DataArray for easier temporal operations
    da = xr.DataArray(stacked, dims=("time", "y", "x"))
    
    return da
