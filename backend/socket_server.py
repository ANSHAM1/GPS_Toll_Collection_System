from ClassOrganizer import Organizer, FileReader # type: ignore
from DBManager import MongoDB # type: ignore
import random
import time

#database connectivity
uri = "enter your mongo db atlas uri and create the below db and collection with proper entries"
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
PATH = random.choice([f'PATH_{x}' for x in range(1,9)])
CP = f"backend/CAR_PATHS/{PATH}.json"

#load file data 
FR = FileReader()
CAR_COORD = FR.readFile(CP)
NATIONAL_HIGHWAYS = FR.readFile(NH)

# ------------------------------------------------------------------------------------------------------
#defining initial coordinate
PRE_COORD = CAR_COORD[0]
#index for iteration
INDEX = 0

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
#flask server with socketio 
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import eventlet

app = Flask(__name__)
CORS(app) 
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    PRE_ON_ROAD,PRE_DATA = ORG.isEntityOnTollRoad(PRE_COORD,NATIONAL_HIGHWAYS)
    if(PRE_ON_ROAD):
        ORG.collectToll(PRE_DATA[0],PRE_DATA[1])
        ORG.ENTITY.COORDINATES.clear()
        ORG.ENTITY.TOTAL_DISTANCE_ON_TOLL_ROAD=0
    payment()
    print(ORG.ENTITY.ROAD_DEPENDENT_TOLLS)
    MDB.disconnect()
    

@socketio.on('message_from_client')
def handle_message_from_client(speed):
    global INDEX,CAR_COORD

    if(INDEX<len(CAR_COORD)):
        CAR_COORD_CLIENT=[CAR_COORD[INDEX][1],CAR_COORD[INDEX][0]]
        TOLL_ROAD=CAR_TRAVELL_DETECTOR(CAR_COORD[INDEX])
        if(TOLL_ROAD==None):
            TOLL_ROAD=[0,"not a toll road"]
        RM = [CAR_COORD_CLIENT,{
            "totalDistance": f"{ORG.ENTITY.TOTAL_DISTANCE:.4f}",
            "tollRoadDistance": f"{ORG.ENTITY.TOTAL_DISTANCE_ON_TOLL_ROAD:.4f}",
            "tollTax": TOLL_ROAD[1],
            "tollRoad": TOLL_ROAD[0]
        }]
        if(INDEX==len(CAR_COORD)-1):
            RM.append("End")
        emit('message_from_server',RM)
    else:
        PRE_ON_ROAD,PRE_DATA = ORG.isEntityOnTollRoad(PRE_COORD,NATIONAL_HIGHWAYS)
        ORG.collectToll(PRE_DATA[0],PRE_DATA[1])
        ORG.ENTITY.COORDINATES.clear()
        ORG.ENTITY.TOTAL_DISTANCE_ON_TOLL_ROAD=0
    INDEX=INDEX+1
    if speed in [x for x in range(1,61)]:
        print(speed)
        time.sleep((61-speed)/10)
    else:
        time.sleep(1)

@socketio.on('message_from_client_for_end')
def handle_message(end):
        ARRAY=ENVOICES_TO_ARRAY()
        payment()
        MDB.disconnect()
        emit('message_from_server_for_envoices',ARRAY)

if __name__ == '__main__':
    socketio.run(app, debug=True) # type: ignore
