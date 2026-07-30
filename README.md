<h2 align="center"><em><code>NDVI Mapping</code></em></h2>
<p align="center">
  Flight telemetry acquisition and multi-sensor environmental monitoring system built for the NASA TechRise / WorldView payload platform.
</p>

## Overview

**NDVI Mapping** is an embedded data acquisition system designed to collect, process, and store real-time flight and environmental measurements during a payload mission.

The system integrates **WorldView flight telemetry** with multiple external sensors to record GPS data, atmospheric conditions, spectral measurements, illumination levels, and inertial motion. All measurements are logged to an onboard SD card in a structured CSV format for post-flight analysis.

The payload automatically tracks flight phases, monitors sensor availability, handles hardware failures gracefully, and provides visual status feedback through onboard LEDs.
