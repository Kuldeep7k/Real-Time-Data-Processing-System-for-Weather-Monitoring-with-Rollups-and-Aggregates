# config.py
API_KEY = '43a14ac1cde79206013df3f26ebac597'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
INTERVAL = 300  
DB_NAME = 'weather_data.db'

ALERT_THRESHOLDS = {
    'temperature': {
        'value': 35,  # Degrees Celsius
        'consecutive_count': 2  # Number of consecutive updates needed to trigger an alert
    },
    'conditions': ['Rain', 'Storm'] 
}
