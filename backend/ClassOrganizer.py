from shapely.geometry import Point, LineString
import geopandas as gpd
import json
import math

class Entity:
    def __init__(self, plateNo):
        self.PLATE_NO = plateNo

        self.TOTAL_DISTANCE = 0
        self.TOTAL_DISTANCE_ON_TOLL_ROAD = 0
        self.ROAD_DEPENDENT_TOLLS = {}
        self.PENDING_TOLLS = {}

        self.COORDINATES = CoordinateList(self) 

    def updateDistance(self, previous, current):
        X1,Y1 = previous
        X2,Y2 = current
        DISTANCE = math.sqrt(pow(X1-X2,2)+pow(Y1-Y2,2)) * 100
        self.TOTAL_DISTANCE_ON_TOLL_ROAD += DISTANCE
        self.TOTAL_DISTANCE += DISTANCE

class CoordinateList:
    def __init__(self, entity):
        self.COORDINATES = []
        self.ENTITY = entity

    def append(self, coordinate):
        if self.COORDINATES:
            previous = self.COORDINATES[-1]
            self.ENTITY.updateDistance(previous, coordinate)
        self.COORDINATES.append(coordinate)

    def clear(self):
        self.COORDINATES = []

class Organizer:
    def __init__(self,entity):
        self.ENTITY = Entity(entity)

    def collectToll(self, road, taxRate = 1):
        ROAD_TAX = self.ENTITY.TOTAL_DISTANCE_ON_TOLL_ROAD * taxRate
        if ROAD_TAX != 0:
            if road in self.ENTITY.PENDING_TOLLS:
                self.ENTITY.PENDING_TOLLS[road] += ROAD_TAX
            else:
                self.ENTITY.PENDING_TOLLS[road] = ROAD_TAX

            if road in self.ENTITY.ROAD_DEPENDENT_TOLLS:
                self.ENTITY.PENDING_TOLLS[road][0] += self.ENTITY.TOTAL_DISTANCE_ON_TOLL_ROAD
                self.ENTITY.PENDING_TOLLS[road][1] += ROAD_TAX
            else:
                self.ENTITY.ROAD_DEPENDENT_TOLLS[road] = [self.ENTITY.TOTAL_DISTANCE_ON_TOLL_ROAD,ROAD_TAX]
    
    def returnTotalTolltoDeduct(self):
        PENDING_TOLL = 0
        for ROAD in self.ENTITY.PENDING_TOLLS.keys():
            PENDING_TOLL += self.ENTITY.PENDING_TOLLS[ROAD]
        if PENDING_TOLL != 0:    
            return PENDING_TOLL
        return False
            
    def isEntityOnTollRoad(self, vehiclePosition, nationalHighways, bufferDistanceMeters=5):
        for NAME,TAX_RATE,COORDS in nationalHighways:
            HIGHWAY = LineString(COORDS)
            POINT = Point(vehiclePosition)
            BUFFER = HIGHWAY.buffer(bufferDistanceMeters / 111139)
            if BUFFER.contains(POINT):
                return [True,[NAME,TAX_RATE]]
        return [False,None]


class FileReader:
    @staticmethod
    def readFile(filePath):
        EXTENSION = filePath.split(".")[-1]
        if EXTENSION.lower() == "json":
            DATA=''
            with open(filePath, 'r') as file:
                DATA=json.load(file)
            return FileReader.loadCarPath(DATA)
        elif EXTENSION.lower() == "geojson":
            GDF = gpd.read_file(filePath)
            return FileReader.loadNationalHighways(GDF.iterrows())

    @staticmethod
    def loadNationalHighways(gdfData):
        NH=[]
        for INDEX, ROW in gdfData:
            if ROW.geometry.geom_type == 'LineString':
                HIGHWAY = ROW.geometry
                NH_NO = ROW['NH_No']
                # TAX_RATE = ROW['NH_No']
                NH.append((NH_NO, 2,HIGHWAY))
        return NH
    
    @staticmethod
    def loadCarPath(pathData):
        COORDINATES = pathData['PATH']
        return COORDINATES