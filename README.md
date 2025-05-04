# EZ-TRAK Satellite Hand Tracking Suite

![EZ-TRAK Logo](images/ez-trak-logo.png)

## Overview

EZ-TRAK is a comprehensive satellite tracking suite designed for amateur radio operators, weather satellite enthusiasts, and educational purposes. The software interfaces with an EZ-TRAK BLE device which is mounted to a lightweight foldable portable satellite dish antenna to hand track satellites in real-time, providing azimuth and elevation data for optimal antenna positioning.

## Features

- **Dynamic Satellite Tracking**: Track satellites in real-time with azimuth/elevation display
- **Pass Prediction**: Calculate upcoming satellite passes for your location
- **BLE Device Integration**: Seamlessly connects to EZ-TRAK BLE device
- **Position Recording**: Record antenna pointing data for later analysis
- **Multi-Source TLE Data**: Download satellite data from Celestrak or SatNOGS DB
- **User-friendly Interface**: Easy-to-use application launcher and configuration tool

## Components

### 1. EZ-TRAK Launcher (`eztrak_welcome.py`)

A graphical interface to configure and launch the main applications:

- Set your geographic location (latitude, longitude, altitude)
- Configure tracked satellites
- Set minimum elevation for valid passes
- Download and verify TLE data
- Launch main tracking applications

### 2. Satellite Tracker (`eztrack.py`)

The main satellite tracking application:

- Visual polar plot showing real-time azimuth/elevation of your hand tracking antenna
- Real-time position display
- Pass prediction information
- Track recording functionality
- Automatic satellite data updates

### 3. Rotator Control (`eztrackrotator.py`)

Optional application for controlling antenna rotators (if available).

## Installation

### Prerequisites

- Python 3.8 or higher
- Bluetooth-enabled computer (Windows, macOS, or Linux)
- EZ-TRAK BLE hardware device

### Required Python Packages

```bash
pip install bleak matplotlib skyfield numpy requests
```

### Installation Steps

1. Clone this repository:
```bash
git clone https://github.com/benb0jangles/EZ-TRAK.git
cd EZ-TRAK
```

2. Run the launcher application:
```bash
python eztrak_welcome.py
```

## Usage

1. **Configure Your Setup**:
   - Enter your latitude, longitude, and altitude
   - Select satellites to track (e.g., "NOAA 19", "METOP-C")
   - Set minimum elevation (typically 20° for good reception)
   - Download current TLE data

2. **Launch Tracking Application**:
   - Click "Launch EZ-TRAK" to start the main tracking application
   - Make sure your EZ-TRAK BLE device is powered on and nearby

3. **Using the Tracker**:
   - The circular display shows azimuth (compass direction) and elevation
   - The red dot shows the current position
   - Blue lines show predicted satellite passes
   - Use recording functionality to track your antenna movement

## Troubleshooting

### Common Issues

- **Device Not Found**: Ensure the EZ-TRAK device is powered on and within range
- **TLE Download Errors**: If Celestrak access is limited, try the SatNOGS data source
- **No Satellite Passes**: Verify your location settings and satellite selection

### Debug Information

The application logs information to the serial console which can be helpful for troubleshooting. Look for messages related to:

- BLE device connection
- Satellite TLE parsing
- Pass prediction calculations

## Hardware

The EZ-TRAK BLE device is available from [Ez-Trak sales page](coming-soon). This compact device:

- Interfaces with Farabrella satellite antenna [Buy a Farabrella here](https://www.ebay.co.uk/itm/204232411345) to provide positional data
- Connects via Bluetooth Low Energy
- Battery-powered for field operation
- Simple button interface for recording and resetting

## Legal Notice

**All Rights Reserved © 2025 Benb0jangles**

This software is proprietary. No permission is granted to copy, distribute, or modify this software without explicit written permission from the author.

This project is provided as-is without any warranty. The software can be used for personal and educational purposes, but redistribution is prohibited.

## Acknowledgments

- Satellite TLE data provided by [Celestrak](https://celestrak.org/) and [SatNOGS](https://db.satnogs.org/)
- Built using [Skyfield](https://rhodesmill.org/skyfield/) for satellite calculations
- Special thanks to the amateur radio and satellite tracking community
