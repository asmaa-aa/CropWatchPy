import numpy as np

class VegetationAnalyzer:
    """
    Encapsulates logic for NDVI statistical analysis and anomaly detection.
    """
    def __init__(self, threshold=1.5):
        self.threshold = threshold

    def compute_stats(self, ndvi_array):
        """Calculate mean and std"""
        mean = np.nanmean(ndvi_array, axis=(1,2))
        std = np.nanstd(ndvi_array, axis=(1,2))
        return mean, std

    def detect_anomalies(self, ndvi_array):
        """Identify anomalies based on the initialized threshold."""
        mean, std = self.compute_stats(ndvi_array)
        anomalies = np.zeros_like(ndvi_array, dtype=bool)
        
        for t in range(ndvi_array.shape[0]):
            z_score = (ndvi_array[t] - mean[t]) / (std[t] + 1e-6)
            anomalies[t] = z_score < -self.threshold
            
        return anomalies