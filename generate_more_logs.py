import json
from pathlib import Path


DATASET_PATH = Path("data/logs.json")

faults = [
    ("STM32-B01", "2.1.0", "E601", "can_bus", "high", "CAN bus communication lost"),
    ("ESP32-011", "1.5.0", "E602", "imu", "medium", "IMU calibration failed"),
    ("NRF52-22", "3.2.1", "E603", "flash_memory", "high", "flash write operation failed"),
    ("RPI-PICO-12", "1.0.3", "E604", "adc", "medium", "ADC reading outside expected range"),
    ("ARDUINO-MEGA-05", "2.4.0", "E605", "pwm_driver", "high", "PWM driver overheated"),
    ("NODEMCU-30", "2.5.1", "E606", "wifi", "medium", "Wi-Fi connection repeatedly dropped"),
    ("ESP8266-14", "1.9.2", "E607", "gpio", "low", "GPIO pin configuration failed"),
    ("STM32-F4-09", "4.0.0", "E608", "ethernet", "high", "Ethernet link was not established"),
    ("TEENSY-41-03", "1.3.5", "E609", "sd_card", "medium", "SD card could not be mounted"),
    ("ESP32-S3-07", "2.0.4", "E610", "bluetooth", "medium", "Bluetooth pairing failed"),
    ("NRF52-31", "3.4.0", "E611", "accelerometer", "high", "accelerometer returned invalid values"),
    ("RPI-PICO-W-06", "1.2.0", "E612", "rtc", "low", "real-time clock synchronization failed"),
    ("STM32-G0-16", "2.2.3", "E613", "watchdog_timer", "critical", "watchdog reset triggered"),
    ("ESP32-C6-02", "1.1.1", "E614", "power_supply", "critical", "input voltage dropped below limit"),
    ("ARDUINO-NANO-18", "0.8.9", "E615", "display", "low", "OLED display did not respond"),
    ("NODEMCU-44", "2.7.0", "E616", "keypad", "low", "keypad input scan failed"),
    ("STM32-L4-21", "3.0.2", "E617", "motor_controller", "high", "motor controller reported overload"),
    ("ESP32-DEV-33", "1.6.2", "E618", "gyroscope", "medium", "gyroscope data stream stopped"),
    ("RPI-PICO-19", "1.5.4", "E619", "relay", "medium", "relay state did not change"),
    ("TEENSY-40-11", "2.3.1", "E620", "actuator", "high", "actuator movement timeout"),
]

normal_logs = [
    "ESP32-012 firmware 1.5.1 boot completed normally.",
    "STM32-B02 firmware 2.1.1 completed routine health check.",
    "NRF52-23 entered low-power sleep mode successfully.",
    "RPI-PICO-13 Wi-Fi connection established successfully.",
    "ARDUINO-MEGA-06 system clock configured successfully.",
    "NODEMCU-31 sent telemetry packet successfully.",
    "ESP8266-15 restarted normally after scheduled update.",
    "STM32-F4-10 sensor calibration completed successfully.",
    "TEENSY-41-04 firmware update completed without errors.",
    "ESP32-S3-08 all diagnostic checks passed.",
]

review_logs = [
    "Field engineer reported an intermittent fault but recorded no device details.",
    "The unit stopped working sometime during testing; no log was captured.",
    "A customer reported unusual behaviour after several hours of use.",
    "Technician noted a possible hardware problem, but details are missing.",
    "Device became unresponsive according to the test report.",
    "An unknown issue was mentioned in the maintenance notes.",
    "System performance appeared unstable; no error code was available.",
    "A fault was suspected during operation but could not be reproduced.",
    "Operator reported a problem with the controller without further details.",
    "An incomplete report states that the board may have failed.",
]


def main():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        logs = json.load(file)

    if len(logs) != 10:
        print("Stop: logs.json must contain exactly the original 10 logs.")
        print(f"It currently contains {len(logs)} logs.")
        return

    new_logs = []

    for number, fault in enumerate(faults, start=11):
        device, firmware, error, module, severity, message = fault

        new_logs.append(
            {
                "log_id": f"log_{number:03d}",
                "raw_log": (
                    f"[12:{number:02d}:00] {device} FW:{firmware} "
                    f"ERROR {error}: {message}."
                ),
                "expected": {
                    "extraction_status": "extracted",
                    "device_id": device,
                    "firmware_version": firmware,
                    "error_code": error,
                    "affected_module": module,
                    "severity": severity,
                },
            }
        )

    for number, raw_log in enumerate(normal_logs, start=31):
        new_logs.append(
            {
                "log_id": f"log_{number:03d}",
                "raw_log": raw_log,
                "expected": {
                    "extraction_status": "no_relevant_fields"
                },
            }
        )

    for number, raw_log in enumerate(review_logs, start=41):
        new_logs.append(
            {
                "log_id": f"log_{number:03d}",
                "raw_log": raw_log,
                "expected": {
                    "extraction_status": "needs_review"
                },
            }
        )

    logs.extend(new_logs)

    with DATASET_PATH.open("w", encoding="utf-8") as file:
        json.dump(logs, file, indent=2)

    print(f"Added {len(new_logs)} logs.")
    print(f"Dataset total: {len(logs)} logs.")


if __name__ == "__main__":
    main()