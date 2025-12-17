import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import numpy as np

# --- Project Imports ---
from data_loader import load_multitemporal_geotiffs
from preprocessing import clean_ndvi
from visualization import show_ndvi_dashboard, plot_ndvi_timeseries
from database import DatabaseManager, save_ndvi_to_csv_full
from analysis import VegetationAnalyzer

class CropWatchGUI:
    def __init__(self, master):
        # Set up main window
        self.master = master
        self.master.title("CropWatchPy – NDVI Monitoring")
        self.master.geometry("600x600")
        
        # --- UI Components ---
        
        # Instruction label
        self.label = tk.Label(master, text="Select NDVI GeoTIFF files:", font=("Arial", 12))
        self.label.pack(pady=10)
        
        # Listbox to show selected files
        self.file_listbox = tk.Listbox(master, width=70, height=20)
        self.file_listbox.pack(pady=5)
        
        # Button to add NDVI files
        self.add_button = tk.Button(master, text="Add NDVI Files", command=self.add_files, width=20, bg="#A8BBA3")
        self.add_button.pack(pady=5)
        
        # Button to start analysis
        self.run_button = tk.Button(master, text="Run Analysis", command=self.run_analysis, width=20, bg="#A8BBA3")
        self.run_button.pack(pady=10)
        
        # Button to view time-series plots (disabled initially)
        self.plot_button = tk.Button(master, text="View NDVI Trends", command=self.plot_results, width=20, bg="#778873", state="disabled")
        self.plot_button.pack(pady=5)
        
        # Button to launch interactive dashboard (disabled initially)
        self.launch_dash_button = tk.Button(master, text="Launch Dashboard", command=self.launch_dash, width=20, bg="#778873", state="disabled")
        self.launch_dash_button.pack(pady=5)
        
        # Status label
        self.status_label = tk.Label(master, text="Status: Waiting for input...", fg="gray")
        self.status_label.pack(pady=20)
        
        # --- Internal State ---
        self.file_paths = []      # List of selected GeoTIFF paths
        self.dates = []           # List of corresponding time labels
        self.mean_ndvi = None     # Array of mean NDVI per time step
        self.anomalies = None     # Boolean array for detected anomalies
        self.ndvi_clean = None    # Cleaned NDVI values
        
        self.analyzer = VegetationAnalyzer(threshold=1.5)
        self.db_manager = DatabaseManager("cropwatch.db")

    def add_files(self):
        """Open a file dialog so the user can select NDVI GeoTIFF files."""
        files = filedialog.askopenfilenames(
            title="Select NDVI GeoTIFF Files", 
            filetypes=[("GeoTIFF Files", "*.tif *.tiff")]
        )
        if files:
            self.file_paths.extend(files)
            for f in files:
                self.file_listbox.insert(tk.END, f)
            self.status_label.config(text=f"Loaded {len(files)} files.")

    def run_analysis(self):
        """Start the NDVI processing pipeline in a background thread."""
        if not self.file_paths:
            messagebox.showerror("Error", "Please select NDVI files first.")
            return
        
        # Update status while processing
        self.status_label.config(text="Processing NDVI data... Please wait.", fg="blue")
        
        # Use a separate thread to keep the GUI responsive
        thread = threading.Thread(target=self._process_data)
        thread.start()

    def _process_data(self):
        """Internal method to load, clean, analyze, and save NDVI data."""
        try:
            # load Data
            ndvi_da = load_multitemporal_geotiffs(self.file_paths)
            
            # Preprocessing
            self.ndvi_clean = clean_ndvi(ndvi_da.values)
            # Analysis
            self.mean_ndvi, std_ndvi = self.analyzer.compute_stats(self.ndvi_clean)
            self.anomalies = self.analyzer.detect_anomalies(self.ndvi_clean)
            
            # Generate simple time labels
            self.dates = [f"Time-{i+1}" for i in range(self.ndvi_clean.shape[0])]
            
            # Save to Database 
            self.db_manager.save_results(self.dates, self.mean_ndvi, std_ndvi, self.anomalies)
            
            # UI Updates
            self.master.after(0, self._enable_buttons)
            self.master.after(0, lambda: self.status_label.config(text="Processing complete! Results saved to DB.", fg="green"))
            
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Processing Error", str(e)))
            self.master.after(0, lambda: self.status_label.config(text="Error during processing.", fg="red"))

    def _enable_buttons(self):
        """Helper to enable buttons safely."""
        self.plot_button.config(state="normal")
        self.launch_dash_button.config(state="normal")

    def plot_results(self):
        """Display a time-series plot of mean NDVI values."""
        if self.mean_ndvi is not None:
            plot_ndvi_timeseries(self.mean_ndvi, self.dates)
        else:
            messagebox.showerror("Error", "No analysis results available.")

    def launch_dash(self):
        """Launch an interactive dashboard to explore NDVI maps and anomalies."""
        if self.ndvi_clean is not None and self.anomalies is not None:
            try:
                # Display NDVI maps
                show_ndvi_dashboard(self.ndvi_clean, self.anomalies, self.dates)
                # Save full data to CSV (Utility function)
                save_ndvi_to_csv_full(self.ndvi_clean, self.anomalies, self.dates)
            except Exception as e:
                messagebox.showerror("Visualization Error", str(e))
        else:
            messagebox.showerror("Error", "No analysis results available.")

