import sqlite3

from cls.converter import geojson2features
from format.geojson import GeoJson

geojson = GeoJson([])
geojson.read('sample.geojson')
features = geojson2features(geojson)

DB_FOLDER = 'db/'

conn = sqlite3.connect(DB_FOLDER + "airport" + '.db')

cursor = conn.cursor()

for c in range(1):
    for feature in features:
        geometry_bin = sqlite3.Binary(feature.geometry.export())

        cursor.execute("INSERT INTO outer_circumference (geometry, name) VALUES (?, ?)", (geometry_bin, "HANEDA"))

conn.commit()