from django.shortcuts import render
from django.http import JsonResponse
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from django.views.decorators.csrf import csrf_exempt

# Load the trained model and class names
model = load_model("classifier/keras/keras_model.h5", compile=False)

with open("classifier/keras/labels.txt", "r") as file:
    class_names = [line.strip() for line in file.readlines()]

# Function to preprocess the image
def preprocess_image(image):
    img = Image.open(image).convert("RGB")  # Open image and convert to RGB if necessary
    img = img.resize((224, 224))  # Resize to match the model's expected input size
    img_array = np.array(img) / 255.0  # Normalize the image
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

from django.http import StreamingHttpResponse
import json

@csrf_exempt
def classify_image(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        uploaded_images = request.FILES.getlist('images')

        def generate():
            yield '{"results": [\n'  # Begin JSON list
            first = True
            for uploaded_image in uploaded_images:
                img_array = preprocess_image(uploaded_image)
                predictions = model.predict(img_array)
                predicted_class = np.argmax(predictions, axis=1)
                predicted_label = class_names[predicted_class[0]]
                confidence_score = float(predictions[0][predicted_class[0]])

                result = {
                    'image_name': uploaded_image.name,
                    'predicted_class': predicted_label,
                    'confidence_score': confidence_score
                }

                # Add comma between items (except the first one)
                if not first:
                    yield ',\n'
                else:
                    first = False

                yield json.dumps(result)

            yield '\n]}'  # End JSON list

        return StreamingHttpResponse(generate(), content_type='application/json')

    return JsonResponse({'error': 'No images provided or invalid request'}, status=400)


def home(request):
    return render(request, 'home.html')  # Render the home.html template
