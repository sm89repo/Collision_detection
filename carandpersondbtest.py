import cv2
import numpy as np
import os
import mysql.connector
from mysql.connector import Error
import datetime
import time

from ultralytics import YOLO

# Initialize YOLO model
model = YOLO('yolov8s.pt')

# Video source
video_path = r"C:\Users\Madhwanath\Desktop\test1.mp4"
cap = cv2.VideoCapture(video_path)

# Directory for saving collision frames
collision_frames_dir = 'collision_frames'
if not os.path.exists(collision_frames_dir):
    try:
        os.makedirs(collision_frames_dir)
        print(f"Created directory: {collision_frames_dir}")
    except OSError as e:
        print(f"Error creating directory: {e}")
        exit()

# Initialize variables for collision detection and database insertion
last_collision_time = time.time()
collision_detected = False

# Function to calculate distance between two points
def calculate_distance(center1, center2):
    return np.sqrt((center2[0] - center1[0]) ** 2 + (center2[1] - center1[1]) ** 2)

# Function to insert collision details into the database
def insert_collision_details(time, details):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="collision_det"
        )
        if connection.is_connected():
            cursor = connection.cursor()

            insert_query = "INSERT INTO collision_details (time, details) VALUES (%s, %s)"
            cursor.execute(insert_query, (time, details))
            connection.commit()
            print("Collision details inserted into the database successfully.")

    except Error as e:
        print(f"Error inserting collision details into the database: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

while cap.isOpened():
    ret, annotated_frame = cap.read()
    if not ret:
        break

    # Detect objects using YOLO
    results = model.track(source=annotated_frame, device='cpu', classes=[0, 2], persist=True)
    boxes = results[0].boxes.xyxy
    annotated_frame = results[0].plot()

    person_boxes = []
    car_boxes = []

    for result in results[0]:
        if int(result.boxes.cls[0]) == 0:
            person_boxes.append(result.boxes.xyxy)
        if int(result.boxes.cls[0]) == 2:
            car_boxes.append(result.boxes.xyxy)

    for person_box in person_boxes:
        x1, y1, x2, y2 = [int(coord.item()) for coord in person_box[0]]

        for car_box in car_boxes:
            x3, y3, x4, y4 = [int(coord.item()) for coord in car_box[0]]

            center_person = ((x1 + x2) / 2, (y1 + y2) / 2)
            center_car = ((x3 + x4) / 2, (y3 + y4) / 2)
            distance = calculate_distance(center_person, center_car)

            distance_threshold = 500

            if distance < distance_threshold:
                color = (0, 0, 255, 128)
                cv2.putText(annotated_frame, 'DANGER: CLOSE PROXIMITY', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)
                print('Collision Alert!')

                # Check if a collision has been detected in the last 3 seconds
                if not collision_detected or (time.time() - last_collision_time) >= 3:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    collision_details = "Details of the collision"
                    insert_collision_details(current_time, collision_details)
                    last_collision_time = time.time()  # Update last collision time
                    collision_detected = True

            else:
                color = (0, 255, 0, 128)

            alpha = 0.3
            overlay = annotated_frame.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, cv2.FILLED)
            cv2.addWeighted(overlay, alpha, annotated_frame, 1 - alpha, 0, annotated_frame)

            overlay = annotated_frame.copy()
            cv2.rectangle(overlay, (x3, y3), (x4, y4), color, cv2.FILLED)
            cv2.addWeighted(overlay, alpha, annotated_frame, 1 - alpha, 0, annotated_frame)

            cv2.putText(annotated_frame, f'', (x3, y3 - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("collision frame", annotated_frame)

    if time.time() - last_collision_time >= 3:
        collision_detected = False

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
