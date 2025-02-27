# -*- coding: utf-8 -*-
"""iva_last2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fMANhLWQKyIIQFA17GmVCcoK5Bhj2GxO
"""

from google.colab import files
import cv2
import numpy as np

video_path = "/content/sample_data/2936741-uhd_3840_2160_30fps.mp4"  # Assume the first uploaded file is the video


# Step 2: Initialize video capture
video_capture = cv2.VideoCapture(video_path)
total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
frames_per_quarter = total_frames // 4

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Read the first frame and detect faces
ret, old_frame = video_capture.read()
if not ret:
    print("Error: Cannot read the video.")
    video_capture.release()
    exit()

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(old_gray, scaleFactor=1.1, minNeighbors=5)

# Create points for tracking the detected faces
points_to_track = []
for (x, y, w, h) in faces:
    points_to_track.append([[x + w // 2, y + h // 2]])  # Track the center of the detected face

points_to_track = np.array(points_to_track, dtype=np.float32)

# Optical flow parameters
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

quarter_counts = [0, 0, 0, 0]
frame_count = 0

while video_capture.isOpened():
    ret, frame = video_capture.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate optical flow
    new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, points_to_track, None, **lk_params)

    # Filter valid points
    good_new = new_points[status == 1]
    good_old = points_to_track[status == 1]

    # Draw points on the frame
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        x_new, y_new = new.ravel()
        x_old, y_old = old.ravel()
        cv2.circle(frame, (int(x_new), int(y_new)), 5, (0, 255, 0), -1)
        cv2.line(frame, (int(x_new), int(y_new)), (int(x_old), int(y_old)), (255, 0, 0), 2)

    # Count the number of tracked points in the current frame and determine the quarter
    num_faces_tracked = len(good_new)

    if frame_count < frames_per_quarter:
        quarter_counts[0] += num_faces_tracked
    elif frame_count < frames_per_quarter * 2:
        quarter_counts[1] += num_faces_tracked
    elif frame_count < frames_per_quarter * 3:
        quarter_counts[2] += num_faces_tracked
    else:
        quarter_counts[3] += num_faces_tracked

    frame_count += 1
    old_gray = frame_gray.copy()
    points_to_track = good_new.reshape(-1, 1, 2)

    if frame_count >= total_frames:
        break

video_capture.release()

# Display the counts for each quarter
for i, count in enumerate(quarter_counts):
    print(f"Number of faces tracked in quarter {i + 1}: {count}")

from google.colab import files
import cv2
import numpy as np
from google.colab.patches import cv2_imshow

video_path = "/content/sample_data/2936741-uhd_3840_2160_30fps.mp4"  # Assume the first uploaded file is the video


# Step 2: Initialize video capture
video_capture = cv2.VideoCapture(video_path)
total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
frames_per_quarter = total_frames // 4

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Read the first frame and detect faces
ret, old_frame = video_capture.read()
if not ret:
    print("Error: Cannot read the video.")
    video_capture.release()
    exit()

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(old_gray, scaleFactor=1.1, minNeighbors=5)

# Create points for tracking the detected faces
points_to_track = []
for (x, y, w, h) in faces:
    points_to_track.append([[x + w // 2, y + h // 2]])  # Track the center of the detected face

points_to_track = np.array(points_to_track, dtype=np.float32)

# Optical flow parameters
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

quarter_counts = [0, 0, 0, 0]
frame_count = 0
quarter_frames = [None, None, None, None]  # To store one frame per quarter

while video_capture.isOpened():
    ret, frame = video_capture.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate optical flow
    new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, points_to_track, None, **lk_params)

    # Filter valid points
    good_new = new_points[status == 1]
    good_old = points_to_track[status == 1]

    # Draw points on the frame
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        x_new, y_new = new.ravel()
        x_old, y_old = old.ravel()
        cv2.circle(frame, (int(x_new), int(y_new)), 5, (0, 255, 0), -1)
        cv2.line(frame, (int(x_new), int(y_new)), (int(x_old), int(y_old)), (255, 0, 0), 2)

    # Count the number of tracked points in the current frame and determine the quarter
    num_faces_tracked = len(good_new)
    if frame_count < frames_per_quarter:
        quarter_counts[0] += num_faces_tracked
        if quarter_frames[0] is None:
            quarter_frames[0] = frame  # Save the first frame of the first quarter
    elif frame_count < frames_per_quarter * 2:
        quarter_counts[1] += num_faces_tracked
        if quarter_frames[1] is None:
            quarter_frames[1] = frame  # Save the first frame of the second quarter
    elif frame_count < frames_per_quarter * 3:
        quarter_counts[2] += num_faces_tracked
        if quarter_frames[2] is None:
            quarter_frames[2] = frame  # Save the first frame of the third quarter
    else:
        quarter_counts[3] += num_faces_tracked
        if quarter_frames[3] is None:
            quarter_frames[3] = frame  # Save the first frame of the fourth quarter
    frame_count += 1
    old_gray = frame_gray.copy()
    points_to_track = good_new.reshape(-1, 1, 2)
    if frame_count >= total_frames:
        break
video_capture.release()
# Display the frames from each quarter
for i, frame in enumerate(quarter_frames):
    print(f"Displaying frame from quarter {i + 1} with {int(quarter_counts[i]/10)} tracked faces.")
    cv2_imshow(frame)  # Display one frame from each quarter
# Display the counts for each quarter
for i, count in enumerate(quarter_counts):
    count=int(count/10)
    print(f"Number of faces tracked in quarter {i + 1}: {count}")

