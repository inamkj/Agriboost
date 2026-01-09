
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.conf import settings
import tensorflow as tf
from PIL import Image
import numpy as np
import io
from .models import DiseaseHistory
from .serializers import DiseaseHistorySerializer

_model = None

# 🔹 Disease info dictionary
DISEASE_INFO = {
    "Banded Chlorosis": "Apply Zinc sulphate (ZnSO4) 25 kg/ha with 200 kg urea. Improve soil drainage.",
    "Brown Spot": "Spray Mancozeb 75% WP @ 2.5 g/L or Carbendazim 50% WP @ 1 g/L. Keep field clean.",
    "Dried Leaves": "Check nutrient deficiency. Foliar spray NPK (19:19:19) 2 g/L. Maintain irrigation.",
    "Grassy Shoot": "Caused by phytoplasma. Remove infected clumps. Spray Imidacloprid 0.05%.",
    "Healthy": "No disease detected. Maintain balanced fertilization (NPK 150:60:60 kg/ha).",
    "Mosaic": "Viral disease. Remove infected plants. Use resistant varieties. Spray Dimethoate 2 ml/L.",
    "Pokkah Boeng": "Spray Carbendazim 0.1% or Propiconazole 1 ml/L. Remove infected leaves.",
    "Red Rot": "Severe! Remove infected plants. Treat seed with Carbendazim 0.1% before sowing.",
    "Rust": "Spray Propiconazole 1 ml/L or Mancozeb 2.5 g/L. Use resistant varieties.",
    "Sett Rot": "Treat seed sets with Carbendazim 0.1% or Thiram 0.2% for 30 min.",
    "Smut": "Hot water treatment of sets (50°C, 30 min). Spray Propiconazole 1 ml/L.",
    "Yellow": "Apply ZnSO4 25 kg/ha with urea. Improve irrigation. Spray Mancozeb if fungal.",
}

# 🔹 Class labels
CLASS_NAMES = list(DISEASE_INFO.keys())

def _load_model():
    global _model
    if _model is None:
        try:
            _model = tf.keras.models.load_model(settings.DISEASE_MODEL_PATH)
        except Exception as e:
            raise e
    return _model

def _prepare_image(image_file, target_size=(128, 128)):
    image_bytes = io.BytesIO(image_file.read())
    image = tf.keras.preprocessing.image.load_img(image_bytes, target_size=target_size)
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # shape (1, 128, 128, 3)
    return input_arr

class PredictDiseaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        uploaded = request.FILES.get("image")
        if not uploaded:
            return Response({"image": "Image file is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            model = _load_model()
        except FileNotFoundError:
            return Response({"detail": "Model file not found on server."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"detail": f"Failed to load model: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            input_tensor = _prepare_image(uploaded)
            preds = model.predict(input_tensor)
            prob = float(np.max(preds))
            label_idx = int(np.argmax(preds))

            # 🔹 Confidence threshold
            THRESHOLD = 0.7
            if prob < THRESHOLD:
                return Response({
                    "prediction": {
                        "label_index": None,
                        "label": "Unknown",
                        "confidence": round(prob, 4),
                        "recommendation": "Unclear image. Please upload a clear sugarcane leaf."
                    }
                }, status=status.HTTP_200_OK)

            disease = CLASS_NAMES[label_idx]
            recommendation = DISEASE_INFO.get(disease, "No recommendation available.")

            result = {
                "label_index": label_idx,
                "label": disease,
                "confidence": round(prob, 4),
                "recommendation": recommendation,
            }

            history = DiseaseHistory.objects.create(
                user=request.user,
                
                label=result["label"],
                confidence=result["confidence"],
                recommendation=result["recommendation"],
            )
        except Exception as e:
            return Response({"detail": f"Prediction failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"prediction": result, "history_id": history.id}, status=status.HTTP_200_OK)

class UserDiseaseHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        history = DiseaseHistory.objects.filter(user=request.user).order_by("-created_at")
        serializer = DiseaseHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
