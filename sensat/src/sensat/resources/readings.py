import json
import falcon
from datetime import datetime
from sensat.constants import DATE_FORMAT
from sensat.db.repositories import ReadingsRepository
from sensat.db.connection import DatabaseConnection


class ReadingsResource:
    def __init__(self, connection: DatabaseConnection):
        self.repository = ReadingsRepository(connection)

    def on_get(self, request, response, boxId, fromDate, toDate):
        try:
            startDate = datetime.strptime(fromDate, DATE_FORMAT)
        except Exception:
            raise falcon.HTTPBadRequest(
                f"Invalidate date format {fromDate}. Acceptable format is {DATE_FORMAT}"
            )

        try:
            endDate = datetime.strptime(toDate, DATE_FORMAT)
        except Exception:
            raise falcon.HTTPBadRequest(
                f"Invalidate date format {toDate}. Acceptable format is {DATE_FORMAT}"
            )

        if fromDate >= toDate:
            raise falcon.HTTPBadRequest(
                f"Start date ({str(startDate)}) can't be later than end date ({str(endDate)})"
            )

        try:
            readings = self.repository.getByBoxIdAndDateRange(boxId, startDate, endDate)
        except Exception:
            raise falcon.HTTPInternalServerError(
                "An error ocurred when making a request to the database"
            )

        response.body = json.dumps(readings, default=str)
