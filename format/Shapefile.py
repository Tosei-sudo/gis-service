import struct

from cls.common import RecordsClass
from cls.geometry import Point, Polyline, Polygon, calculate_mbr, GeometryFileFormat

class ShapeTypes:
    NULL = 0
    POINT = 1
    POLYLINE = 3
    POLYGON = 5
    MULTIPOINT = 8
    POINTZ = 11
    POLYLINEZ = 13
    POLYGONZ = 15
    MULTIPOINTZ = 18
    POINTM = 21
    POLYLINEM = 23
    POLYGONM = 25
    MULTIPOINTM = 28
    MULTIPATCH = 31

class ShapeHeader():
    FILE_CODE = b'\x00\x00\x27\x0A'
    def create(self, geometrys):
        self.file_length = 50
        self.version = 1000
        self.shape_type = geometrys[0].shape_type
        
        points = []
        for geometry in geometrys:
            points.extend(geometry.export(GeometryFileFormat.POINTS))
            self.file_length += len(geometry.export())
        self.mbr = calculate_mbr(points)
        self.z_range = (0, 0)
        self.m_range = (0, 0)
    
    def read(self, file):
        self.header = struct.unpack('>i', file.read(4))
        file.read(20) # skip 20 bytes

        self.file_length = struct.unpack('>i', file.read(4))[0]
        self.version = struct.unpack('<i', file.read(4))[0]
        self.shape_type = struct.unpack('<i', file.read(4))[0]

        self.mbr = struct.unpack('<dddd', file.read(32))

        self.z_range = struct.unpack('<dd', file.read(16))

        self.m_range = struct.unpack('<dd', file.read(16))

    def export(self):
        byte_array = bytearray(self.FILE_CODE)
        
        # empty 20 bytes
        byte_array.extend(b'\x00' * 20)
        byte_array += struct.pack('>i', self.file_length)
        # 1000
        byte_array += struct.pack('<i', 1000)

        byte_array += struct.pack('<i', self.shape_type)
        for i in range(4):
            byte_array += struct.pack('<d', self.mbr[i])
        byte_array += struct.pack('<dd', self.z_range[0], self.z_range[1])
        byte_array += struct.pack('<dd', self.m_range[0], self.m_range[1])
        
        return byte_array

class ShapeRecords(RecordsClass):
    def create(self, geometrys):
        self.records = []
        for i, geometry in enumerate(geometrys):
            record = ShapeRecord()
            record.create(i, geometry)
            self.records.append(record)

    def read(self, file):
        self.records = []
        while not file.eof:
            record = ShapeRecord()
            record.read(file)
            self.records.append(record)

    def export(self):
        byte_array = bytearray()
        for record in self.records:
            byte_array += record.export()
        return byte_array

class ShapeRecord():
    def create(self, number, geometry):
        self.header = ShapeRecordHeader()
        self.header.create(number, len(geometry.export()) / 2)
        self.geometry = geometry
    
    def read(self, file):
        self.header = ShapeRecordHeader()
        self.header.read(file)

        shape_type = struct.unpack('<i', file.next(4))[0]

        if shape_type == ShapeTypes.POINT:
            self.geometry = Point()
        elif shape_type == ShapeTypes.POLYLINE:
            self.geometry = Polyline()
        elif shape_type == ShapeTypes.POLYGON:
            self.geometry = Polygon()
        else:
            raise Exception('Unknown shape type: ' + str(shape_type))
        
        self.geometry.read(file)

    def export(self):
        byte_array = self.header.export()
        byte_array += self.geometry.export()
        return byte_array

class ShapeRecordHeader:
    def create(self, number, length):
        self.number = number
        self.length = length
    
    def read(self, file):
        self.number = struct.unpack('>i', file.read(4))[0]
        self.length = struct.unpack('>i', file.read(4))[0]

    def export(self):
        return struct.pack('>ii', self.number, self.length)


class Shapefile:
    def create(self, geometrys):
        self.header = ShapeHeader()
        self.header.create(geometrys)

        self.records = ShapeRecords()
        self.records.create(geometrys)
    
    def get_prj(self):
        return 'GEOGCS["GCS_JGD_2011",DATUM["D_JGD_2011",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
    
    def read(self, file):
        self.file = file
        self.header = ShapeHeader()
        self.header.read(file)

        self.records = ShapeRecords()
        self.records.read(file)
    
    def export(self):
        byte_array = self.header.export()
        byte_array += self.records.export()
        return byte_array