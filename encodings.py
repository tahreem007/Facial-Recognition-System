import face_recognition
import numpy as np
import os


# Define the paths to the input and output directories
input_dir = r"C:\Users\92331\OneDrive\Desktop\Face_recognition Project\faces"
output_dir = r"C:\Users\92331\OneDrive\Desktop\Face_recognition Project\encodings"


# Loop over the files in the input directory
for image_file in os.listdir(input_dir):
    # Load the image
    image = face_recognition.load_image_file(os.path.join(input_dir, image_file))
    
    # Detect faces in the image
    face_locations = face_recognition.face_locations(image)
    
    # Compute the face encodings for each face in the image
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    # Save the face encodings as a CSV file
    output_file = os.path.join(output_dir, os.path.splitext(image_file)[0] + '.csv')
    np.savetxt(output_file, face_encodings, delimiter=',')
