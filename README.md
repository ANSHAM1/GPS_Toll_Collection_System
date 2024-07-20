# GPS Based Toll Collection System

## Overview
This project is a vehicle toll tracking system that uses GPS coordinates to determine if a vehicle is on a toll road. The system integrates with a REST API, processes GPS data, and calculates toll fees based on the vehicle's distance traveled on toll roads.

## Project Background
In today's fast-paced world, efficient toll collection is crucial for maintaining smooth traffic flow and reducing congestion at toll booths. Traditional methods like manual toll collection and FASTag have limitations. This project aims to develop an advanced and efficient toll collection system using GPS technology.

## Features
- **Entity Tracking**: Manage vehicle information and track their travel distance.
- **GeoJSON Integration**: Load national highways and toll zones from GeoJSON files.
- **Distance Calculation**: Use the displacement formula for very short change in coordinates and adding them up to get correct distance travelled.
- **Flask Server with Socket.io**: Socket.io keeps the sending of coordinates in loop till the car stops.
- **Toll Calculation**: Calculate toll fees based on the distance traveled

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/ansham1/GPS_Toll_Collection_System.git
    ```
2. Navigate to the project directory:
    ```bash
    cd GPS_Toll_Collection_System
    ```
3. Install the required packages:
    ```bash
    pip install Flask flask_socketio flask_cors eventlet GeoPandas Shapely pymongo
    ```
4. Unzip the zip file present in the `Backend/NH_DATA` folder using an unzipping app like `WinRAR` and copy the geojson file to `Backend/NH_DATA` folder.
5. Navigate to Frontend:
   ```bash
   cd Frontend
   ```
6. Install all modules:
   ```
   npm install
   ```
## How to Run:
1. Navigate to the Root directory:
    ```bash
    cd GPS_Toll_Collection_System
    ```
2. Run the `flask_server.py` script:
    ```bash
    python flask_server.py
    ```
3. Run the GPS.py to send the coordinates:
    ```bash
    python GPS/GPS.py
    ```
3. Open any browser:
   1.For viewing car location and distance travelled
    ```bash
    http://localhost:5000/
    ```
   2.For zones and other info
   ```bash
    http://localhost:5000/car_path
    http://localhost:5000/square_zones
    http://localhost:5000/toll_roads
    ```
