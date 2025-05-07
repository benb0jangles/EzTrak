# EZ_TRACK_ROTATOR.py
# MIT License
# Copyright (c) 2025 Benb0jangles
# Simplified GUI-only version with no functionality

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Configuration
DEFAULT_IP = "192.168.1.100"  # Default IP address of the ESP32-S3
DEFAULT_PORT = 4533  # Default port for rotctl (standard for hamlib)
ANIMATION_INTERVAL = 100  # Animation update interval in milliseconds

# Default location
DEFAULT_LAT = 01.234567  # Default latitude
DEFAULT_LON = 0.123456  # Default longitude
DEFAULT_ALT = 1337  # Default altitude in meters
MIN_ELEVATION = 20  # Minimum elevation in degrees for satellite passes

# Rotator limits
MIN_AZ = 0
MAX_AZ = 360
MIN_EL = 0
MAX_EL = 180

# User can edit these satellites
USER_SELECTED_SATELLITES = [
    "NOAA 19",
    "METOP-C",
    "ISS (ZARYA)"
]

class RotatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EZ-Track Rotator Control")
        self.root.geometry("1000x800")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Create the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the top frame for connection settings
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=5)
        
        # IP Address entry
        ttk.Label(self.top_frame, text="IP Address:").pack(side=tk.LEFT, padx=5)
        self.ip_var = tk.StringVar(value=DEFAULT_IP)
        self.ip_entry = ttk.Entry(self.top_frame, textvariable=self.ip_var, width=15)
        self.ip_entry.pack(side=tk.LEFT, padx=5)
        
        # Port entry
        ttk.Label(self.top_frame, text="Port:").pack(side=tk.LEFT, padx=5)
        self.port_var = tk.StringVar(value=str(DEFAULT_PORT))
        self.port_entry = ttk.Entry(self.top_frame, textvariable=self.port_var, width=6)
        self.port_entry.pack(side=tk.LEFT, padx=5)
        
        # Dummy function for all buttons
        def dummy_function(*args, **kwargs):
            pass
        
        # Connect button
        self.connect_button = ttk.Button(self.top_frame, text="Connect", command=dummy_function)
        self.connect_button.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Disconnected")
        self.status_label = ttk.Label(self.top_frame, textvariable=self.status_var, foreground="red")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Create the location frame
        self.location_frame = ttk.LabelFrame(self.main_frame, text="Observer Location", padding="5")
        self.location_frame.pack(fill=tk.X, pady=5)
        
        # Location entries
        ttk.Label(self.location_frame, text="Latitude:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.lat_var = tk.StringVar(value=str(DEFAULT_LAT))
        self.lat_entry = ttk.Entry(self.location_frame, textvariable=self.lat_var, width=10)
        self.lat_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(self.location_frame, text="Longitude:").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.lon_var = tk.StringVar(value=str(DEFAULT_LON))
        self.lon_entry = ttk.Entry(self.location_frame, textvariable=self.lon_var, width=10)
        self.lon_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(self.location_frame, text="Altitude (m):").grid(row=0, column=4, padx=5, pady=2, sticky=tk.W)
        self.alt_var = tk.StringVar(value=str(DEFAULT_ALT))
        self.alt_entry = ttk.Entry(self.location_frame, textvariable=self.alt_var, width=6)
        self.alt_entry.grid(row=0, column=5, padx=5, pady=2)
        
        # Update location button
        self.update_loc_button = ttk.Button(self.location_frame, text="Update Location", command=dummy_function)
        self.update_loc_button.grid(row=0, column=6, padx=10, pady=2)
        
        # Create the control frame with two columns
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Left column - Manual control
        self.manual_frame = ttk.LabelFrame(self.control_frame, text="Manual Control", padding="10")
        self.manual_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Current position display
        ttk.Label(self.manual_frame, text="Current Position:").grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.current_pos_var = tk.StringVar(value="AZ: 0.0° EL: 0.0°")
        ttk.Label(self.manual_frame, textvariable=self.current_pos_var, font=("Arial", 12, "bold")).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Target position entry
        ttk.Label(self.manual_frame, text="Target Azimuth:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.target_az_var = tk.StringVar(value="0.0")
        self.target_az_entry = ttk.Entry(self.manual_frame, textvariable=self.target_az_var, width=8)
        self.target_az_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.manual_frame, text="Target Elevation:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.target_el_var = tk.StringVar(value="0.0")
        self.target_el_entry = ttk.Entry(self.manual_frame, textvariable=self.target_el_var, width=8)
        self.target_el_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Move button
        self.move_button = ttk.Button(self.manual_frame, text="Move to Position", command=dummy_function)
        self.move_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Home button
        self.home_button = ttk.Button(self.manual_frame, text="Home Rotator", command=dummy_function)
        self.home_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Stop button
        self.stop_button = ttk.Button(self.manual_frame, text="Stop", command=dummy_function)
        self.stop_button.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Right column - Satellite tracking
        self.tracking_frame = ttk.LabelFrame(self.control_frame, text="Satellite Tracking", padding="10")
        self.tracking_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Satellite selection
        ttk.Label(self.tracking_frame, text="Select Satellite:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.satellite_var = tk.StringVar()
        self.satellite_combo = ttk.Combobox(self.tracking_frame, textvariable=self.satellite_var, state="readonly")
        self.satellite_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Set some sample values for the combobox
        self.satellite_combo['values'] = USER_SELECTED_SATELLITES
        if USER_SELECTED_SATELLITES:
            self.satellite_combo.current(0)
        
        # Update TLE button
        self.update_tle_button = ttk.Button(self.tracking_frame, text="Update TLE Data", command=dummy_function)
        self.update_tle_button.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Next pass info
        ttk.Label(self.tracking_frame, text="Next Pass:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.next_pass_var = tk.StringVar(value="No pass data available")
        ttk.Label(self.tracking_frame, textvariable=self.next_pass_var).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Cycle through passes button
        self.next_pass_button = ttk.Button(self.tracking_frame, text="Next Pass", command=dummy_function)
        self.next_pass_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Start tracking button
        self.track_button = ttk.Button(self.tracking_frame, text="Start Tracking", command=dummy_function)
        self.track_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Create the plot frame
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create the circular plot
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111, polar=True)
        self.ax.set_theta_zero_location('N')  # 0 degrees at North
        self.ax.set_theta_direction(-1)  # Clockwise
        self.ax.set_rlim(0, 90)  # Set max radius to 90 (horizon to zenith)
        
        # Add compass labels
        self.ax.set_xticks(np.pi/180. * np.array([0, 90, 180, 270]))
        self.ax.set_xticklabels(['N (0°)', 'E (90°)', 'S (180°)', 'W (270°)'])
        
        # Add concentric circles for elevation
        elevation_circles = [0, 15, 30, 45, 60, 75]
        for elevation in elevation_circles:
            radius = 90 - elevation
            circle = plt.Circle((0, 0), radius, transform=self.ax.transData._b, 
                               fill=False, edgecolor='gray', alpha=0.5, ls='--')
            self.ax.add_artist(circle)
            self.ax.text(0, radius, f"{elevation}°", ha='center', va='bottom',
                       bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        
        # Center text for 90° elevation
        self.ax.text(0, 0, "90°", ha='center', va='center',
                   bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        # Initialize the position marker (red dot for current position)
        self.position_marker, = self.ax.plot([], [], 'ro', markersize=10)
        
        # Initialize the satellite pass line
        self.satellite_line, = self.ax.plot([], [], 'b-', linewidth=2, alpha=0.7)
        self.pass_start_marker, = self.ax.plot([], [], 'go', markersize=8)
        self.pass_end_marker, = self.ax.plot([], [], 'yo', markersize=8)
        
        # Embed the plot in the tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Simple animation update function - does nothing
        def update_plot(frame):
            return self.position_marker, self.satellite_line, self.pass_start_marker, self.pass_end_marker
        
        # Set up animation
        self.ani = FuncAnimation(self.fig, update_plot, interval=ANIMATION_INTERVAL, blit=False)
    
    def on_close(self):
        """Handle window close event."""
        self.root.destroy()

def main():
    """Main function to start the application."""
    root = tk.Tk()
    app = RotatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()