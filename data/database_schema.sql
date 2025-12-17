-- ==========================================================
-- Database Schema for CropWatchPy
-- Description:
--   SQLite schema defining tables for NDVI analysis results.
--   This database stores per-date NDVI statistics and anomaly counts.
-- ==========================================================

-- Drop table if it already exists (for clean setup)
DROP TABLE IF EXISTS ndvi_results;

-- Create main results table
CREATE TABLE ndvi_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,              -- Label or timestamp of the NDVI image (e.g., '2023-06')
    mean_ndvi REAL,                  -- Mean NDVI value for that date
    std_ndvi REAL,                   -- Standard deviation of NDVI values
    anomaly_pixels INTEGER,          -- Number of pixels classified as anomalies
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of record creation
);

-- Optional: Index to speed up date-based queries
CREATE INDEX idx_ndvi_date ON ndvi_results(date);
