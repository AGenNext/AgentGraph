"""
IoT Database - Devices & Sensors

IoT database:
- Devices, Sensors
- Gateways, Networks
- Measurements, Alerts

Reference:
- MQTT: https://mqtt.org/
- AWS IoT: https://aws.amazon.com/iot/

Schema.org: Thing, Device, PropertyValue

Data Sources:
- AWS IoT Core
- Google Cloud IoT
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class DeviceType(Enum):
    Sensor = "Sensor"
    Actuator = "Actuator"
    Gateway = "Gateway"
    Camera = "Camera"
    Switch = "Switch"


@dataclass
class Device:
    id: str
    name: str
    
    device_type: DeviceType = DeviceType.Sensor
    
    location: str = ""
    
    status: str = "Online"  # Online, Offline
    
    firmware: str = ""
    
    last_seen: str = ""


@dataclass
class Measurement:
    id: str
    device_id: str
    value: float
    unit: str = ""
    timestamp: str = ""


class IoTDatabase:
    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.measurements: Dict[str, Measurement] = {}
    
    def add_device(self, d: Device) -> str:
        self.devices[d.id] = d
        return d.id
    
    def add_measurement(self, m: Measurement) -> str:
        self.measurements[m.id] = m
        return m.id
    
    def stats(self) -> Dict:
        return {"devices": len(self.devices), "measurements": len(self.measurements)}


def main():
    db = IoTDatabase()
    d = Device(id="d1", name="Temp Sensor 1", device_type=DeviceType.Sensor)
    db.add_device(d)
    print(f"Device: {d.name}")
    print(f"Stats: {db.stats()}")


if __name__ == "__main__":
    main()