from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt  # To display images
import tensorflow as tf

print(tf.__version__)
print(tf.keras.__version__)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("classifier/keras/keras_model.h5", compile=False)
model.summary()
# Load the labels
with open("classifier/keras/labels.txt", "r") as file:
    class_names = [line.strip() for line in file.readlines()]

# Replace this with the path to your image
image_path = "classifier/test (1).jpg"

# Open the image
image = Image.open(image_path).convert("RGB")

# Display the image to verify it's correct
plt.imshow(image)
plt.title("Input Image")
plt.show()

# Print the image version (size and format)
print(f"Image Size: {image.size}")  # Width, Height
print(f"Image Mode: {image.mode}")  # Color format (RGB, L, etc.)

# Resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

# Display the resized image to verify it
plt.imshow(image)
plt.title("Resized Image")
plt.show()

# Turn the image into a numpy array
image_array = np.asarray(image)

# Print image array shape and type for debugging
print(f"Image Array Shape: {image_array.shape}")  # Should be (224, 224, 3)
print(f"Image Array Type: {image_array.dtype}")  # Should be float32 or uint8

# Normalize the image (if the model was trained with this method)
normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

# Create the array of the right shape to feed into the keras model
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
data[0] = normalized_image_array

# Predict with the model
prediction = model.predict(data)

# Get the index of the highest prediction
index = np.argmax(prediction)

# Retrieve the class name and confidence score
class_name = class_names[index]
confidence_score = prediction[0][index]

# Print prediction and confidence score
print("Class:", class_name)
print("Confidence Score:", confidence_score)
