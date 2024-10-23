import unittest
from unittest.mock import patch
from datetime import datetime
import sqlite3
from weather.fetch import fetch_weather_data
from weather.aggregate import calculate_daily_summary
from weather.database import (
    create_db,
    store_daily_summary,
    get_daily_summaries,
    store_alert,
    get_alerts_summaries,
)
from weather.conversion import kelvin_to_celsius
import config

class TestWeatherMonitor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the database once before all tests
        """Initialize the database once before all tests."""
        
        create_db()

    def setUp(self):
        # Prepare common test data
        """
        Prepare common test data and clear the database tables to ensure test isolation.
        The common test data includes:
            - city
            - timestamp
            - avg_temp
            - max_temp
            - min_temp
            - dominant_condition
            - wind_speed
            - wind_direction
            - visibility
            - cloudiness
        """
        self.city = "Delhi"
        self.timestamp = datetime.now()
        self.avg_temp = kelvin_to_celsius(298.15)  
        self.max_temp = kelvin_to_celsius(303.15)  
        self.min_temp = kelvin_to_celsius(293.15)  
        self.dominant_condition = "Clear"
        self.wind_speed = 5.0
        self.wind_direction = "N"
        self.visibility = 10000
        self.cloudiness = 0

        # Clear the database tables to ensure test isolation
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM daily_summary")
        cursor.execute("DELETE FROM alerts")
        conn.commit()
        conn.close()

    @patch('weather.fetch.requests.get')
    def test_fetch_weather_data(self, mock_get):
        # Mock API response
        """
        Test that fetch_weather_data returns expected data and that it can be stored in the database
        properly. The test mocks the API response and verifies that the returned data is correct.
        It then calls calculate_daily_summary and verifies that the summary is stored in the database
        correctly.
        """
        mock_response = {
            'main': {
                'temp': 298.15,  # Kelvin
                'feels_like': 298.15,
                'humidity': 40,
                'pressure': 1012
            },
            'weather': [{'description': 'clear sky'}],
            'wind': {
                'speed': 3.5,
                'deg': 90
            },
            'clouds': {'all': 0},
            'visibility': 10000,
            'dt': 1633024800  
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Fetch weather data
        result = fetch_weather_data(self.city)
        self.assertEqual(result['city'], self.city)
        self.assertAlmostEqual(result['temp'], mock_response['main']['temp'])  

        # Convert 'temp' to Celsius before passing to calculate_daily_summary
        result['temp'] = kelvin_to_celsius(result['temp'])
        calculate_daily_summary([result])

        # Retrieve summaries and validate
        summaries = get_daily_summaries()
        self.assertEqual(len(summaries), 1)  
        self.assertEqual(summaries[0][0], self.city) 
        self.assertAlmostEqual(summaries[0][2], self.avg_temp) 

    def test_store_daily_summary(self):
        """
        Test storing a daily summary

        This test ensures that a daily summary can be stored in the database correctly.
        It first stores a daily summary using the store_daily_summary function and then
        retrieves the summary using get_daily_summaries. It verifies that one summary is
        stored and that the city and average temperature are correct.
        """
        store_daily_summary(
            self.city, self.timestamp, self.avg_temp, self.max_temp,
            self.min_temp, self.dominant_condition, self.wind_speed,
            self.wind_direction, self.visibility, self.cloudiness
        )
        summaries = get_daily_summaries()
        self.assertEqual(len(summaries), 1)
        self.assertEqual(summaries[0][0], self.city) 
        self.assertAlmostEqual(summaries[0][2], self.avg_temp)  

    def test_get_daily_summaries(self):
        """
        Test retrieving daily summaries

        This test ensures that daily summaries can be retrieved from the database correctly.
        It first stores a daily summary using the store_daily_summary function and then
        retrieves the summary using get_daily_summaries. It verifies that a summary is
        stored and that the city is correct.
        """
        store_daily_summary(
            self.city, self.timestamp, self.avg_temp, self.max_temp,
            self.min_temp, self.dominant_condition, self.wind_speed,
            self.wind_direction, self.visibility, self.cloudiness
        )
        summaries = get_daily_summaries()
        self.assertGreater(len(summaries), 0)
        self.assertEqual(summaries[0][0], self.city) 

    def test_store_alert(self):
        """
        Test storing an alert

        This test ensures that an alert can be stored in the database correctly.
        It first stores an alert using the store_alert function and then
        retrieves the alert using get_alerts_summaries. It verifies that one alert is
        stored and that the alert message is correct.
        """
        alert_message = "Test alert"
        store_alert(self.city, alert_message, self.timestamp)
        alerts = get_alerts_summaries()
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0][1], alert_message) 

    def test_get_alerts_summaries(self):
        """
        Test retrieving alerts

        This test ensures that alerts can be retrieved from the database correctly.
        It first stores an alert using the store_alert function and then
        retrieves the alerts using get_alerts_summaries. It verifies that at least
        one alert is stored and that the alert message is correct.
        """
        alert_message = "Test alert"
        store_alert(self.city, alert_message, self.timestamp)
        alerts = get_alerts_summaries()
        self.assertGreater(len(alerts), 0)
        self.assertEqual(alerts[0][1], alert_message) 

    def test_calculate_daily_summary(self):
        """
        Test calculating daily summaries

        This test ensures that daily summaries can be correctly calculated from weather data.
        It first stores some weather data in the database and then
        calculates the daily summary using calculate_daily_summary.
        It verifies that the summary is stored in the database correctly.
        """
        weather_data = [{
            'city': self.city,
            'temp': self.avg_temp,
            'weather_condition': self.dominant_condition,
            'wind_speed': self.wind_speed,
            'wind_direction': self.wind_direction,
            'visibility': self.visibility,
            'cloudiness': self.cloudiness,
            'timestamp': self.timestamp
        }]
        calculate_daily_summary(weather_data)
        summaries = get_daily_summaries()
        self.assertEqual(len(summaries), 1)
        self.assertAlmostEqual(summaries[0][2], self.avg_temp) 

if __name__ == '__main__':
    unittest.main()
