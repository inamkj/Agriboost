"""
Firebase service for fetching sensor readings from Firebase Realtime Database.

This service handles:
- Firebase Admin SDK initialization
- Fetching sensor data from Firebase Realtime Database
- Normalizing sensor payloads to include all required fields
- Generating alerts based on sensor thresholds
- Fallback to placeholder data if Firebase is unavailable

TODO: Add your Firebase Admin SDK credentials to backend/firebase_key.json
      Download the service account key from Firebase Console:
      1. Go to Firebase Console > Project Settings > Service Accounts
      2. Click "Generate New Private Key"
      3. Save the JSON file as backend/firebase_key.json
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from django.conf import settings

# Try to import Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, db
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Warning: firebase-admin not installed. Install it with: pip install firebase-admin")


class FirebaseService:
    """Service for interacting with Firebase Realtime Database."""
    
    _initialized = False
    _firebase_connected = False
    
    @classmethod
    def initialize(cls):
        """
        Initialize Firebase Admin SDK.
        Falls back gracefully if credentials are missing or Firebase is unavailable.
        """
        if not FIREBASE_AVAILABLE:
            print("Firebase Admin SDK not available. Using placeholder data.")
            cls._firebase_connected = False
            cls._initialized = True
            return
        
        if cls._initialized:
            return
        
        try:
            # Get Firebase key file path from settings
            firebase_key_path = getattr(settings, 'FIREBASE_KEY_FILE', None)
            
            if not firebase_key_path or not os.path.exists(firebase_key_path):
                print(f"Firebase key file not found at {firebase_key_path}. Using placeholder data.")
                cls._firebase_connected = False
                cls._initialized = True
                return
            
            # Check if the key file is empty or just contains {}
            try:
                with open(firebase_key_path, 'r') as f:
                    key_content = json.load(f)
                    if not key_content or key_content == {}:
                        print("Firebase key file is empty. Using placeholder data.")
                        cls._firebase_connected = False
                        cls._initialized = True
                        return
            except (json.JSONDecodeError, ValueError):
                print("Firebase key file is invalid. Using placeholder data.")
                cls._firebase_connected = False
                cls._initialized = True
                return
            
            # Initialize Firebase Admin SDK
            # Check if Firebase app is already initialized to avoid re-initialization errors
            try:
                # Try to get existing app - if it doesn't exist, this will raise ValueError
                firebase_admin.get_app()
                # If we get here, app is already initialized
                cls._firebase_connected = True
                cls._initialized = True
                print("Firebase already initialized.")
            except ValueError:
                # App doesn't exist, so initialize it
                cred = credentials.Certificate(firebase_key_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': getattr(settings, 'FIREBASE_DATABASE_URL', 
                                          'https://agriboost-fyp-default-rtdb.firebaseio.com/')
                })
                
                cls._firebase_connected = True
                cls._initialized = True
                print("Firebase initialized successfully.")
            
        except Exception as e:
            print(f"Error initializing Firebase: {str(e)}. Using placeholder data.")
            cls._firebase_connected = False
            cls._initialized = True
    
    @classmethod
    def is_connected(cls) -> bool:
        """Check if Firebase is successfully connected."""
        if not cls._initialized:
            cls.initialize()
        return cls._firebase_connected
    
    @staticmethod
    def normalize_sensor_data(raw_data: Optional[Dict]) -> Dict:
        """
        Normalize sensor data to include all required fields.
        
        Args:
            raw_data: Raw sensor data dictionary from Firebase (may have missing fields)
        
        Returns:
            Normalized dictionary with all required sensor fields
        """
        if not raw_data:
            raw_data = {}
        
        # Helper function to safely convert to float with fallback
        # Handles string values from Firebase (since Firebase stores numbers as strings sometimes)
        def safe_float(value, default=0.0):
            """Safely convert value to float, returning default if conversion fails.
            Handles string values from Firebase database."""
            if value is None:
                return default
            try:
                # Convert to string first to handle any type, then to float
                if isinstance(value, str):
                    # Remove any whitespace
                    value = value.strip()
                    # Handle empty strings
                    if value == '':
                        return default
                return float(value)
            except (ValueError, TypeError):
                print(f"WARNING: Could not convert value '{value}' (type: {type(value)}) to float. Using default {default}")
                return default
        
        # Extract values from raw data, providing defaults if missing
        # Handle different possible field names from Firebase
        # IMPORTANT: Check for None explicitly to allow zero (0) values
        # Note: User's Firebase has: temperature, Moisture, PH, EC, Potassium, Phosphorous, Nitrogen
        
        # Helper to get value from multiple possible keys, allowing zero values
        def get_value(keys, default=None):
            """Get value from dict using multiple possible keys, allowing zero values."""
            for key in keys:
                if key in raw_data and raw_data[key] is not None:
                    return raw_data[key]
            return default
        
        label = get_value(['label', 'name', 'sensor_name'], 'NPK Sensor')
        
        # Temperature in Celsius - handle typo "temprature" (missing 'a') from Firebase
        # FIXED: Now correctly handles zero (0) values
        temp_val = get_value(['temprature', 'temperature', 'Temperature', 'temp', 'Temp'])
        temperature = safe_float(temp_val, 25.0)
        
        # Humidity as percentage (optional field, not in user's 7 variables)
        # FIXED: Now correctly handles zero (0) values
        hum_val = get_value(['humidity', 'Humidity', 'hum', 'Hum'])
        humidity = safe_float(hum_val, 60.0)
        
        # Soil moisture as percentage - maps from "Moisture" in Firebase
        # FIXED: Now correctly handles zero (0) values
        moisture_val = get_value(['Moisture', 'moisture', 'soil_moisture', 'soilMoisture'])
        soil_moisture = safe_float(moisture_val, 50.0)
        
        # Soil pH - maps from "PH" in Firebase (note: user uses "PH" not "pH")
        # FIXED: Now correctly handles zero (0) values
        ph_val = get_value(['PH', 'ph', 'pH', 'soil_ph', 'soilPh'])
        soil_ph = safe_float(ph_val, 6.5)
        
        # Electrical Conductivity (EC) - direct match from Firebase
        # FIXED: Now correctly handles zero (0) values
        ec_val = get_value(['EC', 'ec', 'electrical_conductivity'])
        ec = safe_float(ec_val, 1.5)
        
        # NPK values - maps from user's Firebase field names
        # Nitrogen - direct match
        # FIXED: Now correctly handles zero (0) values
        nitrogen_val = get_value(['Nitrogen', 'nitrogen', 'N'])
        nitrogen = safe_float(nitrogen_val, 50.0)
        
        # Phosphorus - maps from "Phosphorous" (note: user spelled it "Phosphorous")
        # FIXED: Now correctly handles zero (0) values
        phosphorous_val = get_value(['Phosphorous', 'phosphorous', 'P'])
        phosphorous = safe_float(phosphorous_val, 30.0)
        
        # Potassium - direct match
        # FIXED: Now correctly handles zero (0) values
        potassium_val = get_value(['Potassium', 'potassium', 'K'])
        potassium = safe_float(potassium_val, 40.0)
        
        # Battery level as percentage
        # FIXED: Now correctly handles zero (0) values
        battery_val = get_value(['battery', 'battery_level', 'batteryLevel'])
        battery = safe_float(battery_val, 85.0)
        
        # Timestamp - try to get from data, or use current time
        timestamp_str = raw_data.get('timestamp') or raw_data.get('time') or raw_data.get('updated_at')
        timestamp = datetime.now()  # Default to current time
        
        if timestamp_str:
            try:
                # Try to parse if it's a string
                if isinstance(timestamp_str, str):
                    # Handle ISO format with Z timezone
                    clean_timestamp = timestamp_str.replace('Z', '+00:00')
                    # Try parsing ISO format (Python 3.7+)
                    try:
                        timestamp = datetime.fromisoformat(clean_timestamp)
                    except ValueError:
                        # If ISO parsing fails, try without timezone
                        clean_timestamp = clean_timestamp.split('+')[0].split('Z')[0]
                        try:
                            timestamp = datetime.fromisoformat(clean_timestamp)
                        except ValueError:
                            # If all parsing fails, keep current time
                            timestamp = datetime.now()
                elif isinstance(timestamp_str, (int, float)):
                    # Unix timestamp (seconds since epoch)
                    timestamp = datetime.fromtimestamp(float(timestamp_str))
                elif isinstance(timestamp_str, datetime):
                    # Already a datetime object
                    timestamp = timestamp_str
            except (ValueError, TypeError, OSError):
                # If parsing fails for any reason, use current time
                timestamp = datetime.now()
        
        # Generate alerts based on thresholds
        alerts = []
        if temperature > 40:
            alerts.append(f"High temperature alert: {temperature}°C exceeds 40°C threshold")
        elif temperature < 10:
            alerts.append(f"Low temperature alert: {temperature}°C below 10°C threshold")
        
        if soil_ph < 5:
            alerts.append(f"Low pH alert: {soil_ph} below 5.0 threshold")
        elif soil_ph > 8:
            alerts.append(f"High pH alert: {soil_ph} exceeds 8.0 threshold")
        
        if soil_moisture < 30:
            alerts.append(f"Low soil moisture alert: {soil_moisture}% below 30% threshold")
        
        # Build normalized sensor data dictionary
        normalized_data = {
            'label': label,
            'temperature': round(temperature, 2),
            'humidity': round(humidity, 2),
            'soil_moisture': round(soil_moisture, 2),
            'soil_ph': round(soil_ph, 2),
            'ec': round(ec, 2),
            'nitrogen': round(nitrogen, 2),
            'phosphorous': round(phosphorous, 2),
            'potassium': round(potassium, 2),
            'battery': round(battery, 2),
            'timestamp': timestamp.isoformat(),
            'alerts': alerts
        }
        
        return normalized_data
    
    @classmethod
    def get_sensor_readings(cls) -> Dict:
        """
        Fetch sensor readings from Firebase Realtime Database.
        
        Returns:
            Dictionary containing sensor readings and metadata
        """
        # Initialize Firebase if not already done
        if not cls._initialized:
            cls.initialize()
        
        # If Firebase is not connected, return placeholder data
        if not cls._firebase_connected:
            print("FIREBASE: Not connected. Returning placeholder data.")
            print(f"FIREBASE: Connection status - Initialized: {cls._initialized}, Connected: {cls._firebase_connected}")
            return cls.get_placeholder_data()
        
        try:
            # Get the sensors path from settings
            sensors_path = getattr(settings, 'FIREBASE_SENSORS_PATH', '/sensors')
            
            # First, check what's at the root to understand the structure
            print(f"FIREBASE: Checking root path...")
            root_ref = db.reference('/')
            root_data = root_ref.get()
            if root_data:
                print(f"FIREBASE: Root data keys: {list(root_data.keys()) if isinstance(root_data, dict) else 'Not a dict'}")
            
            # Get reference to the sensors node
            ref = db.reference(sensors_path)
            
            # Fetch data from Firebase - IMPORTANT: This fetches fresh data each time
            print(f"FIREBASE: Fetching from path: {sensors_path}")
            sensor_data = ref.get()
            
            # Debug: Print what we received from Firebase
            print(f"FIREBASE: Received data type: {type(sensor_data)}")
            if sensor_data:
                if isinstance(sensor_data, dict):
                    print(f"FIREBASE: Data keys: {list(sensor_data.keys())}")
                    # Print actual values if it's a direct sensor object
                    if any(key in sensor_data for key in ['temprature', 'temperature', 'Temperature', 'Moisture', 'PH', 'EC', 'Nitrogen', 'Potassium', 'Phosphorous']):
                        print(f"FIREBASE: Direct sensor data found:")
                        for key in ['temprature', 'temperature', 'Temperature', 'Moisture', 'PH', 'EC', 'Nitrogen', 'Potassium', 'Phosphorous']:
                            if key in sensor_data:
                                print(f"  {key} = {sensor_data[key]}")
                else:
                    print(f"FIREBASE: Data is not a dict: {sensor_data}")
            else:
                print("FIREBASE: sensor_data is None or empty")
            
            if not sensor_data:
                print("FIREBASE: No sensor data found. Returning placeholder data.")
                return cls.get_placeholder_data()
            
            # Handle different Firebase data structures
            # Firebase can return: dict, list, or direct sensor object
            if isinstance(sensor_data, list):
                # If it's a list, get the first item
                if len(sensor_data) > 0:
                    raw_data = sensor_data[0] if isinstance(sensor_data[0], dict) else {}
                else:
                    # Empty list - use placeholder
                    return cls.get_placeholder_data()
            elif isinstance(sensor_data, dict):
                # Check if it's a direct sensor reading or nested structure
                # Look for the user's Firebase field names: temprature (typo), Moisture, PH, EC, Potassium, Phosphorous, Nitrogen
                if ('label' in sensor_data or 'temprature' in sensor_data or 'temperature' in sensor_data or 'Temperature' in sensor_data or 
                    'Moisture' in sensor_data or 'PH' in sensor_data or 'EC' in sensor_data or
                    'Nitrogen' in sensor_data or 'Potassium' in sensor_data or 'Phosphorous' in sensor_data):
                    # Direct sensor data object
                    raw_data = sensor_data
                elif len(sensor_data) == 1:
                    # Single sensor in a dict: {sensor_id: {...}}
                    first_key = list(sensor_data.keys())[0]
                    raw_data = sensor_data[first_key] if isinstance(sensor_data[first_key], dict) else {}
                elif len(sensor_data) > 1:
                    # Multiple sensors - get the first one
                    first_key = list(sensor_data.keys())[0]
                    raw_data = sensor_data[first_key] if isinstance(sensor_data[first_key], dict) else {}
                else:
                    # Empty dict
                    return cls.get_placeholder_data()
            else:
                # Unsupported type - use placeholder
                print(f"Unexpected sensor data type: {type(sensor_data)}. Using placeholder data.")
                return cls.get_placeholder_data()
            
            # Ensure raw_data is a dict
            if not isinstance(raw_data, dict):
                raw_data = {}
            
            # Print raw data before normalization
            print(f"FIREBASE: Raw data before normalization: {raw_data}")
            
            # Normalize the sensor data
            normalized_data = cls.normalize_sensor_data(raw_data)
            
            # Print normalized data
            print(f"FIREBASE: Normalized data: temperature={normalized_data.get('temperature')}, moisture={normalized_data.get('soil_moisture')}, PH={normalized_data.get('soil_ph')}")
            
            return {
                'sensors': [normalized_data],
                'last_updated': normalized_data['timestamp'],
                'source': 'firebase'
            }
            
        except Exception as e:
            print(f"Error fetching sensor data from Firebase: {str(e)}")
            return cls.get_placeholder_data()
    
    @staticmethod
    def get_placeholder_data() -> Dict:
        """
        Return placeholder sensor data when Firebase is unavailable.
        
        Returns:
            Dictionary with realistic placeholder sensor readings
        """
        current_time = datetime.now()
        
        placeholder_sensor = {
            'label': 'NPK Sensor',
            'temperature': 28.5,
            'humidity': 65.0,
            'soil_moisture': 55.0,
            'soil_ph': 6.8,
            'ec': 1.8,
            'nitrogen': 45.0,
            'phosphorous': 25.0,
            'potassium': 35.0,
            'battery': 92.0,
            'timestamp': current_time.isoformat(),
            'alerts': []
        }
        
        return {
            'sensors': [placeholder_sensor],
            'last_updated': current_time.isoformat(),
            'source': 'placeholder'
        }

