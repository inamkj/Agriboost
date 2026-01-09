"""
Test script to check Firebase connection and data fetching.
Run this from the backend directory: python test_firebase.py
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriboost.settings')
django.setup()

from sensors.firebase_service import FirebaseService

print("=" * 60)
print("TESTING FIREBASE CONNECTION")
print("=" * 60)

# Test Firebase initialization
print("\n1. Testing Firebase initialization...")
FirebaseService.initialize()
is_connected = FirebaseService.is_connected()
print(f"   Firebase connected: {is_connected}")

# First, let's explore the Firebase database structure
print("\n2. Exploring Firebase database structure...")
try:
    from firebase_admin import db
    
    # Check root level
    print("\n   Checking root level...")
    root_ref = db.reference('/')
    root_data = root_ref.get()
    if root_data:
        print(f"   Root level keys: {list(root_data.keys()) if isinstance(root_data, dict) else 'Not a dict'}")
        if isinstance(root_data, dict):
            for key in root_data.keys():
                print(f"      - {key}: {type(root_data[key])}")
    
    # Check /sensors path
    print("\n   Checking /sensors path...")
    sensors_ref = db.reference('/sensors')
    sensors_data = sensors_ref.get()
    if sensors_data:
        print(f"   Found data at /sensors!")
        print(f"   Type: {type(sensors_data)}")
        if isinstance(sensors_data, dict):
            print(f"   Keys: {list(sensors_data.keys())}")
            print(f"   First few items:")
            for i, (key, value) in enumerate(list(sensors_data.items())[:10]):
                print(f"      {key}: {value} (type: {type(value)})")
        else:
            print(f"   Data: {sensors_data}")
    else:
        print("   No data found at /sensors path")
        
    # Try other common paths
    print("\n   Checking common alternative paths...")
    alt_paths = ['/', '/data', '/Sensor', '/sensor', '/SensorData', '/sensor_data', '/readings']
    for path in alt_paths:
        alt_ref = db.reference(path)
        alt_data = alt_ref.get()
        if alt_data:
            print(f"   Found data at {path}!")
            if isinstance(alt_data, dict):
                print(f"      Keys: {list(alt_data.keys())[:10]}")
    
except Exception as e:
    print(f"   ERROR exploring database: {str(e)}")
    import traceback
    traceback.print_exc()

# Test data fetching
print("\n3. Testing data fetching with service...")
try:
    sensor_data = FirebaseService.get_sensor_readings()
    print(f"   Data source: {sensor_data.get('source')}")
    print(f"   Sensors count: {len(sensor_data.get('sensors', []))}")
    
    if sensor_data.get('sensors') and len(sensor_data['sensors']) > 0:
        first_sensor = sensor_data['sensors'][0]
        print(f"\n   Sensor readings:")
        print(f"     - Temperature: {first_sensor.get('temperature')}")
        print(f"     - Moisture: {first_sensor.get('soil_moisture')}")
        print(f"     - PH: {first_sensor.get('soil_ph')}")
        print(f"     - EC: {first_sensor.get('ec')}")
        print(f"     - Nitrogen: {first_sensor.get('nitrogen')}")
        print(f"     - Phosphorus: {first_sensor.get('phosphorus')}")
        print(f"     - Potassium: {first_sensor.get('potassium')}")
        print(f"     - Last updated: {sensor_data.get('last_updated')}")
    else:
        print("   No sensor data found!")
        
except Exception as e:
    print(f"   ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

