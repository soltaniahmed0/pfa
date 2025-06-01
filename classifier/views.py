from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from django.contrib.auth.decorators import login_required
from PIL import Image
import numpy as np
import os
import uuid
from django.conf import settings
from django.utils import timezone
from classifier.models import AnalysisHistory

# Load model
model_path = os.path.join(settings.BASE_DIR, "classifier/keras/keras_model.h5")
labels_path = os.path.join(settings.BASE_DIR, "classifier/keras/labels.txt")

model = load_model(model_path, compile=False)
class_names = [line.strip() for line in open(labels_path, "r")]

def preprocess_image(image):
    img = Image.open(image).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def home(request):
    return render(request, 'classifier/home.html')


def about(request):
    return render(request, 'classifier/about.html')


def landing_page(request):
    return render(request, 'classifier/landing.html')

@csrf_exempt
def classify_image(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        try:
            results = []
            
            for img in request.FILES.getlist('images'):
                # Generate unique filename
                img_name = f"{uuid.uuid4().hex}{os.path.splitext(img.name)[1]}"
                img_path = os.path.join(settings.MEDIA_ROOT, img_name)
                
                # Save image
                with open(img_path, 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)
                
                # Process and predict
                img_array = preprocess_image(img_path)
                predictions = model.predict(img_array)
                class_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][class_idx]) * 100
                
                # Class mapping
                class_mapping = {
                    0: "Aculus olearius",
                    1: "Peacock Spot",
                    2: "Healthy"
                }
                
# Enregistrer dans l'historique
                if request.user.is_authenticated:
                    AnalysisHistory.objects.create(
                        user=request.user,
                        image=img_name,
                        disease_name=class_mapping.get(class_idx, "Unknown"),
                        confidence=confidence,
                        is_healthy=(class_idx == 2),
                        treatment_recommendation=get_treatment_recommendation(class_idx)
                    )

                results.append({
                    'image_name': img.name,
                    'image_path': img_name,
                    'disease_name': class_mapping.get(class_idx, "Unknown"),
                    'confidence': confidence,
                    'is_healthy': class_idx == 2,
                    'treatment_recommendation': get_treatment_recommendation(class_idx),
                })
            
            context = {
                'results': results,
                'MEDIA_URL': settings.MEDIA_URL,
            }
            
            return render(request, 'classifier/results.html', context)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'classifier/upload.html')

def get_treatment_recommendation(class_idx):
    recommendations = {
        0: "Application of specific acaricide recommended.",
        1: "Copper-based fungicide treatment required.",
        2: "No treatment needed. Your olive tree is healthy."
    }
    return recommendations.get(class_idx, "Please consult a specialist.")

