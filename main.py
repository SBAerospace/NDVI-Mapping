#W15 v2
from worldview_lib import *
import time
import sdcardio
import board
import busio
import digitalio
import storage
import adafruit_tsl2591
from adafruit_bme280 import basic as adafruit_bme280
from adafruit_as7343 import AS7343, Channel, Gain, SmuxMode
import adafruit_mpu6050

"""
GO LED Behavior is based on PBF header and data streaming:
* When the PBF header is inserted and data is not streaming = 5 seconds ON, 5 seconds OFF
* When the PBF header is removed and data is not streaming = 1 second ON, 1 second OFF
* When the PBF header is inserted and data is streaming = 3 seconds ON, 3 seconds OFF
* When the PBF header is removed and data is streaming = LED ON (no blinking)

Neopixel Behavior is based on flight status:
* Initializing: Yellow
* Launching: Green
* Floating: Cyan
* Terminating: Blue
* unknown: Gray
"""

# Set up flags
SD_avail = False
I2C_avail = False
TSL_avail = False
BME_avail = False
AS_avail = False
MPU_avail = False

# Set up SD Card
try:
    SD_CS = board.D10  # Use any pin that is not taken by SPI
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    sdcard = sdcardio.SDCard(spi, SD_CS)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    SD_avail = True
except OSError as e:
    print(f"Could not mount SD card: {e}")

# Set up I2C
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    I2C_avail = True
except Exception as e:
    print(f"I2C initialization failed: {e}")

# Set up components on I2C
if I2C_avail:
    try:
        tsl = adafruit_tsl2591.TSL2591(i2c)
        TSL_avail = True
    except Exception as e:
        print(f"Lux sensor initialization failed: {e}")

    try:
        bme = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
        BME_avail = True
    except Exception as e:
        print(f"BME sensor initialization failed: {e}")

    try:
        as7 = AS7343(i2c)
        AS_avail = True
        as7.gain = Gain.X64
        as7.atime = 29
        as7.astep = 599
        as7.smux_mode = SmuxMode.CH18
        as7.wtime = 100
        as7.persistence = 4
        as7.threshold_channel = 0
        as7.spectral_threshold_low = 100
        as7.spectral_threshold_high = 60000
        as7.led_current_ma = 20
    except Exception as e:
        print(f"Color sensor initialization failed: {e}")

    try:
        mpu = adafruit_mpu6050.MPU6050(i2c)
        MPU_avail = True
    except Exception as e:
        print(f"MPU sensor initialization failed: {e}")

def log_exception_to_sd(exception_message):
    if not SD_avail:
        return
    try:
        with open("/sd/error_log.txt", "a") as f:
            f.write(f"{time.monotonic()}: {exception_message}\n")
        print("Exception logged to SD card.")
    except OSError as e:
        print(f"Error writing to SD card log: {e}")

