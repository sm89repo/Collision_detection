import cv2
from ultralytics import YOLO
import numpy as np
import os

def calculate_distance(center1, center2):
    return np.sqrt((center2[0] - center1[0]) ** 2 + (center2[1] - center1[1]) ** 2)

model = YOLO('yolov8s.pt')
video_path = r"C:\Users\Madhwanath\Downloads\forklift-accident.mp4"
cap = cv2.VideoCapture(video_path)
collision_frames_dir = 'collision_frames'

if not os.path.exists(collision_frames_dir):
    try:
        os.makedirs(collision_frames_dir)
        print(f"Created directory: {collision_frames_dir}")
    except OSError as e:
        print(f"Error creating directory: {e}")
        exit()

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, device='cpu')
    boxes = results[0].boxes.xyxy

    person_boxes = []
    car_boxes = []

    for result in results[0]:
        if int(result.boxes.cls[0]) == 0:
            person_boxes.append(result.boxes.xyxy)
        if int(result.boxes.cls[0]) == 2:
            car_boxes.append(result.boxes.xyxy)

    for person_box in person_boxes:
        x1, y1, x2, y2 = [int(coord.item()) for coord in person_box[0]]
        center_person = ((x1 + x2) / 2, (y1 + y2) / 2)
        person_radius = int(calculate_distance((x1, y1), (x2, y2)) / 2)

        for car_box in car_boxes:
            x3, y3, x4, y4 = [int(coord.item()) for coord in car_box[0]]
            center_car = ((x3 + x4) / 2, (y3 + y4) / 2)
            car_radius = int(calculate_distance((x3, y3), (x4, y4)) / 2)

            distance = calculate_distance(center_person, center_car)

            if distance < car_radius:
                color = (0, 0, 255)
                cv2.putText(frame, 'DANGER: CLOSE PROXIMITY', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)
                print('Collision Alert!')

                cv2.imwrite(os.path.join(collision_frames_dir, f"collision_frame_{frame_count}.jpg"), frame)
                print(f"Saved collision frame {frame_count}")
                frame_count += 1

            else:

                color = (0, 255, 0)

            cv2.circle(frame, (int(center_person[0]),int(center_person[1])),person_radius,color, 2)
            cv2.circle(frame, (int(center_car[0]),int(center_car[1])),car_radius, color, 2)

    cv2.imshow("collision frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
