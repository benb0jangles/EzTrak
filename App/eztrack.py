# EZ_TRAK.py
# MIT License
# Copyright (c) 2025 Benb0jangles
# Using a BLE EZ-TRAK connected to a Linux/Windows/Mac computer 
# EZ-TRAK device is available from Benb0jangles sales page

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox, AxesWidget
import numpy as np
from collections import deque

# Configuration
DEVICE_NAME = "EZ-TRAK"  # Device name to search for
ANIMATION_INTERVAL = 50  # Animation update interval in milliseconds

# Default location values
DEFAULT_LAT = 01.234567  # Home
DEFAULT_LON = 0.123456
DEFAULT_ALT = 1337  # meters
MIN_ELEVATION = 30  # minimum elevation in degrees for satellite passes

# Data storage
tracking_points_theta = deque(maxlen=1000)  # Store theta values for tracking line
tracking_points_r = deque(maxlen=1000)  # Store r values for tracking line
is_tracking = False  # Flag to indicate if we're tracking position

# User can edit these three satellites (names from Celestrak database)
USER_SELECTED_SATELLITES = [
    "NOAA 19",
    "METOP-C",
]

# Create figure with modern styling
plt.style.use('ggplot')  # More modern style
fig = plt.figure(figsize=(7, 9))  # Slightly taller to accommodate controls
fig.canvas.manager.set_window_title('EZ-Trak')
# Reorganized grid to move the Next Passes box higher up and add recording controls
grid = plt.GridSpec(8, 4, height_ratios=[0.2, 0.2, 0.1, 0.1, 2.8, 0.8, 0.3, 0.3])

# Location input area (moved to top)
loc_label_ax = fig.add_subplot(grid[0, 0])
loc_label_ax.axis('off')
loc_label_ax.text(0.05, 0.5, "Location:", ha='left', va='center', fontweight='bold')

lat_ax = fig.add_subplot(grid[0, 1])
lat_text = TextBox(lat_ax, 'Lat: ', initial=str(DEFAULT_LAT), color='lightblue', hovercolor='lightgreen')

lon_ax = fig.add_subplot(grid[0, 2])
lon_text = TextBox(lon_ax, 'Lon: ', initial=str(DEFAULT_LON), color='lightblue', hovercolor='lightgreen')

alt_ax = fig.add_subplot(grid[0, 3])
alt_text = TextBox(alt_ax, 'Alt(m): ', initial=str(DEFAULT_ALT), color='lightblue', hovercolor='lightgreen')

# Dummy function for all buttons
def dummy_function(event=None):
    pass

# Button row
update_tle_ax = fig.add_subplot(grid[1, 3])
update_tle_button = Button(update_tle_ax, 'Update TLE', color='lightblue', hovercolor='lightgreen')
update_tle_button.on_clicked(dummy_function)

# Next Pass button
next_pass_button_ax = fig.add_subplot(grid[1, 2])
next_pass_button = Button(next_pass_button_ax, 'Next Pass', color='lightblue', hovercolor='lightgreen')
next_pass_button.on_clicked(dummy_function)

# Status display area
status_ax = fig.add_subplot(grid[1, 0:2])
status_ax.axis('off')
status_text = status_ax.text(0.05, 0.5, "Status: Disconnected", 
                             ha='left', va='center', fontsize=10, fontweight='bold',
                             color='blue', bbox=dict(facecolor='white', alpha=0.8, 
                                                  edgecolor='gray', boxstyle='round,pad=0.5'))

# Reset button moved to bottom row
reset_ax = fig.add_subplot(grid[6, 3])
reset_button = Button(reset_ax, 'Reset Device', color='salmon', hovercolor='red')
reset_button.on_clicked(dummy_function)

# Recording control buttons
record_ax = fig.add_subplot(grid[7, 0:2])
record_button = Button(record_ax, 'Start Recording', color='lightgreen', hovercolor='green')
record_button.on_clicked(dummy_function)

clear_ax = fig.add_subplot(grid[7, 2:4])
clear_button = Button(clear_ax, 'Clear Trace', color='lightcoral', hovercolor='red')
clear_button.on_clicked(dummy_function)

# Create the main circular plot
ax = fig.add_subplot(grid[2:5, :], polar=True)
ax.set_theta_zero_location('N')  # 0 degrees at North
ax.set_theta_direction(-1)  # Clockwise
ax.set_rlim(0, 72)  # Set max radius to 90*0.8 to match our 20% reduction
ax.set_yticklabels([])  # Hide radial ticks

# Add compass labels
ax.set_xticks(np.pi/180. * np.array([0, 90, 180, 270]))
ax.set_xticklabels(['N (0°)', 'E (90°)', 'S (180°)', 'W (270°)'])

# Add concentric circles for elevation - including 0° for the horizon
elevation_circles = [0, 15, 30, 45, 60, 75]
for elevation in elevation_circles:
    # Apply 20% reduction for consistency with other parts of the code
    radius = (90-elevation) * 0.8
    circle = plt.Circle((0, 0), radius, transform=ax.transData._b, 
                       fill=False, edgecolor='gray', alpha=0.5, ls='--')
    ax.add_artist(circle)
    ax.text(0, radius, f"{elevation}°", ha='center', va='bottom',
           bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# Center text for 90° elevation
ax.text(0, 0, "90°", ha='center', va='center',
       bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# Add crosshair (horizontal and vertical lines through the center)
ax.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
ax.axvline(x=0, color='gray', linestyle='-', alpha=0.5)

# Initialize the position marker (red dot for current position)
position_marker, = ax.plot([], [], 'ro', markersize=10)

# Initialize the satellite pass lines
satellite_line, = ax.plot([], [], 'b-', linewidth=2, alpha=0.7)
pass_start_marker, = ax.plot([], [], 'go', markersize=8)
pass_end_marker, = ax.plot([], [], 'yo', markersize=8)

# Initialize the tracking line (red line for tracked positions)
tracking_line, = ax.plot([], [], 'r-', linewidth=2, alpha=0.8)

# Next Pass display area
next_pass_ax = fig.add_subplot(grid[5, 0:2])
next_pass_ax.axis('off')
next_pass_text = next_pass_ax.text(0.05, 0.95, "Next Passes:", 
                             ha='left', va='top', fontsize=10,
                             bbox=dict(facecolor='white', alpha=0.7, 
                                     edgecolor='gray', boxstyle='round,pad=0.5'))

# Current data display area
data_ax = fig.add_subplot(grid[5, 2:])
data_ax.axis('off')
current_text = data_ax.text(0.5, 0.5, "Azimuth: --- Elevation: ---", 
                           ha='center', va='center', fontsize=10,
                           bbox=dict(facecolor='white', alpha=0.7, 
                                   edgecolor='gray', boxstyle='round,pad=0.5'))

# Current pass indicator
current_pass_ax = fig.add_subplot(grid[6, 0:3])
current_pass_ax.axis('off')
current_pass_text = current_pass_ax.text(0.05, 0.5, "Current Pass: ---", 
                                      ha='left', va='center', fontsize=10,
                                      bbox=dict(facecolor='white', alpha=0.7, 
                                              edgecolor='gray', boxstyle='round,pad=0.5'))

# Animation update function - just draws the static elements
def update_animation(frame):
    return position_marker, satellite_line, pass_start_marker, pass_end_marker, tracking_line, status_text, current_text, next_pass_text, current_pass_text

# Set up simple animation
ani = FuncAnimation(fig, update_animation, interval=ANIMATION_INTERVAL, blit=False, cache_frame_data=False)

# Main function just shows the GUI
def main():
    # Show the plot (blocks until window is closed)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()