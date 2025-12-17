
#  CropWatchPy: NDVI Monitoring & Vegetation Anomaly Detection

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

**CropWatchPy** is a desktop application designed to automate the processing of satellite imagery (GeoTIFFs) for agricultural research. It calculates the Normalized Difference Vegetation Index (NDVI), detects statistical anomalies in vegetation health over time, and persists results in a local database for longitudinal study.

---

##  Table of Contents
- [Project Motivation](#-project-motivation)
- [Key Features](#-key-features)
- [Project Architecture](#-project-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Testing](#-testing)
- [Authors](#-authors)

---

##  Project Motivation
In agricultural remote sensing, monitoring vegetation health manually across hundreds of satellite images is time-consuming and prone to error. 

This tool automates the workflow by:
1.  **Ingesting** multi-temporal GeoTIFF data.
2.  **Calculating** NDVI using the standard formula: $NDVI = (NIR - Red) / (NIR + Red)$.
3.  **Flagging** anomalies where vegetation health drops significantly (Z-score analysis).
4.  **Archiving** statistical results for future reporting.

##  Key Features
* **GUI Interface:** User-friendly Tkinter dashboard—no command line needed for daily use.
* **Automated Analysis:** Batch processes multiple time-steps instantly.
* **Anomaly Detection:** Uses statistical thresholds (Z-score > 1.5) to identify stressed crops.
* **Data Persistence:** Automatically saves all results to an SQLite database (`cropwatch.db`).
* **Visualization:** Interactive time-series dashboard with sliders to view changes over time.
* **Export:** Exports cleaned data and flags to CSV for use in Excel or R.

---

##  Project Architecture
The project follows a modular **Object-Oriented Design (OOP)** pattern:

```text
cropwatchpy/
│
├── src/
│   ├── main.py             # Entry point
│   ├── gui.py              # Main GUI Class (CropWatchGUI)
│   ├── analysis.py         # Analysis Logic Class (VegetationAnalyzer)
│   ├── database.py         # Database Management Class (DatabaseManager)
│   ├── data_loader.py      # GeoTIFF I/O utilities
│   ├── preprocessing.py    # Data cleaning functions
│   └── visualization.py    # Plotting logic
│
├── tests/                  # Unit tests (pytest)
├── data/                   # Sample GeoTIFFs and output CSVs
└── docs/                   # User Guides and Technical Reports
```
---

##  Installation

To run CropWatchPy on your local machine, follow these steps.

### Prerequisites
* **Python 3.8** or higher.
* **Git** (for cloning the repository).

### Step-by-Step Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/asmaa-aa/cropwatchpy.git](https://github.com/yourusername/cropwatchpy.git)
    cd cropwatchpy
    ```

2.  **Create a Virtual Environment** (Recommended)
    It is best practice to run this project in an isolated environment to avoid library conflicts.

    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies**
    Install the required libraries (rasterio, pandas, matplotlib, pytest, etc.) using the provided requirements file.
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

### 1. Launch the Application
Execute the main script from the project root directory:
```bash
python src/main.py
