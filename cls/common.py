
class RecordsClass():
    def __len__(self):
        return len(self.records)

    def __iter__(self):
        return iter(self.records)
    
    def __getitem__(self, index):
        return self.records[index]
    
    def export(self, *args):
        byte_array = bytearray()
        for record in self.records:
            byte_array += record.export(*args)
        if hasattr(self, 'END_SIGN'):
            byte_array += self.END_SIGN
        return byte_array