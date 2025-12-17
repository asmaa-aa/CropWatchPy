import sys
import os
import numpy as np
import pytest
from src.preprocessing import clean_ndvi
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def synthetic_ndvi_example():
    """
    Example fixture to provide synthetic NDVI data for testing.
    Not strictly needed here but can be expanded for future tests.
    """
    pass  


def test_fill_value_replaced():
    """
    Test that the specified fill value is correctly replaced with NaN.
    """
    arr = np.array([[0.2, -9999], [0.5, 0.1]])
    cleaned = clean_ndvi(arr, fill_value=-9999)
    
    assert np.isnan(cleaned[0,1])
    
    assert cleaned[0,0] == 0.2
    assert cleaned[1,0] == 0.5


def test_extreme_values_replaced():
    """
    Test that extremely high or low NDVI values are replaced with NaN.
    """
    arr = np.array([[-20000, 0.1], [10001, -0.5]])
    cleaned = clean_ndvi(arr)
    
    assert np.isnan(cleaned[0,0])
    assert np.isnan(cleaned[1,0])
    
    assert cleaned[0,1] == 0.1
    assert cleaned[1,1] == -0.5


def test_no_change_for_valid_data():
    """
    Test that valid NDVI values are not altered during cleaning.
    """
    arr = np.array([[-0.1, 0.0], [0.5, 0.9]])
    cleaned = clean_ndvi(arr)
    
    assert np.allclose(cleaned, arr, equal_nan=True)


def test_zero_values_kept_by_default():
    """
    Test that zero values are preserved by default unless explicitly removed.
    """
    arr = np.array([[0, 0.2], [0.3, -0.1]])
    cleaned = clean_ndvi(arr)
    
    assert cleaned[0,0] == 0
