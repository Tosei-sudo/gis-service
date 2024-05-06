
from cls.dummy import File

from format.Shapefile import Shapefile
from format.dBase4 import dBase4
from format.ShapeIndex import ShapeIndex

class ShapePackage():
    def __init__(self):
        self.shapefile = Shapefile()
        self.dbf = dBase4()
        self.shx = ShapeIndex()
    
    def read(self, path):
        with open(path + '.shp', 'rb') as f:
            shp_file = File(f.read())

        self.shapefile.read(shp_file)
        
        with open(path + '.dbf', 'rb') as f:
            dbf_file = File(f.read())
        
        self.dbf.read(dbf_file)
        
        with open(path + '.shx', 'rb') as f:
            shx_file = File(f.read())
        
        self.shx.read(shx_file)

    def save(self, path, export_prj = False):
        with open(path + '.shp', 'wb') as f:
            f.write(self.shapefile.export())

        with open(path + '.dbf', 'wb') as f:
            f.write(self.dbf.export())

        with open(path + '.shx', 'wb') as f:
            f.write(self.shx.export())
        
        if export_prj:
            with open(path + '.prj', 'w') as f:
                f.write(self.shapefile.get_prj())
