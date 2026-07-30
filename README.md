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
