import os
import json
import time
import random
import datetime
import requests
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point
from dotenv import load_dotenv
from pathlib import Path


#config
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY env variable not set")
#for local:
URL = "http://127.0.0.1:8000/data"
HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

#map names to callsigns
call_sign_map = {
    "Disaster_City_Survey":       "DUSKY27",
    "RELLIS_North_to_Hearne":     "DUSKY18",
    "RELLIS_South_to_AggieFarm":  "DUSKY24",
    "RELLIS_West_to_Caldwell":    "DUSKY21"
}

flight_paths = {
    "Disaster_City_Survey":       "Disaster_City_Survey_V2_converted.xlsx",
    "RELLIS_North_to_Hearne":     "RELLIS_NORTH_-_REL→Hearne_converted.xlsx",
    "RELLIS_South_to_AggieFarm":  "RELLIS_SOUTH_-_REL_→_AggieFarm_converted.xlsx",
    "RELLIS_West_to_Caldwell":    "RELLIS_WEST_-_REL_→_Caldwell_converted.xlsx"
}

def generate_telemetry_packet(lat, lon, alt, call_sign):
    """Generate a complete telemetry packet with simulated velocity, battery, and orientation."""
    return {
        "call_sign": call_sign,
        "position": {
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "altitude": round(alt, 6)
        },
        "velocity": {
            "airspeed": round(50.0 + random.uniform(-5, 5), 2),
            "ground_speed": round(50.0 + random.uniform(-5, 5), 2),
            "verticle_speed": round(random.uniform(-0.5, 0.5), 2),
            "units_speed": "MetersPerSecond",
            "track": round(random.uniform(0, 360), 2)
        },
        "time_measured": datetime.datetime.utcnow().isoformat() + "Z",
        "battery": {
            "voltage": round(12.0 + random.uniform(0, 0.6), 2),
            "current": round(1.0 + random.uniform(-0.2, 0.2), 2),
            "percentage": round(random.uniform(80, 100), 2)
        },
        "orientation": {
            "pitch": round(random.uniform(-5, 5), 2),
            "roll": round(random.uniform(-5, 5), 2),
            "yaw": round(random.uniform(0, 360), 2),
            "pitch_rate": round(random.uniform(-1, 1), 2),
            "roll_rate": round(random.uniform(-1, 1), 2),
            "yaw_rate": round(random.uniform(-1, 1), 2)
        },
        "airframe": "Generic"
    }

#process each flight plan
for flight_name, xlsx in flight_paths.items():
    print(f"\n=== Processing {flight_name} ===")
    
    #load waypoints from xlsx
    df = (pd.read_excel(xlsx, sheet_name="in")
            [["Latitude","Longitude","Altitude"]]
            .dropna()
            .reset_index(drop=True))
    
    call_sign = call_sign_map.get(flight_name, flight_name)
    
    #send telemetry for each waypoint
    for idx, row in df.iterrows():
        packet = generate_telemetry_packet(
            row["Latitude"],
            row["Longitude"],
            row["Altitude"],
            call_sign
        )
        
        #post
        resp = requests.post(URL, headers=HEADERS, json=packet)
        print(f"Waypoint {idx+1}/{len(df)}: {call_sign} | HTTP {resp.status_code}")
        
        #wait 1 second before next
        time.sleep(1)
