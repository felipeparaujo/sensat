from unittest import mock
from falcon import testing

from sensat.main import application
from sensat.db.repositories import ReadingsRepository


class ReadingsResourceTestCase(testing.TestCase):
    def setUp(self):
        super().setUp()
        self.app = application


@mock.patch.object(ReadingsRepository, "getByBoxIdAndDateRange", autospec=True, return_value=[])
class TestReadingsResource(ReadingsResourceTestCase):
    def test_successful_on_get(self, mocked_readings_repository):
        result = self.simulate_get('/readings/ID/2019-08-08/2019-08-09')
        assert result.status_code == 200

    def test_refuses_invalid_date_range(self, mocked_readings_repository):
        result = self.simulate_get('/readings/ID/2019-08-10/2019-08-09')
        assert result.status_code == 400

    def test_refuses_invalid_start_date_format(self, mocked_readings_repository):
        result = self.simulate_get('/readings/ID/2019-08-10T00:00:00/2019-08-09')
        assert result.status_code == 400

    def test_refuses_invalid_end_date_format(self, mocked_readings_repository):
        result = self.simulate_get('/readings/ID/2019-08-10/2019-08-09T00:00:00')
        assert result.status_code == 400
