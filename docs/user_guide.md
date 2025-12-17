***


#  CropWatchPy User Guide

Welcome to the **CropWatchPy** user manual. This guide will help you navigate the application to monitor vegetation health using satellite imagery.

---

## 1. Getting Started

### Launching the App
1. Open your terminal or command prompt.
2. Navigate to the project folder.
3. Run the command: `python src/main.py`

The main window will appear, looking like this:

<img width="770" height="807" alt="image" src="https://github.com/user-attachments/assets/1a894c29-5e1a-43b5-bd41-377eb2089335" />


---

## 2. Analyzing Your Data

### Step 1: Loading Files
Click the **"Add NDVI Files"** button (Blue). 
* A file dialog will open.
* Select the GeoTIFF (`.tif`) images you wish to analyze. 


https://github.com/user-attachments/assets/25786106-561f-4789-9587-9f805d9c92ea



### Step 2: Running the Analysis
Once files are listed in the white box, click the **"Run Analysis"** button (Green).

**What happens next?**
* The system loads the images.
* It removes invalid data .
* It calculates the Mean NDVI and Standard Deviation for each date.
* It detects "Anomalies" (areas where vegetation is significantly lower than average).
* **Data is automatically saved** to the internal database.

Wait until the status bar at the bottom says:  
 *"Processing complete! Results saved to DB."*


https://github.com/user-attachments/assets/36089926-b488-4c7c-895c-0da9889a85bd


---

## 3. Visualization Tools

Once the analysis is done, the visualization buttons become active.

###  View NDVI Trends
Click this button to see a line chart.
* **X-Axis:** Time steps (Dates).
* **Y-Axis:** Average NDVI Health.
* **Use case:** Quickly see if the overall crop health is improving or declining.

<img width="1868" height="927" alt="image" src="https://github.com/user-attachments/assets/89c04bed-300b-45b9-b5bc-ecf63cd96666" />


###  Launch Dashboard
Click this button to open the interactive map explorer.
* **Left Image:** The actual NDVI map.
* **Right/Overlay:** Red highlights showing where anomalies were detected.
* **Slider:** Use the slider at the bottom to move forward and backward through time.

<img width="1010" height="852" alt="image" src="https://github.com/user-attachments/assets/f87968f2-8ecf-4e85-8ee1-4415facb3b73" />

---

## 4. Exporting Data
Every time you run the dashboard, the application automatically exports a detailed CSV file to:
`data/ndvi_full.csv`

---

## 5. Troubleshooting

| Issue | Possible Cause | Solution |
| :--- | :--- | :--- |
| **"Please select NDVI files first"** | You clicked Run without adding files. | Click "Add NDVI Files" first. |
| **App crashes on load** | Corrupt GeoTIFF file. | Ensure your `.tif` files are valid satellite images. |
| **No Anomalies detected** | The vegetation is stable. | This is good news! Or, the threshold is too high. |

---


