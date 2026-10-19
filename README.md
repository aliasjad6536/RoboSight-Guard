<img width="913" height="526" alt="image" src="https://github.com/user-attachments/assets/9991958a-2502-4f6c-9545-13b3970e5995" />

# RoboSight Guard: AI-Powered Workplace Safety & Collision Avoidance System

## Abstract
RoboSight Guard is a highly optimized, computer vision-based safety system engineered to mitigate the risk of industrial accidents. By ingesting and processing real-time CCTV footage, the system identifies human workers and heavy industrial machinery (specifically forklifts), continuously calculates their spatial Euclidean proximity, and triggers immediate visual and auditory emergency protocols if a predefined safety radius is breached. Developed as a robust solution for the NYLP AI Hackathon 2026, the architecture emphasizes practical deployment, low-latency inference, and real-time hazard mitigation in dynamic environments.

## Problem Statement
Industrial warehouses and construction sites exhibit a high statistical probability of collisions between pedestrians and moving machinery. Conventional CCTV networks serve a purely passive role, heavily reliant on continuous human observation which is prone to fatigue and error. The objective of this research and development phase was to engineer an active, automated AI surveillance layer capable of proactively detecting near-miss events and impending collisions under suboptimal conditions, including camera glare, motion blur, and low-resolution sensor feeds.

## Research & Methodology (System Evolution)

### Phase 1: Custom Model Training & Weights Generation
Initial developmental phases focused on training a specialized YOLOv8 architecture strictly for forklift detection. The model was trained using a custom annotated dataset (data.yaml) over 10 epochs to generate the baseline weights.

*Training Configurations and Checkpoint Verification:*
[Drag and drop your step4_train.py and runs/detect folder screenshots here]

### Phase 2: Addressing the Domain Gap & Tracking Integration
While the custom model demonstrated high precision on the localized dataset, deployment against raw CCTV feeds revealed a significant "Domain Gap" caused by environmental variance. The architecture was strategically pivoted:
*   **Generalized Weights:** Transitioned to a generalized, pre-trained medium architecture (`yolov8m.pt`) for superior feature extraction.
*   **ByteTrack Algorithm:** To counter false negatives caused by harsh lighting and partial occlusions, the YOLO ByteTrack algorithm was integrated. This assigned persistent tracking IDs, stabilizing bounding box rendering across consecutive frames.
*   **Algorithmic Filtering:** Replaced rigid class dependencies with a dimensional filtering heuristic to identify moving industrial objects while suppressing background noise.

### Phase 3: Web Dashboard Optimization
The backend computer vision pipeline was bridged to a Streamlit frontend for user interaction. To prevent browser rendering latency during high-resolution processing:
*   **Resolution Scaling:** Inference resolution was constrained to `imgsz=736`.
*   **Temporal Subsampling:** A frame-skipping mechanism was introduced, processing every third frame to maintain real-time performance overhead without sacrificing safety parameters.

## System Architecture Workflow

```text
[CCTV Video Input Stream] 
           |
           v
[Frame Extraction & Pre-processing]
           |
           v
[YOLOv8 Medium + ByteTrack Algorithm]
(Continuous Entity Identification)
           |
           v
[Euclidean Distance Calculation]
(Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2))
           |
           v
[Proximity Threshold Evaluation]
(Is derived distance 

<img width="487" height="377" alt="2" src="https://github.com/user-attachments/assets/f790587f-81a7-4ba6-b059-fd8131faf4d6" />

### Emergency Alert Triggered (Danger Zone)
Euclidean threshold breach resulting in visual collision warnings (Reference: step3_math.py).

<img width="1797" height="932" alt="Screenshot 2026-10-19 202414" src="https://github.com/user-attachments/assets/9991958a-2502-4f6c-9545-13b3970e5995" />
