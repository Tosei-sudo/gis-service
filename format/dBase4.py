import struct
from datetime import datetime as dt

from cls.common import RecordsClass

def bcd2dec(value):
    return_value = 0
    minus = False
    for i in range(len(value)):
        if value[i] == "-":
            minus = True
            continue
        return_value += int(value[i]) * (10 ** (len(value) - i - 1))
    if minus:
        return_value *= -1
    return return_value

def dec2bcd(value):
    return_value = bytearray()
    str_value = str(value)
    for i in range(len(str_value)):
        return_value.extend([ord(str_value[i])])
    return return_value

class dBaseFields(RecordsClass):
    END_SIGN = b'\r'
    def create(self, properties_list):
        self.records = []
        fields = {}
        keys = properties_list[0].keys()
        for properties in properties_list:
            for key in keys:
                if key == 'deleted':
                    continue
                if key not in fields:
                    fields[key] = dBaseField()
                    if type(properties[key]) == int:
                        fields[key].create(key, 'N', 0)
                    else:
                        fields[key].create(key, 'C', 0)
                fields[key].length = max(fields[key].length, len(str(properties[key])))
        for key in keys:
            if key == 'deleted':
                continue
            self.records.append(fields[key])
    
    def read(self, file):
        self.records = []
        while True:
            field = dBaseField()
            field.read(file)
            self.records.append(field)
            if file.next() == self.END_SIGN:
                file.read(1)
                break

class dBaseField:
    def create(self, name, type_chr, length):
        self.name = name
        self.type = type_chr
        self.length = length
        self.decimal = 0
    
    def read(self, file):
        self.name = file.read(11).decode('utf-8').split('\x00')[0]
        
        self.type = file.read(1).decode('utf-8')
        file.read(4)

        self.length = int(ord(file.read(1)))
        self.decimal = struct.unpack('<b', file.read(1))[0]
        file.read(14)

    def export(self):
        byte_array = bytearray()
        byte_array += bytes(self.name.ljust(11, b'\x00'))

        byte_array += self.type.encode('utf-8')
        byte_array += b'\x00' * 4

        byte_array += bytes(chr(self.length))
        byte_array += struct.pack('<b', self.decimal)
        byte_array += b'\x00' * 14
        
        return byte_array

class dBaseRecords(RecordsClass):
    END_SIGN = b'\x1A'
    def create(self, properties_list):
        self.records = []
        for properties in properties_list:
            record = dBaseRecord()
            record.create(properties)
            self.records.append(record)
    
    def read(self, file, fields):
        self.records = []
        while True:
            record = dBaseRecord()
            record.read(file, fields)
            self.records.append(record)
            if file.next() == self.END_SIGN:
                file.read(1)
                break

class dBaseRecord:
    def create(self, properties):
        self.deleted = False
        for key, value in properties.items():
            if key == 'deleted':
                continue
            setattr(self, key, value)
    
    def read(self, file, fields):
        self.deleted = file.read(1) == b'*'
        for field in fields:
            value = file.read(field.length).strip()

            if field.type == 'C':
                value = value.decode('sjis').encode('utf-8')
            elif field.type == 'N':
                value = bcd2dec(value)
            elif field.type == 'F':
                value = bcd2dec(value)

            setattr(self, field.name, value)

    def export(self, fields):
        byte_array = bytearray()
        byte_array += b'*' if self.deleted else b' '
        for field in fields:
            value = getattr(self, field.name)
            if field.type == 'C':
                value = value.decode('utf-8').encode('sjis')
                value = value.ljust(field.length, b" ")
            elif field.type == 'N':
                # Convert to BCD
                value = dec2bcd(value)
                value = value.rjust(field.length, chr(32))
            byte_array += value
        return byte_array

class dBaseHeader:
    FILE_CODE = b'\x03'
    def create(self, fields, records):
        new_time = dt.now()
        self.last_update = bytearray([new_time.year - 1900, new_time.month, new_time.day])
        
        self.num_records = len(records)
        
        self.header_length = 32 + 32 * len(fields) + 1
        
        field_length_sum = sum(field.length for field in fields)
        self.record_length = field_length_sum + 1
        
        self.transaction = b'\x00'
        self.encryption = b'\x00'
        self.has_mdx = b'\x00'
        self.language = b'\x13'
    
    def read(self, file):
        self.header = file.read(1)
        
        self.last_update = bytearray(file.read(3))
        
        self.num_records = struct.unpack('<i', file.read(4))[0]
        
        self.header_length = struct.unpack('<h', file.read(2))[0]
        self.record_length = struct.unpack('<h', file.read(2))[0]

        file.read(2)
        self.transaction = file.read(1)
        self.encryption = file.read(1)
        file.read(12)
        
        self.has_mdx = file.read(1)
        self.language = file.read(1)
        file.read(2)
    
    def export(self):
        byte_array = bytearray(self.FILE_CODE)
        byte_array += self.last_update
        byte_array += struct.pack('<i', self.num_records)
        byte_array += struct.pack('<h', self.header_length)
        byte_array += struct.pack('<h', self.record_length)
        byte_array += b'\x00' * 2
        byte_array += self.transaction
        byte_array += self.encryption
        byte_array += b'\x00' * 12
        byte_array += self.has_mdx
        byte_array += self.language
        byte_array += b'\x00' * 2
        return byte_array

class dBase4():
    def create(self, properties_list):
        self.header = dBaseHeader()
        self.fields = dBaseFields()
        self.records = dBaseRecords()
        
        self.fields.create(properties_list)
        self.records.create(properties_list)
        self.header.create(self.fields.records, self.records.records)
    
    def read(self, file):
        self.header = dBaseHeader()
        self.header.read(file)
        
        self.fields = dBaseFields()
        self.fields.read(file)

        self.records = dBaseRecords()
        self.records.read(file, self.fields)
    
    def export(self):
        byte_array = bytearray()
        byte_array += self.header.export()
        byte_array += self.fields.export()
        byte_array += self.records.export(self.fields)

        return byte_array