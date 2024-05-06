import json

class GeoJson():
    def __init__(self, features):
        self.features = features
    
    def read(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.features = data["features"]
    
    def get_dict(self):
        return {
            "type": "FeatureCollection",
            "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
            "features": self.features
        }

    def add_feature(self, feature):
        self.features.append(feature)
    
    def add_feature(self, coords, properties, geo_type = "Polygon"):
        feature = {
            "type": "Feature",
            "geometry": {
                "type": geo_type,
                "coordinates": coords
            },
            "properties": properties
        }
        self.features.append(feature)