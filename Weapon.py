# Import necessary libraries
import cv2
import numpy as np
from tensorflow import keras

# Load the pre-trained model from the HDF5 file
model = keras.models.load_model('gun_model.h5')

# Load an image for detection
image_path = 'gun.jpg'
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV loads images in BGR, convert to RGB

# Resize the image to match the input size of the model
input_shape = model.input_shape[1:3]  # Assuming the model's input shape is (height, width, channels)
resized_image = cv2.resize(image, (input_shape[1], input_shape[0]))

# Normalize the image to match the preprocessing used during training
normalized_image = resized_image / 255.0  # Assuming the model was trained with values in the range [0, 255]

# Expand the dimensions to create a batch of size 1
input_image = np.expand_dims(normalized_image, axis=0)

# Make predictions using the model
predictions = model.predict(input_image)

# Process the predictions as needed for your specific task (e.g., object detection)
# This may involve extracting bounding box coordinates, class scores, etc.

# Example: Print the class probabilities
print("Class Probabilities:", predictions)

# Example: Extract bounding box coordinates
box_coordinates = predictions[0][:, :4]  # Assuming the bounding box coordinates are in the first 4 elements
print("Bounding Box Coordinates:", box_coordinates)

cv2.imshow('Webcam', image)
