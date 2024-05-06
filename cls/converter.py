import struct

from cls.geometry import GeometryFileFormat
from cls.geometry import Point, Polyline, Polygon
from cls.dummy import File
from cls.feature import Feature
from format.ShapePackage import ShapePackage
from format.geojson import GeoJson
from format.Shapefile import ShapeTypes

def shapepackage2geojson(shapepackage):
    """
    Convert GeoJSON file to Shapefile
    """
    geojson = GeoJson([])

    for index, record in enumerate(shapepackage.shapefile.records):
        properties = shapepackage.dbf.records[index].__dict__
        geojson.add_feature(record.geometry.export(GeometryFileFormat.GEOJSON), properties, record.geometry.TYPE_NAME)

    return geojson

def __create_geometry__(geojson_geometry):
    if geojson_geometry["type"] == "Point":
        geometry = Point()
        geometry.create(geojson_geometry["coordinates"][0], geojson_geometry["coordinates"][1])
    elif geojson_geometry["type"] == "LineString":
        geometry = Polyline()
        coordinates = []
        for point in geojson_geometry["coordinates"]:
            coordinates.append(Point(point[0], point[1]))
        geometry.create(coordinates)
    elif geojson_geometry["type"] == "Polygon":
        geometry = Polygon()
        rings = []
        for ring in geojson_geometry["coordinates"]:
            coordinates = []
            for point in ring:
                coordinates.append(Point(point[0], point[1]))
            rings.append(coordinates)
        geometry.create(rings)
    return geometry

def geojson2shapepackage(geojson):
    """
    Convert Shapefile to GeoJSON file
    """
    shapepackage = ShapePackage()
    
    properties_list = []
    geometrys = []

    for record in geojson.features:
        if record["geometry"]["type"] == "MultiPolygon":
            for polygon in record["geometry"]["coordinates"]:
                geometrys.append(__create_geometry__({"type": "Polygon", "coordinates": polygon}))
                properties_list.append(record["properties"])
        else:
            geometrys.append(__create_geometry__(record["geometry"]))
            properties_list.append(record["properties"])

    shapepackage.shapefile.create(geometrys)
    shapepackage.dbf.create(properties_list)
    shapepackage.shx.create(shapepackage.shapefile)
    shapepackage.shx

    return shapepackage

def sqlite2features(results):
    fs = []
    for record in results:

        f = File(record["geometry"])
        shape_type = struct.unpack('<i', f.next(4))[0]
        
        if shape_type == ShapeTypes.POINT:
            geometry = Point()
        elif shape_type == ShapeTypes.POLYLINE:
            geometry = Polyline()
        elif shape_type == ShapeTypes.POLYGON:
            geometry = Polygon()
        else:
            raise Exception('Unknown shape type: ' + str(shape_type))
        
        geometry.read(f)
        
        record.pop("geometry")
        f = Feature(geometry, record)
        
        fs.append(f)
    return fs

def geojson2features(geojson):
    features = []

    for record in geojson.features:
        if record["geometry"]["type"] == "MultiPolygon":
            for polygon in record["geometry"]["coordinates"]:
                features.append(Feature(__create_geometry__({"type": "Polygon", "coordinates": polygon}), record["properties"]))   
        else:
            features.append(Feature(__create_geometry__(record["geometry"]), record["properties"]))
    return features

def features2geojson(features):
    geojson = GeoJson([])
    for feature in features:
        geojson.add_feature(feature.geometry.export(GeometryFileFormat.GEOJSON), feature.properties, feature.geometry.TYPE_NAME)
    return geojson