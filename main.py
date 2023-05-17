import cv2
import os
import tkinter as tk
from tkinter import filedialog
import face_recognition
import numpy as np

# Load known faces
known_faces = []
known_names = []
for file_name in os.listdir('encodings'):
    if file_name.endswith('.csv'):
        # Load the encoding from the CSV file
        encoding_file = os.path.join('encodings', file_name)
        encoding = np.loadtxt(encoding_file, delimiter=',')
        
        # Extract the name from the file name
        name = os.path.splitext(file_name)[0]
        
        # Add the encoding and name to the lists
        known_faces.append(encoding)
        known_names.append(name)
print(known_names)

#open file dialogue window
root = tk.Tk()
root.withdraw()
video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
video = cv2.VideoCapture(video_path)

while True:
    ret, frame = video.read()

    if not ret:
        break

    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

    # Loop over the detected faces
    for (x, y, w, h) in faces:
        # Extract the face ROI
        face_roi = frame_gray[y:y+h, x:x+w]

        # Resize the face ROI to 160x160
        face_roi = cv2.resize(face_roi, (160, 160))


        face_encoding = face_recognition.face_encodings(cv2.cvtColor(face_roi, cv2.COLOR_GRAY2RGB))[0]
        matches = face_recognition.compare_faces(np.array(known_faces), np.array(face_encoding))
        if True in matches:
            predicted_label = known_names[matches.index(True)]
        else:
            predicted_label = "Unknown"

        # Draw a rectangle around the face and display the predicted label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        cv2.putText(frame, predicted_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

    # Display the frame
    cv2.imshow("Faces", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
video.release()
cv2.destroyAllWindows()
