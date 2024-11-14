# -*- coding: utf-8 -*-
"""iva_last5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YB0oRElmIq_Q7JDBGMzKNhk2EgmjcOSF
"""

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# Step 1: Load the video
video_path = "/content/sample_data/10901926-hd_1920_1080_30fps.mp4"  # Replace with your video path
video_capture = cv2.VideoCapture(video_path)

# Step 2: Define the Region of Interest (ROI)
# ROI as a rectangle (x, y, width, height)
roi_x, roi_y, roi_w, roi_h = 1200, 600, 300, 400  # Adjust these values based on your video
roi = (roi_x, roi_y, roi_w, roi_h)

# Step 3: Initialize the background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

# Step 4: Track the time each object stays in the ROI
object_times = {}

frame_count = 0
start_frame = 50  # Start from frame 50
end_frame = 100   # Stop at frame 100

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Only process frames within the range [start_frame, end_frame]
    if frame_count < start_frame:
        frame_count += 1
        continue
    if frame_count > end_frame:
        break

    # Step 5: Apply background subtraction to detect moving objects
    fgmask = fgbg.apply(frame)

    # Step 6: Find contours of the moving objects
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 7: Iterate over the contours and track moving objects in the ROI
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Ignore small contours (noise)
            x, y, w, h = cv2.boundingRect(contour)

            # Check if the bounding box intersects the ROI
            if (x + w > roi_x and x < roi_x + roi_w and
                y + h > roi_y and y < roi_y + roi_h):

                # Draw bounding box around the detected object
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Track the object in the ROI
                object_id = f"{x}-{y}-{w}-{h}"  # Unique ID based on bounding box
                if object_id not in object_times:
                    object_times[object_id] = {'enter': frame_count, 'exit': None}
                else:
                    # Update exit time if the object leaves the frame
                    if object_times[object_id]['exit'] is None:
                        object_times[object_id]['exit'] = frame_count

                # Show time inside ROI on the frame
                if object_times[object_id]['exit'] is None:
                    time_in_roi = frame_count - object_times[object_id]['enter']
                else:
                    time_in_roi = object_times[object_id]['exit'] - object_times[object_id]['enter']

                cv2.putText(frame, f"Time in ROI: {time_in_roi} frames", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Draw the ROI rectangle on the frame
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 0, 0), 2)

    # Step 8: Display the result
    cv2.putText(frame, f"Objects in ROI: {len(object_times)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2_imshow(frame)

    # Print the time spent in the ROI for each object
    print(f"Frame {frame_count}:")
    for object_id, times in object_times.items():
        if times['exit'] is None:
            time_in_roi = frame_count - times['enter']
        else:
            time_in_roi = times['exit'] - times['enter']

        print(f"Object {object_id} has been in the ROI for {time_in_roi} frames.")

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
