import struct

from format.Shapefile import ShapeHeader
from cls.common import RecordsClass

class ShapeIndexHeader(ShapeHeader):
    def create(self, shapefile):
        self.file_length = 50 + 4 * len(shapefile.records)
        self.shape_type = shapefile.header.shape_type
        self.mbr = shapefile.header.mbr
        self.z_range = shapefile.header.z_range
        self.m_range = shapefile.header.m_range

class ShapeIndexRecords(RecordsClass):
    def create(self, shapefile):
        self.records = []
        offset = 50
        for record in shapefile.records:
            index_record = ShapeIndexRecord()
            index_record.create(offset, record.header.length)
            self.records.append(index_record)
            offset += record.header.length + 4
        
    def read(self, file):
        self.records = []
        while not file.eof:
            record = ShapeIndexRecord()
            record.read(file)

            self.records.append(record)

    def export(self):
        byte_array = bytearray()
        for record in self.records:
            byte_array += record.export()
        return byte_array

class ShapeIndexRecord():
    def create(self, offset, length):
        self.offset = offset
        self.length = length
    
    def read(self, file):
        self.offset = struct.unpack('>i', file.read(4))[0]
        self.length = struct.unpack('>i', file.read(4))[0]

    def export(self):
        byte_array = bytearray()
        byte_array += struct.pack('>ii', self.offset, self.length)
        return byte_array

class ShapeIndex():
    def create(self, shapefile):
        self.header = ShapeIndexHeader()
        self.header.create(shapefile)
        
        self.records = ShapeIndexRecords()
        self.records.create(shapefile)
    
    def read(self, file):
        self.file = file
        
        self.header = ShapeIndexHeader()
        self.header.read(self.file)
        
        self.records = ShapeIndexRecords()
        self.records.read(self.file)

    def export(self):
        byte_array = self.header.export()
        byte_array += self.records.export()
        return byte_array