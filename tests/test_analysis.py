import pytest
import numpy as np
import sys
import os
from src.analysis import VegetationAnalyzer


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def analyzer():
    """Fixture to create an analyzer instance."""
    return VegetationAnalyzer(threshold=1.5)

@pytest.fixture
def synthetic_data():
    """
    Creates a synthetic 3D NDVI array (time, y, x).
    Shape: (3 time steps, 4 rows, 5 columns)
    """
    np.random.seed(42)
    data = np.random.rand(3, 4, 5)  
    data[1, 2, 3] = -0.5
    return data

def test_compute_stats_shape(analyzer, synthetic_data):
    """Test if mean and std arrays have correct shapes."""
    mean, std = analyzer.compute_stats(synthetic_data)
    
    assert mean.shape[0] == 3
    assert std.shape[0] == 3
    assert mean.ndim == 1

def test_anomaly_detection(analyzer, synthetic_data):
    """Test if the known anomaly is correctly flagged."""
    anomalies = analyzer.detect_anomalies(synthetic_data)
    
    assert anomalies.shape == synthetic_data.shape
    assert anomalies[1, 2, 3] == True

def test_empty_array(analyzer):
    """Test behavior with empty input."""
    empty_data = np.array([]) 
    try:
        analyzer.compute_stats(empty_data)
    except (IndexError, ValueError, RuntimeWarning):
        pass  

def test_threshold_sensitivity():
    """Test that changing threshold affects sensitivity."""
    data = np.ones((1, 5, 5)) * 0.5
    data[0, 2, 2] = 0.3  
    
    strict_analyzer = VegetationAnalyzer(threshold=0.1)
    anomalies_strict = strict_analyzer.detect_anomalies(data)
    assert anomalies_strict[0, 2, 2] == True
    
    loose_analyzer = VegetationAnalyzer(threshold=10.0)
    anomalies_loose = loose_analyzer.detect_anomalies(data)
    assert anomalies_loose[0, 2, 2] == False