def main():
    num_packets = 0  # Variable for tracking number of full telemetry packets received
    timestamp = time.time()  # Initialize timer for data collection rate
    start_time = time.time()  # Save start time for elapsed time calculation
    endstamp = time.time() + 54000  # Set maximum data collection time at T+15hrs
    phase = "Ground"  # Set initial flight phase
    prev_status = 0  # Initialize variable for tracking phase changes
    wv = Telem()  # Initialize WV data processing

    # 39 columns - must match the 39 values written below
    headers = (
        "Flight Phase, Elapsed Time, Packets, WV Time, WV Latitude, "
        "WV Longitude, WV Altitude, WV Speed, WV Heading, WV Velocity Down, "
        "WV Pressure, WV Temperature, Lux, IR, Visible, Full Spectrum, "
        "BME Temp, BME Rel Hum, BME Pressure, BME Altitude, "
        "Channel F1, Channel F2, Channel FZ, Channel F3, Channel F4, "
        "Channel F5, Channel FY, Channel FXL, Channel F6, Channel F7, "
        "Channel F8, Channel NIR, Acceleration X, Acceleration Y, Acceleration Z, "
        "Gyro X, Gyro Y, Gyro Z, MPU Temp\n"
    )

    # Remember to change the file name to your team number
    if SD_avail:
        try:
            with open("/sd/WORLD_15.txt", "a") as f:
                f.write(headers)
        except Exception as e:
            print(f"An error occurred: {e}")
            log_exception_to_sd(str(e))

    print(headers)
    while True:
        wv.update()  # Update with new data from WV Telemetry
        if wv.new_data:
            num_packets += 1  # If data is new, add 1 to count of telemetry packets received
            data = wv.data
            current_status = wv.status  # Grab current status to track if status has changed
            if current_status != prev_status:  # If status has changed, update flight phase
                if current_status == STATUS_INITIALIZING:
                    phase = "Initializing"
                elif current_status == STATUS_LAUNCHING:
                    phase = "Launching"
                elif current_status == STATUS_FLOATING:
                    phase = "Floating"
                elif current_status == STATUS_TERMINATING:
                    phase = "Terminating"
                prev_status = current_status  # Update the previous status for tracking

            """
            * Uncomment to print out every packet of WV data
            print("New data received:")
            print("Time:", wv.time)
            print("Latitude:", wv.latitude)
            print("Longitude:", wv.longitude)
            print("Altitude:", wv.altitude)
            print("Speed:", wv.speed)
            print("Heading:", wv.heading)
            print("Velocity Down:", wv.velocity_down)
            print("Pressure:", wv.pressure)
            print("Temperature:", wv.temperature)
            print("Flight Status:", wv.status)
            print("PBF State:", "Removed" if wv.pbf else "Inserted")
            print("GO LED State:", "Lit" if wv.go else "Off")
            print("-----------------------------------")
            """
        # If current time is greater than or equal to last timestamp + 1 and current time is less than maximum data collection time
        if time.time() >= (timestamp + 1) and time.time() < endstamp:
            #  COLLECT DATA HERE

            if TSL_avail:
                tlux = tsl.lux
                ir = tsl.infrared
                vs = tsl.visible
                fs = tsl.full_spectrum
            else:
                tlux = ir = vs = fs = "N/A"

            if BME_avail:
                temp = bme.temperature
                rhum = bme.relative_humidity
                pres = bme.pressure
                alt = bme.altitude
            else:
                temp = rhum = pres = alt = "N/A"

            if AS_avail:
                readings = as7.all_channels
                ch_f1 = readings[Channel.F1]
                ch_f2 = readings[Channel.F2]
                ch_fz = readings[Channel.FZ]
                ch_f3 = readings[Channel.F3]
                ch_f4 = readings[Channel.F4]
                ch_f5 = readings[Channel.F5]
                ch_fy = readings[Channel.FY]
                ch_fxl = readings[Channel.FXL]
                ch_f6 = readings[Channel.F6]
                ch_f7 = readings[Channel.F7]
                ch_f8 = readings[Channel.F8]
                ch_nir = readings[Channel.NIR]
            else:
                ch_f1 = ch_f2 = ch_fz = ch_f3 = ch_f4 = ch_f5 = ch_fy = ch_fxl = ch_f6 = ch_f7 = ch_f8 = ch_nir = "N/A"

            if MPU_avail:
                accelX = mpu.acceleration[0]
                accelY = mpu.acceleration[1]
                accelZ = mpu.acceleration[2]
                gyroX = mpu.gyro[0]
                gyroY = mpu.gyro[1]
                gyroZ = mpu.gyro[2]
                mpu_temp = mpu.temperature
            else:
                accelX = accelY = accelZ = gyroX = gyroY = gyroZ = mpu_temp = "N/A"

            elapsed = timestamp - start_time  # Grab elapsed time
            timestamp = time.time()  # Reset timestamp

            # Create a comma separated string with all the data to save (39 fields)
            data_to_save = (
                "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},"
                "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n"
            ).format(
                phase, elapsed, num_packets,
                wv.time, wv.latitude, wv.longitude, wv.altitude, wv.speed, wv.heading,
                wv.velocity_down, wv.pressure, wv.temperature,
                tlux, ir, vs, fs,
                temp, rhum, pres, alt,
                ch_f1, ch_f2, ch_fz, ch_f3, ch_f4, ch_f5, ch_fy, ch_fxl, ch_f6, ch_f7, ch_f8, ch_nir,
                accelX, accelY, accelZ, gyroX, gyroY, gyroZ, mpu_temp
            )

            # Write data to the SD card
            if SD_avail:
                try:
                    with open("/sd/WORLD_15.txt", "a") as f:  # Remember to change the file name to your team number
                        f.write(data_to_save)
                        print("Saving to SD card:", data_to_save)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    log_exception_to_sd(str(e))
            else:
                print(data_to_save)


if __name__ == "__main__":
    main()