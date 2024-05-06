
from decsvr import DecServerRouter, ContentType

from cls.converter import features2geojson, sqlite2features

from lib.db import DB

router = DecServerRouter.DecServerRouter()
db = DB("airport", check_same_thread=False)

@router.get('/airport', ContentType.APPLICATION_JSON)
def get_airport(req):

    result = db.query("SELECT * FROM outer_circumference")
    fs = sqlite2features(result)

    return features2geojson(fs).get_dict()