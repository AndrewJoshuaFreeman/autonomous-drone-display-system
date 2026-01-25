#!/usr/bin/env python3
import os
import json
import time
import random
import datetime
import requests
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path


#config
#local
URL = "http://127.0.0.1:8000/data"

#load environment variables from .env file
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY env variable not set")

HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

#flight paths and callsign
flight_paths = {
    "RELLIS_North_to_Hearne": "RELLIS_NORTH_-_REL→Hearne_converted.xlsx",
    "RELLIS_West_to_Caldwell": "RELLIS_WEST_-_REL_→_Caldwell_converted.xlsx",
    "RELLIS_South_to_AggieFarm": "RELLIS_SOUTH_-_REL_→_AggieFarm_converted.xlsx",
    "Disaster_City_Survey": "Disaster_City_Survey_V2_converted.xlsx"
}

call_sign_map = {
    "RELLIS_North_to_Hearne": "DUSKY18",
    "RELLIS_West_to_Caldwell": "DUSKY21",
    "RELLIS_South_to_AggieFarm": "DUSKY24",
    "Disaster_City_Survey": "DUSKY27"
}

#cardinal direction helper
def get_cardinal(angle):
    """Convert degrees (0–360) to one of 8 cardinal directions."""
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    #each sector is 360/8 = 45°, offset so 0° is centered on 'N'
    idx = int((angle + 22.5) // 45) % 8
    return dirs[idx]

def generate_telemetry_packet(lat, lon, alt, call_sign):
    """Generate a complete telemetry packet with simulated velocity, battery, and orientation."""
    track = round(random.uniform(0, 360), 2)
    
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
            "track": track
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

#load all flight data from .xlsx
flight_data = {}
for flight_name, xlsx in flight_paths.items():
    if not os.path.exists(xlsx):
        print(f"Warning: {xlsx} not found, skipping {flight_name}")
        continue
    
    #load waypoints
    df = (pd.read_excel(xlsx, sheet_name="in")
            [["Latitude", "Longitude", "Altitude"]]
            .dropna()
            .reset_index(drop=True))
    
    flight_data[flight_name] = {
        "waypoints": df,
        "index": 0,
        "call_sign": call_sign_map.get(flight_name, flight_name),
        "complete": False
    }

print(f"Loaded {len(flight_data)} flights")
for name, data in flight_data.items():
    print(f"  {name}: {len(data['waypoints'])} waypoints → {data['call_sign']}")

#main loop: send one packet per second per flight
active_flights = len(flight_data)

while active_flights > 0:
    for flight_name, data in flight_data.items():
        if data["complete"]:
            continue
        
        idx = data["index"]
        waypoints = data["waypoints"]
        
        #check if this flight is finished
        if idx >= len(waypoints):
            data["complete"] = True
            active_flights -= 1
            print(f"\n✓ {flight_name} complete ({len(waypoints)} waypoints sent)\n")
            continue
        
        #get curr waypoint
        row = waypoints.iloc[idx]
        call_sign = data["call_sign"]
        
        #generate tel packet
        packet = generate_telemetry_packet(
            row["Latitude"],
            row["Longitude"],
            row["Altitude"],
            call_sign
        )
        
        #extract heading and compute cardinal
        heading = packet["velocity"]["track"]
        cardinal = get_cardinal(heading)
        
        #print info for our sake
        info = [
            f"{flight_name} [{idx+1}/{len(waypoints)}]",
            f"callsign: {call_sign}",
            f"heading: {heading:.2f}° ({cardinal})"
        ]
        print(" | ".join(info))
        
        #send packet
        try:
            resp = requests.post(URL, headers=HEADERS, json=packet)
            print(f"→ HTTP Status: {resp.status_code}")
        except Exception as e:
            print(f"→ ERROR: {e}")
        
        #move to next waypoint
        data["index"] += 1
    
    #wait 1 second before next round
    time.sleep(1)

print("\n=== All flights complete ===")
