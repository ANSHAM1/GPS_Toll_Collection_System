# Vehicle Toll Tracking System

## Overview
This project is a vehicle toll tracking system that uses GPS coordinates to determine if a vehicle is on a toll road. The system integrates with a REST API, processes GPS data, and calculates toll fees based on the vehicle's distance traveled on toll roads.

## Project Background
In today's fast-paced world, efficient toll collection is crucial for maintaining smooth traffic flow and reducing congestion at toll booths. Traditional methods like manual toll collection and FASTag have limitations. This project aims to develop an advanced and efficient toll collection system using GPS technology.

## Features
- **Entity Tracking**: Manage vehicle information and track their travel distance.
- **GeoJSON Integration**: Load national highways and toll zones from GeoJSON files.
- **API Integration**: Use the OSRM API to calculate the distance between GPS coordinates.
- **Flask Server**: Receive GPS coordinates via a POST request and process them to check if the vehicle is on a toll road.
- **Toll Calculation**: Calculate toll fees based on the distance traveled.
- **Privacy Concern**: Encrypt and decrypt data on the client and server side.

## GPS
GPS.py mimic the google map which continously send the car current location in form of coordinates to the server.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/ansham1/GPS_Toll_Collection_System.git
    ```
2. Navigate to the project directory:
    ```bash
    cd vehicle-toll-tracking
    ```
3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```bash
    pip install Flask GeoPandas Requests Shapely cryptography pymongo
    ```
5. Unzip the zip file present in the `geo_data` folder using an unzipping app like WinRAR.

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
