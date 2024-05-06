import struct

class GeometryFileFormat():
    SHAPE_FILE = 0
    GEOJSON = 1
    POINTS = 2

def calculate_mbr(points):
    points_x = [point.x for point in points]
    points_y = [point.y for point in points]
    return [min(points_x), min(points_y), max(points_x), max(points_y)]

class Geometry:
    def create(self):
        return
    
    def read(self, file):
        return

    def export(self):
        return

class Null(Geometry):
    def create(self):
        self.shape_type = 0
    
    def read(self, file):
        self.shape_type = struct.unpack('<i', file.read(4))[0]

    def export(self, format = GeometryFileFormat.SHAPE_FILE):
        if format == GeometryFileFormat.SHAPE_FILE:
            return struct.pack('<i', self.shape_type)
        elif format == GeometryFileFormat.GEOJSON:
            return []

class Point(Geometry, object):
    TYPE_NAME = "Point"
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def create(self, x, y):
        self.shape_type = 1
        self.x = x
        self.y = y
    
    def read(self, file, is_component=False):
        if not is_component:
            self.shape_type = struct.unpack('<i', file.read(4))[0]
        
        self.x = struct.unpack('<d', file.read(8))[0]
        self.y = struct.unpack('<d', file.read(8))[0]

    def export(self, format = GeometryFileFormat.SHAPE_FILE, is_component=False):
        if format == GeometryFileFormat.SHAPE_FILE:
            byte_data = bytearray()
            if not is_component:
                byte_data.extend(struct.pack('<i', self.shape_type))

            byte_data.extend(struct.pack('<dd', self.x, self.y))
            return byte_data
        elif format == GeometryFileFormat.GEOJSON or format == GeometryFileFormat.POINTS:
            return [self.x, self.y]

class Polyline(Geometry, object):
    TYPE_NAME = "LineString"
    
    def create(self, points):
        self.shape_type = 3
        
        self.mbr = calculate_mbr(points)
        
        self.num_parts = 1
        self.num_points = len(points)
        
        self.parts = [0]
        self.points = points
    
    def read(self, file):
        self.shape_type = struct.unpack('<i', file.read(4))[0]
        
        self.mbr = struct.unpack('<dddd', file.read(32))

        self.num_parts = struct.unpack('<i', file.read(4))[0]
        self.num_points = struct.unpack('<i', file.read(4))[0]

        self.parts = []
        for i in range(self.num_parts):
            self.parts.append(struct.unpack('<i', file.read(4))[0])
        
        self.points = []
        for i in range(self.num_points):
            point = Point()
            point.read(file, True)
            self.points.append(point)

    def export(self, format = GeometryFileFormat.SHAPE_FILE):
        if format == GeometryFileFormat.SHAPE_FILE:
            byte_data = bytearray()
            
            byte_data.extend(struct.pack('<i', self.shape_type))
            
            for i in range(4):
                byte_data.extend(struct.pack('<d', self.mbr[i]))
            
            byte_data.extend(struct.pack('<ii', self.num_parts, self.num_points))
            
            for part in self.parts:
                byte_data.extend(struct.pack('<i', part))
            
            for point in self.points:
                byte_data.extend(point.export(is_component = True))

            return byte_data
        elif format == GeometryFileFormat.GEOJSON:
            return [point.export(format) for point in self.points]
        elif format == GeometryFileFormat.POINTS:
            return self.points

class Polygon(Geometry, object):
    TYPE_NAME = "Polygon"
    
    def create(self, rings):
        self.shape_type = 5
        
        points = []
        for ring in rings:
            points.extend(ring)
        
        self.mbr = calculate_mbr(points)
        
        self.num_parts = len(rings)
        self.num_points = len(points)
        
        self.parts = []
        index = 0
        for i in range(self.num_parts):
            self.parts.append(index)
            index += len(rings[i])
            
        self.points = points
    
    def read(self, file):
        self.shape_type = struct.unpack('<i', file.read(4))[0]
        
        self.mbr = struct.unpack('<dddd', file.read(32))

        self.num_parts = struct.unpack('<i', file.read(4))[0]
        self.num_points = struct.unpack('<i', file.read(4))[0]
        
        self.parts = []
        for i in range(self.num_parts):
            self.parts.append(struct.unpack('<i', file.read(4))[0])

        self.points = []
        for i in range(self.num_points):
            point = Point()
            point.read(file, True)
            self.points.append(point)

    def export(self, format = GeometryFileFormat.SHAPE_FILE):
        if format == GeometryFileFormat.SHAPE_FILE:
            byte_data = bytearray()
            
            byte_data.extend(struct.pack('<i', self.shape_type))
                
            for i in range(4):
                byte_data.extend(struct.pack('<d', self.mbr[i]))
            
            byte_data.extend(struct.pack('<ii', self.num_parts, self.num_points))
            
            for part in self.parts:
                byte_data.extend(struct.pack('<i', part))
            
            for point in self.points:
                byte_data.extend(point.export(is_component = True))

            return byte_data
        elif format == GeometryFileFormat.GEOJSON:
            rings = []
            for i in range(self.num_parts):
                start_index = self.parts[i]
                end_index = self.parts[i+1] if i < self.num_parts - 1 else self.num_points
                rings.append([point.export(format) for point in self.points[start_index:end_index]])
            return rings
        elif format == GeometryFileFormat.POINTS:
            return self.points