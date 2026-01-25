# Autonomous Drone Combat Display System - Deprecated(first working prototype)

![Main Display](static/main.png)


Overview
--------
This project implements a real time combat display and analytics system for tracking autonomous drones during research and testing operations. The system ingests live telemetry data from multiple unmanned platforms, processes it through a Python-based API, and visualizes drone positions and performance metrics via an interactive web interface. This was built for the [Bush Combat Development Complex](https://bcdc.tamus.edu/) in coordination with Corpus Christi's [Autonomy Research Institute](https://www.tamucc.edu/autonomy-research-institute/)

The primary goals of this project were:

- real time situational awareness for autonomous systems
- low latency telemetry ingestion and visualization
- scalable architecture for research and operational experimentation

this system was designed and built from scratch to support autonomy research and operational analysis

Impact
--------
This repository contains the initial prototype that proved the concept. The production system is now being used at the BCDC to [track 4 autonomous UH-60 Blackhawk helicopters](https://bcdc.tamus.edu/press-releases/texas-am-system-to-lead-59-8m-autonomous-helicopter-wildfire-response-initiative/),  for their [ALIAS Project](https://www.darpa.mil/research/programs/aircrew-labor-in-cockpit-automation-system) in conjunction with DARPA.

## Screenshots

### Analytics Dashboard
![Data Page](static/data.png)

### Individual Drone View
![Single Drone Page](static/individual.png)

System Architecture
-------------------

At a high level, the system consists of:

- **Telemetry Ingestion API (Python)**
  receives live telemetry streams from autonomous drones, validates incoming data, and processes updates for downstream visualization

- **Real Time Visualization Frontend**
  interactive web based combat display map showing live drone positions, status, and mission data

- **Analytics and Statistics Dashboard**
  displays per drone performance metrics using live updating graphs to support trend analysis and post test evaluation

Architecture Flow:

    Autonomous Drones
            |
            v
    Python Telemetry API
            |
            v
    Realime Data Pipeline
            |
      +-----+-----+
      |           |
      v           -- v
    Interactive     Analytics and
    Combat Display  Statistics
    Map             Dashboard

Key Features
------------

- real time tracking of multiple autonomous drones
- live geospatial visualization of drone positions
- low latency telemetry updates
- Per drone statistics and performance analytics
- continuously updating graphs and metrics
- modular and extensible system design

Telemetry Data
--------------

The API is designed to ingest structured telemetry data, including but not limited to:

- drone identifier
- latitude, longitude, and altitude
- velocity and heading
- timestamped status updates
- mission or research specific data fields

The system is extensible and can support additional telemetry formats and autonomous platforms with minimal modification.

Technologies Used
-----------------

- **Backend**: Python (REST API, telemetry processing)
- **Frontend**: web based interactive visualization (HTML, JavaSjcript, CSS)
- **Data Visualization**: live updating charts and graphs (Jinja2, Plotly)
- **Networking**: real time data streaming and low latency updates

Use Cases
---------

- monitoring autonomous drone behavior during live testing
- supporting real time situational awareness for research teams
- analyzing performance metrics and trends across multiple platforms
- providing a foundation for future autonomy and command and control visualization tools

# Building(locally) - make sure you have python3 installed!

1. Make dir and git clone
```bash
mkdir -p droneDisplaySystem

cd droneDisplaySystem

git clone https://github.com/AndrewJoshuaFreeman/autonomous-drone-display-system.git

cd autonomous-drone-display-system
```
2. Create and activate virtual environment
```bash
python3 -m venv .venv

#(mac/linux)
source .venv/bin/activate

#(windows cmd)
.venv\Scripts\Activate.ps1
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Start website(user name is admin, password:password123, very secure)
```bash
python3 app.py
#Cmd+Click to go to website
#^C to end
```
5. Send data to website
```bash
#open new side terminal window, then proceed
cd droneDisplaySystem

#activate virtual enviornment in this window too(refer to 2)

cd json_data/

python3 send_data.py
```

6. Check out the pages - refresh if graphs look wonky

Project Status
--------------

This project is intended for research and educational purposes. It is not designed for YOUR production deployment or YOUR operational combat useage, ie make sure that you test everything if you intend to use it.

Further Infomation
----------

This repository contains no classified, sensitive, or restricted information anymore - all sensitive info has been redacted/deleted.
If interested, please contact me, I can answer any of your questions to the best of my ability!
