import csv
import hashlib
import json
import math
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

#---------- Settings ----------
SEED = 42
BATCH_ID = "80001"
SCHEMA_VERSION = "0.1"
NUM_VEHICLES = 10
PINGS_PER_VEHICLE = 10
PING_INTERVALS_s = 30
START_TIME_UTC = datetime(2026, 11, 2, 22, 0, 0, tzinfo=timezone.utc)
DEPOT_LAT = -31.9522
DEPOT_LON = 115.8605
SPEED_LIMITS = [40, 50, 60, 70, 80, 90, 100, 110]

FIELDS = [
    "ping_id", "batch_id", "vehicle_id", "device_id", "driver_id", "timestamp_utc", "lat", "lon", "speed_kmh", "speed_limit_kmh", "ignition_on", 
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

def make_fleet(num_vehicles):
    """Return a dict of vehicles, each with its registered device and driver."""
    fleet = {}
    for i in range(1, num_vehicles + 1):
        vehicle_id = f"VH-{i:03d}"
        fleet[vehicle_id] = {
            "device_id": f"DEV-{1000 + i}",
            "driver_id": f"DRV-{i:03d}",
        }
    return fleet

def move_point(lat, lon, heading_deg, distance_m):
    """Move from (lat, lon) by distance_m metres in direction heading_deg."""
    heading_rad = math.radians(heading_deg)
    delta_lat = distance_m * math.cos(heading_rad) / 111320
    delta_lon = distance_m * math.sin(heading_rad) / (111320 * math.cos(math.radians(lat)))
    return lat + delta_lat, lon + delta_lon
