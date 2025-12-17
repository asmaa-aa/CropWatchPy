import sqlite3
import numpy as np
import pandas as pd
import os

class DatabaseManager:
    """
    Manages SQLite database interactions for CropWatchPy.
    Encapsulates connection handling and data persistence logic.
    """
    def __init__(self, db_path="cropwatch.db"):
        """
        Initialize the database manager.
        
        Parameters:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """
        Internal method to set up the database table if it doesn't exist.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create the results table with a timestamp
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ndvi_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                mean_ndvi REAL,
                std_ndvi REAL,
                anomaly_pixels INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def save_results(self, dates, mean_ndvi, std_ndvi, anomalies):
        """
        Store NDVI statistics and anomaly counts into the database.
        
        Parameters:
            dates (list of str): List of time steps (e.g., ["2023-06", "2023-07"])
            mean_ndvi (np.ndarray): Mean NDVI values per time step
            std_ndvi (np.ndarray): Standard deviation per time step
            anomalies (np.ndarray): Boolean array marking anomalies (time, y, x)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Insert NDVI stats and anomaly count for each time step
            for i, date in enumerate(dates):
                # Calculate total anomaly pixels for this time step
                anomaly_count = int(np.nansum(anomalies[i]))  
                
                cursor.execute("""
                    INSERT INTO ndvi_results (date, mean_ndvi, std_ndvi, anomaly_pixels)
                    VALUES (?, ?, ?, ?)
                """, (date, float(mean_ndvi[i]), float(std_ndvi[i]), anomaly_count))
            
            conn.commit()
            print(f" Results saved to database '{self.db_path}' successfully.")
        except Exception as e:
            print(f" Error saving to database: {e}")
        finally:
            conn.close()

    def fetch_all(self):
        """
        Retrieve all entries from the NDVI results table.
        
        Returns:
            list of tuples: All records from the table.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM ndvi_results")
        rows = cursor.fetchall()
        
        conn.close()
        return rows


def save_ndvi_to_csv_full(ndvi_array, anomalies, dates, csv_path="./data/ndvi_full.csv"):
    """
    Export the full NDVI dataset with anomaly flags into a CSV file.
    
    Parameters:
        ndvi_array (np.ndarray): NDVI data shaped (time, y, x)
        anomalies (np.ndarray): Boolean array marking anomalies
        dates (list of str): Labels for each time step
        csv_path (str): Output CSV file path
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    rows = []
    time_steps, ny, nx = ndvi_array.shape
    
    # Flatten the NDVI array so each pixel and time step becomes a row
    for t in range(time_steps):
        for y in range(ny):
            for x in range(nx):
                rows.append({
                    "Date": dates[t],
                    "Y": y,
                    "X": x,
                    "NDVI": ndvi_array[t, y, x],
                    "Anomaly": anomalies[t, y, x]
                })
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)
    print(f" Full NDVI data saved to CSV at '{csv_path}'")