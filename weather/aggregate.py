from collections import defaultdict
from weather.database import store_daily_summary
from weather.fetch import fetch_weather_data
from weather.database import store_alert
from weather.conversion import kelvin_to_celsius
import config
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Dictionary to track consecutive breaches for each city
consecutive_breaches = {city: 0 for city in config.CITIES}

def calculate_daily_summary(weather_data):
   
    """
    Calculate daily summaries from weather data.

    Parameters:
        weather_data (list): List of weather data entries, each containing city, timestamp, temperature, condition, wind speed, wind direction, visibility, cloudiness, and timestamp

    Returns:
        None

    Side Effects:
        Stores daily summaries in the database
    """

    summaries = defaultdict(lambda: {
        'temps': [],
        'conditions': [],
        'wind_speeds': [],
        'wind_directions': [],
        'visibilities': [],
        'cloudiness': [],
        'timestamps': []
    })

    for entry in weather_data:
        city = entry['city']
        timestamp = entry['timestamp']

        # Append temperature, condition data, wind data, visibility, cloudiness, and timestamp
        summaries[(city, timestamp.date())]['temps'].append(entry['temp'])
        summaries[(city, timestamp.date())]['conditions'].append(entry['weather_condition'])
        summaries[(city, timestamp.date())]['wind_speeds'].append(entry['wind_speed'])
        summaries[(city, timestamp.date())]['wind_directions'].append(entry['wind_direction'])
        summaries[(city, timestamp.date())]['visibilities'].append(entry['visibility'])
        summaries[(city, timestamp.date())]['cloudiness'].append(entry['cloudiness'])
        summaries[(city, timestamp.date())]['timestamps'].append(timestamp)

    # Calculate averages and store them
    for (city, date), data in summaries.items():
        if data['temps']:  # Only process if there are temperatures
            avg_temp = sum(data['temps']) / len(data['temps'])
            max_temp = max(data['temps'])
            min_temp = min(data['temps'])
            dominant_condition = max(set(data['conditions']), key=data['conditions'].count)  # Find dominant condition

            # Calculate average wind speed, visibility, and cloudiness
            avg_wind_speed = sum(data['wind_speeds']) / len(data['wind_speeds']) if data['wind_speeds'] else 0
            avg_visibility = sum(data['visibilities']) / len(data['visibilities']) if data['visibilities'] else 0
            avg_cloudiness = sum(data['cloudiness']) / len(data['cloudiness']) if data['cloudiness'] else 0

            # Determine the most common wind direction (dominant wind direction)
            dominant_wind_direction = max(set(data['wind_directions']), key=data['wind_directions'].count)

            # Use the first timestamp for the day (or adjust logic if you want another time representation)
            timestamp = data['timestamps'][0]  # Example: Use the earliest timestamp for that day

            # Store the summary in the database with additional fields
            store_daily_summary(
                city, timestamp, avg_temp, max_temp, min_temp, dominant_condition,
                avg_wind_speed, dominant_wind_direction, avg_visibility, avg_cloudiness
            )


def fetch_and_aggregate():
  
    """
    Fetches weather data for each city, converts temperatures from Kelvin to Celsius, checks if the temperature exceeds the threshold, and stores daily summaries and alerts in the database.

    Side Effects:
        Updates the database with daily summaries and alerts
        Logs messages for temperature breaches
    """
    for city in config.CITIES:
        try:
            data = fetch_weather_data(city)
            if data and 'temp' in data:
                # Convert temperature from Kelvin to Celsius
                data['temp'] = kelvin_to_celsius(data['temp'])

                # Check if temperature exceeds the threshold
                if data['temp'] > config.ALERT_THRESHOLDS['temperature']['value']:
                    consecutive_breaches[city] += 1
                    if consecutive_breaches[city] >= config.ALERT_THRESHOLDS['temperature']['consecutive_count']:
                        alert_message = f"Temperature alert in {city}: {data['temp']}°C exceeded the threshold for {config.ALERT_THRESHOLDS['temperature']['consecutive_count']} consecutive updates."
                        logger.warning(alert_message)
                        store_alert(city, alert_message, data['timestamp'])
                else:
                    consecutive_breaches[city] = 0  # Reset if threshold not breached

                # Calculate and store daily summary
                calculate_daily_summary([data])
            else:
                logger.error(f"No temperature data available for {city}.")
        except Exception as e:
            logger.error(f"Error fetching data for {city}: {e}")
