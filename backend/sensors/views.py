# """
# Django REST API views for sensor data endpoints.

# This module provides API endpoints for fetching live sensor readings
# from Firebase Realtime Database and serving them to the React frontend.
# """

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from .firebase_service import FirebaseService
# from .fertilizer_service import FertilizerPredictionService
# from .models import FertilizerPrediction
# from .serializers import FertilizerPredictionSerializer, FertilizerPredictionCreateSerializer
# import pickle
# import pandas as pd

# model = pickle.load(open("sensors/fertilizer model/classifier1.pkl", "rb"))
# fertilizer_encoder = pickle.load(open("sensors/fertilizer model/fertilizer1.pkl", "rb"))
# soil_encoder = pickle.load(open("sensors/fertilizer model/soil_encoder.pkl", "rb"))
# crop_encoder = pickle.load(open("sensors/fertilizer model/crop_encoder.pkl", "rb"))

# class SensorFeedView(APIView):
#     """
#     API view to fetch live sensor readings from Firebase Realtime Database.
#     Public endpoint - no authentication required for sensor data.
    
#     Endpoint: GET /api/sensors/feed/
    
#     Returns:
#         JSON response with:
#         - sensors: List of sensor readings with all 7-in-1 NPK sensor fields
#         - last_updated: ISO 8601 timestamp of the last update
#         - source: 'firebase' or 'placeholder' indicating data source
    
#     Example response:
#         {
#             "sensors": [{
#                 "label": "NPK Sensor",
#                 "temperature": 28.5,
#                 "humidity": 65.0,
#                 "soil_moisture": 55.0,
#                 "soil_ph": 6.8,
#                 "ec": 1.8,
#                 "nitrogen": 45.0,
#                 "phosphorus": 25.0,
#                 "potassium": 35.0,
#                 "battery": 92.0,
#                 "timestamp": "2024-01-15T10:30:00.000000",
#                 "alerts": []
#             }],
#             "last_updated": "2024-01-15T10:30:00.000000",
#             "source": "firebase"
#         }
#     """
#     permission_classes = [AllowAny]  # Allow unauthenticated access to sensor data
    
#     def get(self, request):
#         """
#         Handle GET requests to fetch sensor readings.
        
#         Returns:
#             Response with sensor data in JSON format
#         """
#         try:
#             # Fetch sensor readings from Firebase service
#             print("=" * 50)
#             print("API REQUEST: Fetching sensor data from Firebase...")
#             sensor_data = FirebaseService.get_sensor_readings()
#             print(f"API RESPONSE: Source = {sensor_data.get('source', 'unknown')}")
#             print(f"API RESPONSE: Sensors count = {len(sensor_data.get('sensors', []))}")
#             if sensor_data.get('sensors') and len(sensor_data['sensors']) > 0:
#                 first_sensor = sensor_data['sensors'][0]
#                 print(f"API RESPONSE: Temperature = {first_sensor.get('temperature')}")
#                 print(f"API RESPONSE: Moisture = {first_sensor.get('soil_moisture')}")
#                 print(f"API RESPONSE: PH = {first_sensor.get('soil_ph')}")
#             print("=" * 50)
            
#             return Response(sensor_data, status=status.HTTP_200_OK)
            
#         except Exception as e:
#             # Return error response if something goes wrong
#             return Response(
#                 {
#                     'error': 'Failed to fetch sensor readings',
#                     'detail': str(e),
#                     'sensors': [],
#                     'last_updated': None,
#                     'source': 'error'
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# class FertilizerPredictView(APIView):
#     """
#     API view to predict fertilizer recommendation based on current sensor readings.
    
#     Endpoint: POST /api/sensors/predict/
    
#     Request body (optional - if not provided, uses current sensor readings):
#         {
#             "temperature": 28.5,
#             "soil_moisture": 55.0,
#             "soil_ph": 6.8,
#             "ec": 1.8,
#             "nitrogen": 45.0,
#             "phosphorus": 25.0,
#             "potassium": 35.0
#         }
    
