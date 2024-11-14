# -*- coding: utf-8 -*-
"""iva_last3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EH3jXop8FaolAO66PEJUhHn0L47qgOjT
"""

from google.colab import files
import cv2
import os
import numpy as np
from google.colab.patches import cv2_imshow

reference_image_path = "/content/sample_data/Screenshot 2024-11-14 112532.png"
video_path = "/content/sample_data/faces.mp4"

# Step 2: Load and preprocess the reference photo
reference_img = cv2.imread(reference_image_path)
gray_ref = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)
# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Detect face in the reference photo
ref_faces = face_cascade.detectMultiScale(gray_ref, scaleFactor=1.1, minNeighbors=5)
if len(ref_faces) > 0:
    (x, y, w, h) = ref_faces[0]  # Assume the first detected face is the person of interest
    ref_face = gray_ref[y:y+h, x:x+w]
else:
    print("No face detected in the reference photo.")
    exit()
# Step 3: Initialize video capture
video_capture = cv2.VideoCapture(video_path)
frame_count = 0
tracked_frames = []  # List to store frames with detected faces

# Use ORB detector for feature extraction
orb = cv2.ORB_create()
kp_ref, des_ref = orb.detectAndCompute(ref_face, None)

# Matcher for feature matching
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
while video_capture.isOpened() and frame_count < 50:  # Process only the first 50 frames
    ret, frame = video_capture.read()
    if not ret:
        break
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces in the current frame
    faces_in_frame = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces_in_frame:
        detected_face = gray_frame[y:y+h, x:x+w]
        kp_frame, des_frame = orb.detectAndCompute(detected_face, None)
        if des_frame is not None:
            # Match features between the reference face and detected face
            matches = bf.match(des_ref, des_frame)
            matches = sorted(matches, key=lambda x: x.distance)
            # If enough matches are found, consider it a match
            if len(matches) > 30:
                # Highlight the detected face in the frame
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Store the frame in the list
                tracked_frames.append(frame)
                # Display the frame with the detected face
                print(f"Frame {frame_count}: Detected matching face")
                cv2_imshow(frame)
    frame_count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()

# Step 4: Combine the frames into a video
if tracked_frames:
    height, width, layers = tracked_frames[0].shape
    output_video = 'output_tracked_video.avi'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Use 'mp4v' for .mp4 files or 'XVID' for .avi
    out = cv2.VideoWriter(output_video, fourcc, 20.0, (width, height))

    for frame in tracked_frames:
        out.write(frame)

    out.release()
    print(f"Video has been created and saved as '{output_video}'")
else:
    print("No frames to save in the video.")
