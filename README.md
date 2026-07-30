<h2 align="center"><em><code>NDVI Mapping</code></em></h2>
<p align="center">
  Flight telemetry acquisition and multi-sensor environmental monitoring system built for the NASA TechRise / WorldView payload platform.
</p>

## Overview

**NDVI Mapping** is an embedded data acquisition system designed to collect, process, and store real-time flight and environmental measurements during a payload mission.

The system integrates **WorldView flight telemetry** with multiple external sensors to record GPS data, atmospheric conditions, spectral measurements, illumination levels, and inertial motion. All measurements are logged to an onboard SD card in a structured CSV format for post-flight analysis.

The payload automatically tracks flight phases, monitors sensor availability, handles hardware failures gracefully, and provides visual status feedback through onboard LEDs.

---

## Features

- 📡 **Real-time WorldView telemetry collection**
  - GPS position
  - Altitude
  - Velocity
  - Heading
  - Pressure
  - Temperature
  - Flight status

- 🌎 **Environmental sensing**
  - Ambient light intensity
  - Infrared radiation
  - Visible light
  - Full-spectrum measurements
  - Temperature
  - Relative humidity
  - Atmospheric pressure
  - Estimated altitude

- 🌈 **Spectral analysis**
  - AS7343 11-channel spectral sensor
  - F1-F8 visible spectrum channels
  - NIR measurements
  - Configurable gain and integration settings

- 🛰️ **Motion tracking**
  - 3-axis acceleration
  - 3-axis gyroscope
  - IMU temperature

- 💾 **Reliable onboard storage**
  - CSV telemetry logging
  - SD card support
  - Automatic error logging

- 🛡️ **Fault-tolerant initialization**
  - Individual sensor availability checks
  - Continues operation if sensors fail
  - Missing sensor values recorded as `"N/A"`

## Hardware Components

| Component | Purpose |
|-----------|---------|
| WorldView Telemetry Module | Flight telemetry and GPS data |
| SD Card Module | Data storage |
| TSL2591 | High-resolution ambient light sensing |
| BME280 | Temperature, humidity, and pressure sensing |
| AS7343 | Spectral analysis |
| MPU6050 | Acceleration and gyroscope measurements |
| Microcontroller | Payload processing and control |

---

## Flight Status Indicators

### Neopixel Status

The onboard Neopixel indicates current mission state:

| Status | Color |
|--------|-------|
| Initializing | Yellow |
| Launching | Green |
| Floating | Cyan |
| Terminating | Blue |
| Unknown | Gray |

---

### GO LED Behavior

The GO LED indicates payload readiness and telemetry streaming:

| Condition | LED Pattern |
|-----------|-------------|
| PBF inserted, no streaming | 5 seconds ON / 5 seconds OFF |
| PBF removed, no streaming | 1 second ON / 1 second OFF |
| PBF inserted, streaming | 3 seconds ON / 3 seconds OFF |
| PBF removed, streaming | Solid ON |

---

## Data Collection

The payload records telemetry once every second and stores measurements in: `/sd/WORLD_15.txt`

The output file contains **39 data fields**:

| Field | Description |
|-------|-------------|
| Flight Phase | Current mission state |
| Elapsed Time | Time since previous sample |
| Packets | Number of telemetry packets received |
| WV Time | WorldView timestamp |
| WV Latitude | GPS latitude |
| WV Longitude | GPS longitude |
| WV Altitude | GPS altitude |
| WV Speed | Ground speed |
| WV Heading | Direction of travel |
| WV Velocity Down | Vertical velocity |
| WV Pressure | Telemetry pressure |
| WV Temperature | Telemetry temperature |
| Lux | Ambient light intensity |
| IR | Infrared light |
| Visible | Visible light |
| Full Spectrum | Total spectrum intensity |
| BME Temp | Environmental temperature |
| BME Humidity | Relative humidity |
| BME Pressure | Atmospheric pressure |
| BME Altitude | Calculated altitude |
| AS7343 Channels | Spectral measurements |
| Acceleration | X/Y/Z acceleration |
| Gyroscope | X/Y/Z rotational velocity |
| MPU Temperature | IMU temperature |

---

## Software Architecture

### Initialization

At startup, the system:

1. Mounts the SD card.
2. Initializes the I2C communication bus.
3. Detects connected sensors.
4. Configures sensor parameters.
5. Begins telemetry collection.

---

### Main Data Loop

During flight:

1. WorldView telemetry is continuously updated.
2. Flight phase changes are detected.
3. Sensor readings are collected every second.
4. Data is formatted into CSV format.
5. Measurements are written to the SD card.
