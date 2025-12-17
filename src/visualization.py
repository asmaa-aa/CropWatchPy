import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np


def plot_ndvi_timeseries(mean_ndvi, dates):
    """
    Plot a simple line chart showing the mean NDVI over time.
    
    Parameters:
        mean_ndvi (np.ndarray): Mean NDVI values for each time step.
        dates (list of str): Labels corresponding to each time step.
    """
    # Create a DataFrame for easier plotting with Plotly
    df = pd.DataFrame({"Date": dates, "Mean_NDVI": mean_ndvi})
    
    # Generate an interactive line plot of NDVI over time
    fig = px.line(df, x="Date", y="Mean_NDVI", title="Mean NDVI Time Series")
    fig.show()


def show_ndvi_dashboard(ndvi_array, anomalies, dates):
    """
    Display NDVI maps with anomalies in an interactive Matplotlib window.
    This does not require Flask or Dash; everything runs locally.
    
    Parameters:
        ndvi_array (np.ndarray): NDVI data shaped (time, y, x)
        anomalies (np.ndarray): Boolean array marking anomaly pixels
        dates (list of str): Time labels for each NDVI image
    """
    # Start with the first time step
    t = 0
    ndvi_img = ndvi_array[t]
    anomaly_mask = anomalies[t]

    # Create the main figure
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.25) 

    # Plot the NDVI map
    ndvi_plot = ax.imshow(ndvi_img, cmap="viridis", vmin=-1, vmax=1)
    
    # Overlay anomalies in red with transparency
    anomaly_overlay = ax.imshow(np.where(anomaly_mask, 1, np.nan), cmap="Reds", alpha=0.5)

    # Add a colorbar for NDVI values
    cbar = plt.colorbar(ndvi_plot, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("NDVI Value", rotation=270, labelpad=15)

    # Set initial title and hide axes
    ax.set_title(f"NDVI and Anomalies – {dates[t]}")
    ax.axis("off")

    # Add a slider to navigate through time steps
    ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
    slider = Slider(ax_slider, "Time Index", 0, len(dates)-1, valinit=0, valstep=1)

    # Update function to refresh the map when the slider changes
    def update(val):
        idx = int(slider.val)
        ndvi_plot.set_data(ndvi_array[idx])
        anomaly_overlay.set_data(np.where(anomalies[idx], 1, np.nan))
        ax.set_title(f"NDVI and Anomalies – {dates[idx]}")
        fig.canvas.draw_idle()

    # Link slider to update function
    slider.on_changed(update)
    
    # Display the interactive figure
    plt.show()
