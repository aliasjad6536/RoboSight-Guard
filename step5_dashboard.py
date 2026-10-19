import streamlit as st
import cv2
import math
import tempfile
import winsound
from ultralytics import YOLO

st.set_page_config(page_title="RoboSight Guard", layout="wide")
st.title("🚧 RoboSight Guard")
st.subheader("AI-Powered Warehouse Safety & Collision Avoidance System")

@st.cache_resource
def load_model():
    return YOLO('yolov8m.pt')

model = load_model()

st.sidebar.header("⚙️ Control Panel")
conf_thresh = st.sidebar.slider("AI Confidence", 0.05, 1.0, 0.10)
# Default danger zone thoda zyada (200) kar diya taake jaldi alarm baje
danger_zone = st.sidebar.slider("Danger Zone Radius", 50, 400, 200) 

st.write("### Upload CCTV Footage")
uploaded_file = st.file_uploader("Accident ya Near-Miss ki video upload karein (.mp4)", type=["mp4", "avi"])

if uploaded_file is not None:
    st.success("Video upload ho gayi! AI Processing Shuru ho rahi hai...")
    
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    
    stframe = st.empty()
    warning_msg = st.empty()
    
    frame_skip = 3  
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        if frame_count % frame_skip != 0:
            continue
            
        annotated_frame = frame.copy()
        people_centers = []
        vehicle_centers = []
        
        results = model.track(frame, persist=True, conf=conf_thresh, imgsz=736, tracker="bytetrack.yaml", verbose=False)
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            clss = results[0].boxes.cls.cpu().numpy()
            
            for box, cls in zip(boxes, clss):
                x1, y1, x2, y2 = map(int, box)
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                
                if int(cls) == 0:
                    people_centers.append((cx, cy))
                    cv2.circle(annotated_frame, (cx, cy), danger_zone, (0, 255, 255), 2)
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(annotated_frame, "Worker", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                else:
                    if (x2 - x1) > 40 and (y2 - y1) > 40:
                        vehicle_centers.append((cx, cy))
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(annotated_frame, "Forklift", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        cv2.circle(annotated_frame, (cx, cy), 8, (0, 255, 0), -1)

        danger = False
        for person_center in people_centers:
            for vehicle_center in vehicle_centers:
                distance = math.dist(person_center, vehicle_center)
                if distance < danger_zone:
                    danger = True
                    cv2.line(annotated_frame, person_center, vehicle_center, (0, 0, 255), 4)
                    cv2.putText(annotated_frame, f"Dist: {int(distance)}px", 
                                (int((person_center[0]+vehicle_center[0])/2), int((person_center[1]+vehicle_center[1])/2) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3) 
        
        if danger:
            # TEXT AUR BORDER DOUBLE BADA KAR DIYA
            cv2.rectangle(annotated_frame, (0, 0), (annotated_frame.shape[1], annotated_frame.shape[0]), (0, 0, 255), 20)
            cv2.putText(annotated_frame, "EMERGENCY STOP!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 8)
            warning_msg.error("⚠️ EMERGENCY STOP! COLLISION DANGER DETECTED!")
            try:
                winsound.Beep(2500, 100)
            except:
                pass
        else:
            warning_msg.empty()
            
        display_frame = cv2.resize(annotated_frame, (800, 600))
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        
        stframe.image(display_frame, channels="RGB", use_container_width=True)
        
    cap.release()
    st.success(" Video Processing complete!")