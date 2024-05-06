import sqlite3

DB_FOLDER = 'db/'
from cls.feature import Feature
from lib.db import DB

from cls.geometry import Point, Polyline, Polygon, GeometryFileFormat
from cls.dummy import File

from cls.converter import features2geojson

db = DB("airport")

result = db.query("SELECT * FROM outer_circumference")
fs = []

for record in result:

    f = File(record["geometry"])
    p = Polygon()
    p.read(f)
    
    f = Feature(p, {"name": record["name"], "uid": record["uid"]})
    
    fs.append(f)

print features2geojson(fs).get_dict()