#     Returns:
#         JSON response with fertilizer recommendation and saved prediction history
#     """
# class FertilizerPredictView(APIView):
#     """
#     API view to predict fertilizer recommendation based on sensor readings.
#     Accepts soil type from frontend dropdown, fixed crop type 'Sugarcane',
#     and numeric sensor data from either frontend or Firebase.
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             # -------------------------------
#             # 1. Get sensor data from frontend or Firebase
#             # -------------------------------
#             if request.data:
#                 serializer = FertilizerPredictionCreateSerializer(data=request.data)
#                 if not serializer.is_valid():
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#                 sensor_data = serializer.validated_data
#                 soil_type = sensor_data.get("soil_type", "Loamy")
#             else:
#                 firebase_data = FirebaseService.get_sensor_readings()
#                 if not firebase_data.get('sensors') or len(firebase_data['sensors']) == 0:
#                     return Response(
#                         {'error': 'No sensor data available. Provide sensor readings or wait for Firebase data.'},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#                 sensor = firebase_data['sensors'][0]
#                 sensor_data = {
#                     'temperature': sensor.get('temperature', 25.0),
#                     'humidity': sensor.get('humidity', 50.0),
#                     'soil_moisture': sensor.get('soil_moisture', 50.0),
#                     'nitrogen': sensor.get('nitrogen', 50.0),
#                     'phosphorus': sensor.get('phosphorus', 30.0),
#                     'potassium': sensor.get('potassium', 40.0)
#                 }
#                 soil_type = "Loamy"  # default if using Firebase

#             # -------------------------------
#             # 2. Prepare data for ML model
#             # -------------------------------
#             # Note: column order must match training
#             data_for_model = pd.DataFrame([{
#                 "Temparature": sensor_data['temperature'],
#                 "Humidity": sensor_data['humidity'],
#                 "Moisture": sensor_data['soil_moisture'],
#                 "Soil_Type": soil_type,
#                 "Crop_Type": "Sugarcane",  # fixed
#                 "Nitrogen": sensor_data['nitrogen'],
#                 "Potassium": sensor_data['potassium'],
#                 "Phosphorous": sensor_data['phosphorus']
#             }])

#             # Encode categorical variables
#             data_for_model["Soil_Type"] = soil_encoder.transform(data_for_model["Soil_Type"])
#             data_for_model["Crop_Type"] = crop_encoder.transform(data_for_model["Crop_Type"])

#             # -------------------------------
#             # 3. Predict fertilizer
#             # -------------------------------
#             pred_encoded = model.predict(data_for_model)[0]
#             fertilizer_name = fertilizer_encoder.inverse_transform([pred_encoded])[0]

#             # -------------------------------
#             # 4. Save prediction to history
#             # -------------------------------
#             fertilizer_prediction = FertilizerPrediction.objects.create(
#                 user=request.user,
#                 temperature=sensor_data['temperature'],
#                 humidity=sensor_data['humidity'],
#                 soil_moisture=sensor_data['soil_moisture'],
#                 nitrogen=sensor_data['nitrogen'],
#                 phosphorus=sensor_data['phosphorus'],
#                 potassium=sensor_data['potassium'],
#                 recommended_fertilizer=fertilizer_name,
#                 fertilizer_amount=None,  # optional
#                 confidence_score=None,   # optional
#                 recommendation_details=f"Predicted using ML model for soil {soil_type} and Sugarcane."
#             )

