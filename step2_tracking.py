import cv2
from ultralytics import YOLO

# 1. Pre-trained YOLOv8 model load karein (yolov8s = small, fast & accurate)
model = YOLO('yolov8s.pt')

# 2. Near-miss wali video ko input dein
video_path = 'Video/accident.mp4.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Video file nahi mili ya open nahi ho rahi: {video_path}")
    exit()

print("Video processing shuru ho rahi hai... 'q' dabane par window band hogi.")

# 3. Frame-by-frame processing loop
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Video complete ho gayi.")
        break

    # 4. YOLO Tracking chalayein
    # persist=True: Frame to frame IDs ko maintain rakhta hai
    # classes=[0, 2, 7]: 0=Person, 2=Car, 7=Truck (Forklift aksar truck ya car mein classify hoti hai)
    results = model.track(frame, persist=True, classes=[0, 2, 7], verbose=False)

    # 5. Tracking results ko frame par draw karein (Boxes + IDs)
    annotated_frame = results[0].plot()

    # 6. Screen par live output show karein
    cv2.imshow("RoboSight Guard - Step 2 Object Tracking", annotated_frame)

    # Keyboard par 'q' press karne par loop ruk jaye
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()