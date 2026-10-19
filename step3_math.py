import cv2
import math
import winsound
from ultralytics import YOLO

# HACKATHON MASTER FIX: Powerful Medium Model
model = YOLO('yolov8m.pt') 

video_path = 'Video/accident.mp4.mp4'  # Apni video ka path theek kar lein
cap = cv2.VideoCapture(video_path)

DANGER_ZONE_RADIUS = 150 

print("==================================================")
print("🔥 HACKATHON ULTIMATE FIX: High-Res & No Class Limit")
print("==================================================")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    annotated_frame = frame.copy()
    people_centers = []
    vehicle_centers = []

    # BADA FIX: imgsz=1080 (High resolution) aur classes limit hata di! Confidence 0.10 kar diya.
    results = model.track(frame, persist=True, conf=0.10, imgsz=1080, tracker="bytetrack.yaml", verbose=False)

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        clss = results[0].boxes.cls.cpu().numpy()

        for box, cls in zip(boxes, clss):
            x1, y1, x2, y2 = map(int, box)
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

            # Agar Class 0 (Insaan) hai
            if int(cls) == 0:
                people_centers.append((cx, cy))
                cv2.circle(annotated_frame, (cx, cy), DANGER_ZONE_RADIUS, (0, 255, 255), 2)
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(annotated_frame, "Worker", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            # HACKATHON TRICK: Agar koi bhi aur cheez hai (jo kachra na ho, size > 40px ho)
            else:
                if (x2 - x1) > 40 and (y2 - y1) > 40: # Chote kachre (noise) ko ignore karne ke liye
                    vehicle_centers.append((cx, cy))
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated_frame, "Forklift", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.circle(annotated_frame, (cx, cy), 8, (0, 255, 0), -1)

    # Core Distance Logic & Alarm
    danger = False
    for person_center in people_centers:
        for vehicle_center in vehicle_centers:
            distance = math.dist(person_center, vehicle_center)
            
            if distance < DANGER_ZONE_RADIUS:
                danger = True
                cv2.line(annotated_frame, person_center, vehicle_center, (0, 0, 255), 4)
                cv2.putText(annotated_frame, f"Dist: {int(distance)}px", 
                    (int((person_center[0]+vehicle_center[0])/2), int((person_center[1]+vehicle_center[1])/2) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

    if danger:
        cv2.rectangle(annotated_frame, (0, 0), (annotated_frame.shape[1], annotated_frame.shape[0]), (0, 0, 255), 15)
        cv2.putText(annotated_frame, "EMERGENCY STOP!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        try:
            winsound.Beep(2500, 100)
        except:
            pass

    cv2.imshow("RoboSight Guard - Master Engine", annotated_frame)
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()