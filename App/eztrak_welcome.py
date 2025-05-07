import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

# Create the main window
root = tk.Tk()
root.title("EZ-Trak Satellite Tracking")
root.geometry("600x650")  # Maintained height to show all buttons

# Apply a theme
style = ttk.Style()
style.theme_use('clam')  # Use a modern theme

# Create the main frame with padding
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a header with a title
header_frame = ttk.Frame(main_frame)
header_frame.pack(fill=tk.X, pady=(0, 20))

title_label = ttk.Label(header_frame, text="Welcome to EZ-Trak Satellite Tracking", 
                        font=("Arial", 16, "bold"))
title_label.pack(side=tk.TOP)

# Create the location frame
location_frame = ttk.LabelFrame(main_frame, text="Observer Location", padding="10")
location_frame.pack(fill=tk.X, pady=10)

# Location entries with StringVars
ttk.Label(location_frame, text="Latitude:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
lat_var = tk.StringVar()
lat_entry = ttk.Entry(location_frame, textvariable=lat_var, width=15)
lat_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(location_frame, text="Longitude:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
lon_var = tk.StringVar()
lon_entry = ttk.Entry(location_frame, textvariable=lon_var, width=15)
lon_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(location_frame, text="Altitude (m):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
alt_var = tk.StringVar()
alt_entry = ttk.Entry(location_frame, textvariable=alt_var, width=15)
alt_entry.grid(row=1, column=1, padx=5, pady=5)

# Dummy function for buttons
def dummy_function():
    pass

update_loc_button = ttk.Button(location_frame, text="Update Location", command=dummy_function)
update_loc_button.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=tk.E)

# Create the satellite frame
satellite_frame = ttk.LabelFrame(main_frame, text="Satellite Selection", padding="10")
satellite_frame.pack(fill=tk.X, pady=10)

# Row 0-1: Satellite entries
ttk.Label(satellite_frame, text="Satellite 1:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
sat1_var = tk.StringVar(value="NOAA 19")
sat1_entry = ttk.Entry(satellite_frame, textvariable=sat1_var, width=20)
sat1_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(satellite_frame, text="Satellite 2:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
sat2_var = tk.StringVar(value="METOP-C")
sat2_entry = ttk.Entry(satellite_frame, textvariable=sat2_var, width=20)
sat2_entry.grid(row=1, column=1, padx=5, pady=5)

# Row 2: Update Satellites button
update_sat_button = ttk.Button(satellite_frame, text="Update Satellites", command=dummy_function)
update_sat_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.E)

# Row 3: Min elevation entry
ttk.Label(satellite_frame, text="Min Elevation (°):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
min_elev_var = tk.StringVar(value="20")
min_elev_entry = ttk.Entry(satellite_frame, textvariable=min_elev_var, width=5)
min_elev_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

# Row 4: Update Min Elevation button
update_min_elev_button = ttk.Button(satellite_frame, text="Update Min Elevation", command=dummy_function)
update_min_elev_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.E)

# Create the buttons frame
buttons_frame = ttk.Frame(main_frame)
buttons_frame.pack(fill=tk.X, pady=10)

# Create a grid for buttons
button_grid = ttk.Frame(buttons_frame)
button_grid.pack(pady=10)

download_button = ttk.Button(button_grid, text="Download TLE", command=dummy_function)
download_button.grid(row=0, column=0, padx=10, pady=5)

verify_button = ttk.Button(button_grid, text="Verify Satellites", command=dummy_function)
verify_button.grid(row=0, column=1, padx=10, pady=5)

# Functions to launch the applications
def launch_eztrack():
    """Function to launch eztrack.py"""
    try:
        # Update status
        status_var.set("Launching EZ-Trak...")
        root.update()
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Build the full path to eztrack.py
        eztrack_path = os.path.join(script_dir, 'eztrack.py')
        
        # Check if the file exists
        if not os.path.exists(eztrack_path):
            status_var.set(f"Error: Cannot find {eztrack_path}")
            return
        
        # Determine the Python executable to use
        python_exe = sys.executable
        
        # Launch the subprocess
        subprocess.Popen([python_exe, eztrack_path])
        
        # Update status
        status_var.set("EZ-Trak launched successfully")
    except Exception as e:
        status_var.set(f"Error launching EZ-Trak: {str(e)}")

def launch_eztrackrotator():
    """Function to launch eztrackrotator.py"""
    try:
        # Update status
        status_var.set("Launching EZ-Trak Rotator...")
        root.update()
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Build the full path to eztrackrotator.py
        eztrackrotator_path = os.path.join(script_dir, 'eztrackrotator.py')
        
        # Check if the file exists
        if not os.path.exists(eztrackrotator_path):
            status_var.set(f"Error: Cannot find {eztrackrotator_path}")
            return
        
        # Determine the Python executable to use
        python_exe = sys.executable
        
        # Launch the subprocess
        subprocess.Popen([python_exe, eztrackrotator_path])
        
        # Update status
        status_var.set("EZ-Trak Rotator launched successfully")
    except Exception as e:
        status_var.set(f"Error launching EZ-Trak Rotator: {str(e)}")

# Launch buttons in a separate frame
launch_frame = ttk.LabelFrame(main_frame, text="Launch Applications", padding="10")
launch_frame.pack(fill=tk.X, pady=10)

launch_eztrack_button = ttk.Button(launch_frame, text="Launch EZ-Trak", command=launch_eztrack)
launch_eztrack_button.pack(fill=tk.X, pady=5)

launch_rotator_button = ttk.Button(launch_frame, text="Launch EZ-Trak Rotator", command=launch_eztrackrotator)
launch_rotator_button.pack(fill=tk.X, pady=5)

# Status bar at the bottom
status_frame = ttk.Frame(main_frame)
status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

status_var = tk.StringVar(value="Ready")
status_bar = ttk.Label(status_frame, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(fill=tk.X)

# Set default values for location (without loading from file)
lat_var.set("01.2345")
lon_var.set("-01.2345")
alt_var.set("00")

# Run the application
root.mainloop()