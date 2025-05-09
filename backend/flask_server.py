from ClassOrganizer import Organizer, FileReader # type: ignore
from DBManager import MongoDB # type: ignore

#database connectivity
uri =""
dbName = "GPSBasedTollSimulation"
collection = "Users"

plateNo ='4456'
password ='PASS99@00F4'

MDB = MongoDB()
MDB.connect(uri,dbName,collection)
USER = MDB.retrieveData(plateNo,password)

#Organizer Initialization
ORG = Organizer(plateNo)

#file paths
NH = 'backend/NH_DATA/INDIA_NATIONAL_HIGHWAY.geojson'

#load file data 
FR = FileReader()
NATIONAL_HIGHWAYS = FR.readFile(NH)

# ------------------------------------------------------------------------------------------------------
#defining initial coordinate
PRE_COORD = []

#function for payment reduction from account
def payment():
    global USER, plateNo, password
    TOLL = ORG.returnTotalTolltoDeduct()
    if TOLL==False:
        return "ALL TOLL CLEARED"
    NEW_BALANCE = USER['bankBalance'] - TOLL
    MDB.updateData(plateNo, password, {"plateNo" : ORG.ENTITY.PLATE_NO,"bankBalance" : NEW_BALANCE})

#function for car path detection and validation
def CAR_TRAVELL_DETECTOR(coord):
    global PRE_COORD

    ON_ROAD,DATA = ORG.isEntityOnTollRoad(coord,NATIONAL_HIGHWAYS)
    PRE_ON_ROAD,PRE_DATA = ORG.isEntityOnTollRoad(PRE_COORD,NATIONAL_HIGHWAYS)
    if ON_ROAD:
        print("CAR IS TRAVELLING ON TOLL ROAD")
        if DATA!=PRE_DATA:
            print("...TOLL ROAD CHANGED")
            print("TRAVELLING ON ANOTHER TOLL ROAD....")
            print(PRE_DATA)
            ORG.collectToll(PRE_DATA[0],PRE_DATA[1])
            ORG.ENTITY.COORDINATES.clear()
            ORG.ENTITY.TOTAL_DISTANCE_ON_TOLL_ROAD=0

        ORG.ENTITY.COORDINATES.append(coord)
    else:
        print("CAR IS NOT TRAVELLING ON TOLL ROAD")
        if PRE_ON_ROAD:
            ORG.collectToll(PRE_DATA[0],PRE_DATA[1])
            ORG.ENTITY.COORDINATES.clear()
            ORG.ENTITY.TOTAL_DISTANCE_ON_TOLL_ROAD=0

    PRE_COORD=coord
    return DATA

def ENVOICES_TO_ARRAY():
    ARRAY=[]
    for ROAD in ORG.ENTITY.ROAD_DEPENDENT_TOLLS.keys():
        ARRAY.append([ROAD,f"{ORG.ENTITY.ROAD_DEPENDENT_TOLLS[ROAD][0]:.4f}",f"{ORG.ENTITY.ROAD_DEPENDENT_TOLLS[ROAD][1]:.4f}"])
    return ARRAY

# -------------------------------------------------------------------------------------------------
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/coordinates', methods=['POST'])
def receive_gps():
    global PRE_COORD

    if request.is_json:
        DATA = request.get_json()
        if DATA and 'latitude' in DATA and 'longitude' in DATA:
            latitude = DATA.get('latitude')
            longitude = DATA.get('longitude')

            if PRE_COORD==[]:
                PRE_COORD=[latitude,longitude]

            print(f"Received GPS coordinates: Latitude={latitude}, Longitude={longitude}")
            TOLL_ROAD=CAR_TRAVELL_DETECTOR([latitude,longitude])
            if(TOLL_ROAD==None):
                TOLL_ROAD=[0,"not a toll road"]
            RM = {
                "totalDistance": f"{ORG.ENTITY.TOTAL_DISTANCE:.4f}",
                "tollRoadDistance": f"{ORG.ENTITY.TOTAL_DISTANCE_ON_TOLL_ROAD:.4f}",
                "tollTax": TOLL_ROAD[1],
                "tollRoad": TOLL_ROAD[0]
                }
            
            return jsonify({"DATA":RM}), 200
        else:
            return jsonify({"error": "Invalid coordinates"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400


# @app.route('/end',methods=['GET'])
# def end_gps():
#     PRE_ON_ROAD,PRE_DATA = ORG.isEntityOnTollRoad(PRE_COORD,NATIONAL_HIGHWAYS)
#     if(PRE_ON_ROAD):
#         ORG.collectToll(PRE_DATA[0],PRE_DATA[1])
#         ORG.ENTITY.COORDINATES.clear()
#         ORG.ENTITY.TOTAL_DISTANCE_ON_TOLL_ROAD=0
#     # payment()
#     print(ORG.ENTITY.ROAD_DEPENDENT_TOLLS)
#     MDB.disconnect()
#     ARRAY=ENVOICES_TO_ARRAY()
#     return jsonify({"DATA":ARRAY}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)