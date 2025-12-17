import numpy as np

def clean_ndvi(ndvi_array, fill_value=-9999):
    """
    Clean NDVI data by replacing invalid or corrupted values with NaN.
    
    Parameters:
        ndvi_array (np.ndarray): NDVI data array.
        fill_value (float): Specific value in the array to treat as invalid.
        
    Returns:
        np.ndarray: NDVI array with invalid values replaced by NaN.
    """
    # Make sure the array is float type to allow NaN values
    ndvi_clean = ndvi_array.astype(float)
    
    # Replace any pixel with the fill value with NaN
    ndvi_clean[ndvi_clean == fill_value] = np.nan
    
    # Replace extreme outliers that are likely errors
    ndvi_clean[ndvi_clean < -10000] = np.nan   
    ndvi_clean[ndvi_clean > 10000] = np.nan    

    # Print the original NDVI min and max for quick inspection
    print(f"NDVI min: {np.nanmin(ndvi_array)}, max: {np.nanmax(ndvi_array)}")
    
    return ndvi_clean
