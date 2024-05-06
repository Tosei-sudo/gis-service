
from decsvr import DecServer

from router import airport
from router import wfs

server = DecServer.DecServer()
server.incude_router(airport.router)
server.incude_router(wfs.router)

server.start()  