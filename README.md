# Projectile Motion Simulator

A beautiful and interactive Python application to simulate projectile motion with real-time graphical visualization.

## Features

- **Interactive GUI**: Modern, clean interface with attractive fonts and colors
- **Real-time Animation**: Watch the projectile follow its trajectory in real-time
- **Comprehensive Results**: Displays maximum height, time of flight, and range
- **Customizable Parameters**: Adjust initial velocity, angle, and gravitational acceleration
- **Visual Feedback**: Animated graph showing the complete projectile path

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulator:
```bash
python projectile_simulator.py
```

## How to Use

1. **Enter Parameters**:
   - Initial Velocity (m/s): The starting speed of the projectile
   - Angle of Projection (°): Launch angle between 0 and 90 degrees
   - Gravitational Acceleration (m/s²): Default is 9.8 for Earth

2. **Click "Calculate & Simulate"**: The application will:
   - Calculate the maximum height
   - Calculate the time of flight
   - Calculate the range
   - Animate the projectile motion in real-time

3. **Click "Reset"**: Clear all inputs and start fresh

## Physics Formulas Used

- **Time of Flight**: T = (2 × v × sin(θ)) / g
- **Maximum Height**: H = (v² × sin²(θ)) / (2g)
- **Range**: R = (v² × sin(2θ)) / g
- **Trajectory**: x(t) = v × cos(θ) × t, y(t) = v × sin(θ) × t - 0.5 × g × t²

## Requirements

- Python 3.7+
- tkinter (usually comes with Python)
- matplotlib
- numpy

## Screenshots

The application features:
- Clean, modern UI with professional color scheme
- Real-time animated trajectory
- Clear display of calculated results
- Easy-to-use input controls
