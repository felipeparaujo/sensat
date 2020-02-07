from datetime import datetime
from sensat.db.connection import DatabaseConnection


class ReadingsRepository:
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def getByBoxIdAndDateRange(
        self,
        boxId: str,
        dateStart: datetime,
        dateEnd: datetime
    ) -> list:
        query = """
            SELECT
                r.box_id as box_id,
                s.id as sensor_id,
                s.name as name,
                s.unit as unit,
                r.reading as reading,
                r.reading_ts as reading_ts
            FROM readings r
            JOIN sensors s ON r.sensor_id = s.id
            WHERE r.box_id = %s AND r.reading_ts >= %s AND r.reading_ts <= %s
            ORDER BY r.reading_ts, s.id ASC
        """

        parameters = (boxId, dateStart, dateEnd)

        return self.connection.fetchAll(query, parameters)