#             # -------------------------------
#             # 5. Return response
#             # -------------------------------
#             response_data = {
#                 "prediction": {
#                     "recommended_fertilizer": fertilizer_name
#                 },
#                 "prediction_history": FertilizerPredictionSerializer(fertilizer_prediction).data,
#                 "sensor_readings": sensor_data,
#                 "message": "Fertilizer prediction completed and saved to history"
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 {"error": "Failed to predict fertilizer", "detail": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

# class FertilizerHistoryView(APIView):
#     """
#     API view to get fertilizer prediction history for the authenticated user.
    
#     Endpoint: GET /api/sensors/predictions/
    
#     Returns:
#         List of fertilizer prediction history records
#     """
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         """Get prediction history for the current user."""
#         predictions = FertilizerPrediction.objects.filter(user=request.user).order_by('-created_at')
#         serializer = FertilizerPredictionSerializer(predictions, many=True)
#         return Response({
#             'count': predictions.count(),
#             'results': serializer.data
#         }, status=status.HTTP_200_OK)


"""
Django REST API views for sensor data endpoints.

Provides API endpoints for fetching live sensor readings
from Firebase Realtime Database and serving them to the React frontend.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .firebase_service import FirebaseService
from .models import FertilizerPrediction
from .serializers import FertilizerPredictionSerializer, FertilizerPredictionCreateSerializer
import pickle
import pandas as pd

# Load ML model and encoders
model = pickle.load(open("sensors/fertilizer model/classifier1.pkl", "rb"))
fertilizer_encoder = pickle.load(open("sensors/fertilizer model/fertilizer1.pkl", "rb"))
soil_encoder = pickle.load(open("sensors/fertilizer model/soil_encoder.pkl", "rb"))
crop_encoder = pickle.load(open("sensors/fertilizer model/crop_encoder.pkl", "rb"))


class SensorFeedView(APIView):
    """Fetch live sensor readings from Firebase."""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            sensor_data = FirebaseService.get_sensor_readings()
            return Response(sensor_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    'error': 'Failed to fetch sensor readings',
                    'detail': str(e),
                    'sensors': [],
                    'last_updated': None,
                    'source': 'error'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Fertilizer Guide Dictionary - Contains instructions and precautions for all 14 model-predicted fertilizers
FERTILIZER_GUIDE = {
    "Urea": {
        "instructions": (
            "Urea Application Guidelines:\n"
            "• Dosage: Apply 150-200 kg/ha for sugarcane crops.\n"
            "• Timing: Apply before planting or during early growth stages (30-45 days after planting).\n"
            "• Method: Broadcast evenly or place in furrows 10-15 cm deep and cover with soil.\n"
            "• Split Application: Divide into 2-3 doses for better efficiency.\n"
            "• Irrigation: Apply before irrigation or during light rain for better absorption.\n"
            "• Storage: Store in a cool, dry place away from moisture and direct sunlight."
        ),
        "precautions": (
            "Urea Safety Precautions:\n"
            "• Wear protective gloves, goggles, and a mask when handling.\n"
            "• Avoid direct skin contact - wash immediately if exposed.\n"
            "• Do not apply in windy conditions to prevent drift.\n"
            "• Keep away from water sources to prevent contamination.\n"
            "• Do not mix with seeds as it can cause germination issues.\n"
            "• Avoid application during hot, dry weather - can cause leaf burn.\n"
            "• Keep children and animals away from storage and application areas."
        )
    },
    "TSP": {
        "instructions": (
            "TSP (Triple Super Phosphate) Application Guidelines:\n"
            "• Dosage: Apply 150-200 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply as basal dose before planting or during early growth (20-30 days).\n"
            "• Method: Broadcast and incorporate into soil at 8-10 cm depth.\n"
            "• Mixing: Can be mixed with urea or potash fertilizers.\n"
            "• Irrigation: Light irrigation after application enhances phosphorus availability.\n"
            "• Storage: Store in a dry, well-ventilated area away from moisture."
        ),
        "precautions": (
            "TSP Safety Precautions:\n"
            "• Wear protective gloves, safety glasses, and a dust mask.\n"
            "• Avoid inhalation of dust particles during handling.\n"
            "• Do not apply directly to seeds - maintain 2-3 cm separation.\n"
            "• Keep away from water bodies to prevent algal growth.\n"
            "• Store in sealed containers in a dry area.\n"
            "• Wash hands thoroughly after handling."
        )
    },
    "Superphosphate": {
        "instructions": (
            "Superphosphate Application Guidelines:\n"
            "• Dosage: Apply 200-300 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply as basal dose before planting or during early growth stages.\n"
            "• Method: Broadcast evenly and incorporate into soil at 8-10 cm depth.\n"
            "• Compatibility: Can be mixed with other fertilizers like urea.\n"
            "• Irrigation: Apply before irrigation for better nutrient absorption.\n"
            "• Storage: Keep in dry conditions, away from moisture."
        ),
        "precautions": (
            "Superphosphate Safety Precautions:\n"
            "• Use protective equipment: gloves, mask, and safety glasses.\n"
            "• Avoid dust inhalation during application.\n"
            "• Keep away from water sources.\n"
            "• Store in a dry, well-ventilated area.\n"
            "• Do not mix with seeds during planting.\n"
            "• Wash hands after handling."
        )
    },
    "Potassium sulfate": {
        "instructions": (
            "Potassium Sulfate Application Guidelines:\n"
            "• Dosage: Apply 100-150 kg/ha for sugarcane crops.\n"
            "• Timing: Apply before planting or during early to mid-growth stages.\n"
            "• Method: Broadcast evenly and incorporate into soil or apply in bands.\n"
            "• Compatibility: Can be mixed with nitrogen fertilizers.\n"
            "• Irrigation: Ensure adequate irrigation after application.\n"
            "• Split Application: Divide into 2-3 applications for better efficiency."
        ),
        "precautions": (
            "Potassium Sulfate Safety Precautions:\n"
            "• Wear protective gloves and clothing during handling.\n"
            "• Avoid direct contact with skin and eyes.\n"
            "• Do not apply directly to plant leaves - can cause burn.\n"
            "• Store in a dry place, away from moisture.\n"
            "• Keep away from children and pets.\n"
            "• Follow manufacturer's safety guidelines."
        )
    },
    "Potassium chloride": {
        "instructions": (
            "Potassium Chloride (MOP) Application Guidelines:\n"
            "• Dosage: Apply 80-120 kg/ha for sugarcane crops.\n"
            "• Timing: Apply before planting or during early to mid-growth stages.\n"
            "• Method: Broadcast and incorporate into soil or apply in bands.\n"
            "• Compatibility: Can be mixed with other fertilizers like urea.\n"
            "• Irrigation: Ensure adequate irrigation for proper nutrient movement.\n"
            "• Split Application: Apply in 2-3 doses for better efficiency."
        ),
        "precautions": (
            "Potassium Chloride Safety Precautions:\n"
            "• Handle with care - avoid dust inhalation.\n"
            "• Wear gloves and protective clothing during application.\n"
            "• Do not apply directly to plant leaves - can cause burn.\n"
            "• Store in a dry place, away from moisture.\n"
            "• Keep away from children and pets.\n"
            "• Do not mix with seeds during planting."
        )
    },
    "DAP": {
        "instructions": (
            "DAP (Diammonium Phosphate) Application Guidelines:\n"
            "• Dosage: Apply 100-150 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply before planting as basal dose or during early growth (20-30 days).\n"
            "• Method: Place in planting furrows or broadcast and incorporate into soil.\n"
            "• Depth: Apply at 8-10 cm depth for best root access.\n"
            "• Mixing: Can be mixed with urea, but apply separately from seeds.\n"
            "• Irrigation: Light irrigation after application enhances nutrient availability."
        ),
        "precautions": (
            "DAP Safety Precautions:\n"
            "• Wear protective clothing, gloves, and safety glasses.\n"
            "• Avoid inhalation of dust particles - use a dust mask.\n"
            "• Do not apply directly to seeds - maintain 2-3 cm separation.\n"
            "• Keep away from water bodies to prevent algal growth.\n"
            "• Store in sealed containers in a dry, well-ventilated area.\n"
            "• Do not mix with lime or alkaline substances.\n"
            "• Wash hands thoroughly after handling."
        )
    },
    "28-28": {
        "instructions": (
            "28-28 NPK Application Guidelines:\n"
            "• Dosage: Apply 150-200 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply before planting (basal) and during growth stages (30, 60, 90 days).\n"
            "• Method: Broadcast evenly or apply in bands near root zone.\n"
            "• Split Application: Divide total dose into 3-4 applications for optimal results.\n"
            "• Incorporation: Lightly incorporate into soil after application.\n"
            "• Compatibility: Can be used with organic manures for balanced nutrition."
        ),
        "precautions": (
            "28-28 NPK Safety Precautions:\n"
            "• Use protective equipment: gloves, mask, and safety glasses.\n"
            "• Avoid contact with eyes and skin - rinse immediately if exposed.\n"
            "• Do not apply in excessive amounts - can cause nutrient imbalance.\n"
            "• Keep away from water sources to prevent eutrophication.\n"
            "• Store in original packaging, away from moisture and direct sunlight.\n"
            "• Do not mix with incompatible chemicals - check compatibility first.\n"
            "• Follow recommended dosages based on soil test results."
        )
    },
    "20-20": {
        "instructions": (
            "20-20 NPK Application Guidelines:\n"
            "• Dosage: Apply 150-200 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply before planting (basal) and during growth stages (30, 60, 90 days).\n"
            "• Method: Broadcast evenly or apply in bands near root zone.\n"
            "• Split Application: Divide total dose into 3-4 applications for optimal results.\n"
            "• Incorporation: Lightly incorporate into soil after application.\n"
            "• Compatibility: Can be used with organic manures for balanced nutrition."
        ),
        "precautions": (
            "20-20 NPK Safety Precautions:\n"
            "• Use protective equipment: gloves, mask, and safety glasses.\n"
            "• Avoid contact with eyes and skin - rinse immediately if exposed.\n"
            "• Do not apply in excessive amounts - can cause nutrient imbalance.\n"
            "• Keep away from water sources to prevent eutrophication.\n"
            "• Store in original packaging, away from moisture and direct sunlight.\n"
            "• Do not mix with incompatible chemicals - check compatibility first.\n"
            "• Follow recommended dosages based on soil test results."
        )
    },
    "17-17-17": {
        "instructions": (
            "17-17-17 NPK Application Guidelines:\n"
            "• Dosage: Apply 150-200 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply before planting (basal) and during growth stages (30, 60, 90 days).\n"
            "• Method: Broadcast evenly or apply in bands near root zone.\n"
            "• Split Application: Divide total dose into 3-4 applications for optimal results.\n"
            "• Incorporation: Lightly incorporate into soil after application.\n"
            "• Compatibility: Can be used with organic manures for balanced nutrition."
        ),
        "precautions": (
            "17-17-17 NPK Safety Precautions:\n"
            "• Use protective equipment: gloves, mask, and safety glasses.\n"
            "• Avoid contact with eyes and skin - rinse immediately if exposed.\n"
            "• Do not apply in excessive amounts - can cause nutrient imbalance.\n"
            "• Keep away from water sources to prevent eutrophication.\n"
            "• Store in original packaging, away from moisture and direct sunlight.\n"
            "• Do not mix with incompatible chemicals - check compatibility first.\n"
            "• Follow recommended dosages based on soil test results."
        )
    },
    "15-15-15": {
        "instructions": (
            "15-15-15 NPK Application Guidelines:\n"
            "• Dosage: Apply 150-200 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply before planting (basal) and during growth stages (30, 60, 90 days).\n"
            "• Method: Broadcast evenly or apply in bands near root zone.\n"
            "• Split Application: Divide total dose into 3-4 applications for optimal results.\n"
            "• Incorporation: Lightly incorporate into soil after application.\n"
            "• Compatibility: Can be used with organic manures for balanced nutrition."
        ),
        "precautions": (
            "15-15-15 NPK Safety Precautions:\n"
            "• Use protective equipment: gloves, mask, and safety glasses.\n"
            "• Avoid contact with eyes and skin - rinse immediately if exposed.\n"
            "• Do not apply in excessive amounts - can cause nutrient imbalance.\n"
            "• Keep away from water sources to prevent eutrophication.\n"
            "• Store in original packaging, away from moisture and direct sunlight.\n"
            "• Do not mix with incompatible chemicals - check compatibility first.\n"
            "• Follow recommended dosages based on soil test results."
        )
    },
    "14-35-14": {
        "instructions": (
            "14-35-14 NPK Application Guidelines:\n"
            "• Dosage: Apply 150-200 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply before planting (basal) and during growth stages (30, 60, 90 days).\n"
            "• Method: Broadcast evenly or apply in bands near root zone.\n"
            "• Split Application: Divide total dose into 3-4 applications for optimal results.\n"
            "• Incorporation: Lightly incorporate into soil after application.\n"
            "• Compatibility: Can be used with organic manures for balanced nutrition."
        ),
        "precautions": (
            "14-35-14 NPK Safety Precautions:\n"
            "• Use protective equipment: gloves, mask, and safety glasses.\n"
            "• Avoid contact with eyes and skin - rinse immediately if exposed.\n"
            "• Do not apply in excessive amounts - can cause nutrient imbalance.\n"
            "• Keep away from water sources to prevent eutrophication.\n"
            "• Store in original packaging, away from moisture and direct sunlight.\n"
            "• Do not mix with incompatible chemicals - check compatibility first.\n"
            "• Follow recommended dosages based on soil test results."
        )
    },
    "14-14-14": {
        "instructions": (
            "14-14-14 NPK Application Guidelines:\n"
            "• Dosage: Apply 150-200 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply before planting (basal) and during growth stages (30, 60, 90 days).\n"
            "• Method: Broadcast evenly or apply in bands near root zone.\n"
            "• Split Application: Divide total dose into 3-4 applications for optimal results.\n"
            "• Incorporation: Lightly incorporate into soil after application.\n"
            "• Compatibility: Can be used with organic manures for balanced nutrition."
        ),
        "precautions": (
            "14-14-14 NPK Safety Precautions:\n"
            "• Use protective equipment: gloves, mask, and safety glasses.\n"
            "• Avoid contact with eyes and skin - rinse immediately if exposed.\n"
            "• Do not apply in excessive amounts - can cause nutrient imbalance.\n"
            "• Keep away from water sources to prevent eutrophication.\n"
            "• Store in original packaging, away from moisture and direct sunlight.\n"
            "• Do not mix with incompatible chemicals - check compatibility first.\n"
            "• Follow recommended dosages based on soil test results."
        )
    },
    "10-26-26": {
        "instructions": (
            "10-26-26 NPK Application Guidelines:\n"
            "• Dosage: Apply 150-200 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply before planting (basal) and during growth stages (30, 60, 90 days).\n"
            "• Method: Broadcast evenly or apply in bands near root zone.\n"
            "• Split Application: Divide total dose into 3-4 applications for optimal results.\n"
            "• Incorporation: Lightly incorporate into soil after application.\n"
            "• Compatibility: Can be used with organic manures for balanced nutrition."
        ),
        "precautions": (
            "10-26-26 NPK Safety Precautions:\n"
            "• Use protective equipment: gloves, mask, and safety glasses.\n"
            "• Avoid contact with eyes and skin - rinse immediately if exposed.\n"
            "• Do not apply in excessive amounts - can cause nutrient imbalance.\n"
            "• Keep away from water sources to prevent eutrophication.\n"
            "• Store in original packaging, away from moisture and direct sunlight.\n"
            "• Do not mix with incompatible chemicals - check compatibility first.\n"
            "• Follow recommended dosages based on soil test results."
        )
    },
    "10-10-10": {
        "instructions": (
            "10-10-10 NPK Application Guidelines:\n"
            "• Dosage: Apply 150-200 kg/ha for sugarcane cultivation.\n"
            "• Timing: Apply before planting (basal) and during growth stages (30, 60, 90 days).\n"
            "• Method: Broadcast evenly or apply in bands near root zone.\n"
            "• Split Application: Divide total dose into 3-4 applications for optimal results.\n"
            "• Incorporation: Lightly incorporate into soil after application.\n"
            "• Compatibility: Can be used with organic manures for balanced nutrition."
        ),
        "precautions": (
            "10-10-10 NPK Safety Precautions:\n"
            "• Use protective equipment: gloves, mask, and safety glasses.\n"
            "• Avoid contact with eyes and skin - rinse immediately if exposed.\n"
            "• Do not apply in excessive amounts - can cause nutrient imbalance.\n"
            "• Keep away from water sources to prevent eutrophication.\n"
            "• Store in original packaging, away from moisture and direct sunlight.\n"
            "• Do not mix with incompatible chemicals - check compatibility first.\n"
            "• Follow recommended dosages based on soil test results."
        )
    }
}


class FertilizerPredictView(APIView):
    """Predict fertilizer recommendation using ML model."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # -------------------------------
            # 1. Get sensor data from frontend serializer OR fallback to Firebase
            # -------------------------------
            if request.data:
                # Frontend provided data via serializer
                serializer = FertilizerPredictionCreateSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                validated_data = serializer.validated_data
                sensor_data = {
                    'temperature': validated_data.get('temperature'),
                    'humidity': validated_data.get('humidity'),
                    'moisture': validated_data.get('moisture'),  # Already correct name from serializer
                    'nitrogen': validated_data.get('nitrogen'),
                    'phosphorous': validated_data.get('phosphorous'),  # Correct spelling
                    'potassium': validated_data.get('potassium'),
                    'soil_type': validated_data.get('soil_type', 'Loamy'),
                    'crop_type': 'Sugarcane',  # Fixed crop type - always "Sugarcane"
                    'soil_ph': None,  # Not in serializer, will try Firebase fallback
                    'ec': None  # Not in serializer, will try Firebase fallback
                }
                soil_type = validated_data.get('soil_type', 'Loamy')
                crop_type = 'Sugarcane'  # Fixed - always "Sugarcane"
                
                # Try to get soil_ph and ec from Firebase if not in frontend data
                try:
                    firebase_data = FirebaseService.get_sensor_readings()
                    if firebase_data.get('sensors') and len(firebase_data['sensors']) > 0:
                        firebase_sensor = firebase_data['sensors'][0]
                        if sensor_data['soil_ph'] is None:
                            sensor_data['soil_ph'] = firebase_sensor.get('soil_ph')
                        if sensor_data['ec'] is None:
                            sensor_data['ec'] = firebase_sensor.get('ec')
                        if sensor_data['humidity'] is None:
                            sensor_data['humidity'] = firebase_sensor.get('humidity')
                except Exception:
                    pass  # Continue without Firebase data if unavailable
                    
            else:
                # No frontend data - use Firebase data only
                firebase_data = FirebaseService.get_sensor_readings()
                if not firebase_data.get('sensors') or len(firebase_data['sensors']) == 0:
                    return Response(
                        {'error': 'No sensor data available. Provide sensor readings or wait for Firebase data.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Get normalized sensor data from Firebase (uses normalize_sensor_data method)
                firebase_sensor = firebase_data['sensors'][0]
                
                # Map Firebase fields correctly: soil_moisture -> moisture
                sensor_data = {
                    'temperature': firebase_sensor.get('temperature', 25.0),
                    'humidity': firebase_sensor.get('humidity', 50.0),
                    'moisture': firebase_sensor.get('soil_moisture', 50.0),  # Map soil_moisture to moisture
                    'soil_ph': firebase_sensor.get('soil_ph'),
                    'ec': firebase_sensor.get('ec'),
                    'nitrogen': firebase_sensor.get('nitrogen', 50.0),
                    'phosphorous': firebase_sensor.get('phosphorous', 30.0),  # Correct spelling from Firebase
                    'potassium': firebase_sensor.get('potassium', 40.0),
                    'soil_type': 'Loamy',  # Default if using Firebase only
                    'crop_type': 'Sugarcane'  # Fixed crop type
                }
                soil_type = sensor_data['soil_type']
                crop_type = sensor_data['crop_type']

            # -------------------------------
            # 2. Build DataFrame with EXACT training column names
            # -------------------------------
            # Column order and spelling must match training data EXACTLY:
            # Temparature, Humidity, Moisture, Soil_Type, Crop_Type, Nitrogen, Potassium, Phosphorous
            data_for_model = pd.DataFrame([{
                "Temparature": sensor_data['temperature'],  # Note: typo in training column name
                "Humidity": sensor_data['humidity'],
                "Moisture": sensor_data['moisture'],  # Correct field name
                "Soil_Type": soil_type,
                "Crop_Type": crop_type,  # Fixed to "Sugarcane"
                "Nitrogen": sensor_data['nitrogen'],
                "Potassium": sensor_data['potassium'],
                "Phosphorous": sensor_data['phosphorous']  # Correct spelling
            }])

            # Encode categorical variables using loaded encoders
            data_for_model["Soil_Type"] = soil_encoder.transform(data_for_model["Soil_Type"])
            data_for_model["Crop_Type"] = crop_encoder.transform(data_for_model["Crop_Type"])

            # -------------------------------
            # 3. Predict fertilizer using trained model
            # -------------------------------
            pred_encoded = model.predict(data_for_model)[0]
            fertilizer_name = fertilizer_encoder.inverse_transform([pred_encoded])[0]
            
            # Get confidence score if model supports predict_proba
            confidence_score = None
            try:
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(data_for_model)[0]
                    confidence_score = float(max(proba))
                elif hasattr(model, 'decision_function'):
                    # For some models, use decision function scores
                    scores = model.decision_function(data_for_model)[0]
                    if len(scores) == 1:
                        # Binary classification - convert to probability-like score
                        confidence_score = float(1 / (1 + abs(scores[0])))
                    else:
                        # Multi-class - use max score normalized
                        max_score = max(scores)
                        confidence_score = float(max_score / (sum(scores) + 1e-10))
            except Exception:
                # If confidence calculation fails, leave as None
                pass

            # -------------------------------
            # 4. Get instructions and precautions for the fertilizer
            # -------------------------------
            guide = FERTILIZER_GUIDE.get(fertilizer_name)
            if guide:
                instructions = guide.get("instructions", "")
                precautions = guide.get("precautions", "")
            else:
                # Fallback for unknown fertilizers (should not happen with the 14 fertilizers)
                instructions = (
                    f"{fertilizer_name} Application Guidelines:\n"
                    "• Follow manufacturer's recommended dosage and application rates.\n"
                    "• Apply during appropriate growth stages as per crop requirements.\n"
                    "• Incorporate into soil or apply as per recommended method.\n"
                    "• Ensure proper irrigation after application.\n"
                    "• Store in a cool, dry place away from moisture."
                )
                precautions = (
                    f"{fertilizer_name} Safety Precautions:\n"
                    "• Wear appropriate protective equipment during handling.\n"
                    "• Avoid direct contact with skin and eyes.\n"
                    "• Keep away from water sources and children.\n"
                    "• Follow all safety instructions on the product label.\n"
                    "• Store securely in original packaging."
                )

            # -------------------------------
            # 5. Save prediction using EXACT model field names
            # -------------------------------
            fertilizer_prediction = FertilizerPrediction.objects.create(
                user=request.user,
                temperature=sensor_data['temperature'],
                humidity=sensor_data.get('humidity'),
                moisture=sensor_data['moisture'],  # Model field is 'moisture', not 'soil_moisture'
                soil_ph=sensor_data.get('soil_ph'),
                ec=sensor_data.get('ec'),
                nitrogen=sensor_data['nitrogen'],
                phosphorous=sensor_data['phosphorous'],  # Model field is 'phosphorous', not 'phosphorus'
                potassium=sensor_data['potassium'],
                soil_type=sensor_data.get('soil_type'),
                crop_type=sensor_data.get('crop_type', 'Sugarcane'),
                recommended_fertilizer=fertilizer_name,
                fertilizer_amount=None,  # Not calculated by model
                confidence_score=confidence_score,
                recommendation_details=(
                    f"Predicted using ML model for {sensor_data.get('soil_type', 'Unknown')} "
                    f"soil and {sensor_data.get('crop_type', 'Sugarcane')} crop. "
                    f"Based on current sensor readings: Temperature={sensor_data['temperature']}°C, "
                    f"Moisture={sensor_data['moisture']}%, N={sensor_data['nitrogen']}, "
                    f"P={sensor_data['phosphorous']}, K={sensor_data['potassium']}."
                )
            )

            # -------------------------------
            # 6. Prepare response with required JSON structure
            # -------------------------------
            response_data = {
                "prediction": {
                    "recommended_fertilizer": fertilizer_name,
                    "instructions": instructions,
                    "precautions": precautions,
                    "fertilizer_amount": fertilizer_prediction.fertilizer_amount,
                    "confidence_score": confidence_score
                },
                "prediction_history": FertilizerPredictionSerializer(fertilizer_prediction).data,
                "sensor_readings": {
                    "temperature": sensor_data['temperature'],
                    "humidity": sensor_data.get('humidity'),
                    "moisture": sensor_data['moisture'],
                    "soil_ph": sensor_data.get('soil_ph'),
                    "ec": sensor_data.get('ec'),
                    "nitrogen": sensor_data['nitrogen'],
                    "phosphorous": sensor_data['phosphorous'],
                    "potassium": sensor_data['potassium'],
                    "soil_type": sensor_data.get('soil_type'),
                    "crop_type": sensor_data.get('crop_type', 'Sugarcane')
                },
                "message": "Fertilizer prediction completed successfully"
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            error_detail = str(e)
            traceback.print_exc()
            return Response(
                {"error": "Failed to predict fertilizer", "detail": error_detail},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FertilizerHistoryView(APIView):
    """Get fertilizer prediction history for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        predictions = FertilizerPrediction.objects.filter(user=request.user).order_by('-created_at')
        serializer = FertilizerPredictionSerializer(predictions, many=True)
        return Response({
            'count': predictions.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
