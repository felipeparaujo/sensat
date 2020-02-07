import falcon
import aumbry

from sensat.resources import ReadingsResource
from sensat.db.connection import DatabaseConnection
from sensat.config import AppConfig
from sensat.constants import CONFIG_FILE_PATH

application = falcon.API()

config = aumbry.load(
    aumbry.FILE,
    AppConfig,
    {
        'CONFIG_FILE_PATH': CONFIG_FILE_PATH
    }
)

dbConnection = DatabaseConnection(config.db)

readingsResource = ReadingsResource(dbConnection)
application.add_route('/readings/{boxId}/{fromDate}/{toDate}', readingsResource)
