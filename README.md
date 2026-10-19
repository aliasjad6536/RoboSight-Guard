# RoboSight Guard: AI-Powered Workplace Safety & Collision Avoidance System

<img width="913" height="526" alt="image" src="https://github.com/user-attachments/assets/9991958a-2502-4f6c-9545-13b3970e5995" />

## Abstract

RoboSight Guard is a highly optimized, computer vision-based safety system engineered to mitigate the risk of industrial accidents. By ingesting and processing real-time CCTV footage, the system identifies human workers and heavy industrial machinery (specifically forklifts), continuously calculates their spatial Euclidean proximity, and triggers immediate visual and auditory emergency protocols if a predefined safety radius is breached. Developed as a robust solution for the NYLP AI Hackathon 2026, the architecture emphasizes practical deployment, low-latency inference, and real-time hazard mitigation in dynamic environments.

## Problem Statement

Industrial warehouses and construction sites exhibit a high statistical probability of collisions between pedestrians and moving machinery. Conventional CCTV networks serve a purely passive role, heavily reliant on continuous human observation which is prone to fatigue and error. The objective of this research and development phase was to engineer an active, automated AI surveillance layer capable of proactively detecting near-miss events and impending collisions under suboptimal conditions, including camera glare, motion blur, and low-resolution sensor feeds.

## Research & Methodology (System Evolution)

### Phase 1: Custom Model Training & Weights Generation

Initial developmental phases focused on training a specialized YOLOv8 architecture strictly for forklift detection. The model was trained using a custom annotated dataset (`data.yaml`) over 10 epochs to generate the baseline weights.

*Training Configurations and Checkpoint Verification:*

<!-- Yahan apne step4_train.py aur runs/detect folder ke screenshots upload karke <img> tags add karein -->

### Phase 2: Addressing the Domain Gap & Tracking Integration

While the custom model demonstrated high precision on the localized dataset, deployment against raw CCTV feeds revealed a significant "Domain Gap" caused by environmental variance. The architecture was strategically pivoted:

- **Generalized Weights:** Transitioned to a generalized, pre-trained medium architecture (`yolov8m.pt`) for superior feature extraction.
- **ByteTrack Algorithm:** To counter false negatives caused by harsh lighting and partial occlusions, the YOLO ByteTrack algorithm was integrated. This assigned persistent tracking IDs, stabilizing bounding box rendering across consecutive frames.
- **Algorithmic Filtering:** Replaced rigid class dependencies with a dimensional filtering heuristic to identify moving industrial objects while suppressing background noise.

### Phase 3: Web Dashboard Optimization

The backend computer vision pipeline was bridged to a Streamlit frontend for user interaction. To prevent browser rendering latency during high-resolution processing:

- **Resolution Scaling:** Inference resolution was constrained to `imgsz=736`.
- **Temporal Subsampling:** A frame-skipping mechanism was introduced, processing every third frame to maintain real-time performance overhead without sacrificing safety parameters.

## System Architecture Workflow

### Visual Pipeline (Flowchart)

```mermaid
flowchart TD

    %% ---------- STAGE 1 ----------
    subgraph S1["1. INPUT SOURCE"]
        A["CCTV Video Feed<br/>Live Stream / Uploaded Video"]
    end

    %% ---------- STAGE 2 ----------
    subgraph S2["2. PRE-PROCESSING & EXTRACTION"]
        B["Frame Extraction<br/>OpenCV"]
        C["Frame Skipping and Resizing<br/>Every 3rd Frame, imgsz = 736"]
    end

    %% ---------- STAGE 3 ----------
    subgraph S3["3. CORE AI DETECTION & TRACKING"]
        D["YOLOv8 Medium<br/>yolov8m.pt"]
        E["ByteTrack Algorithm<br/>Persistent Tracking IDs"]
        F["Detected Entities<br/>Workers and Forklifts"]
    end

    %% ---------- STAGE 4 ----------
    subgraph S4["4. MATHEMATICAL PROXIMITY ENGINE"]
        G["Centroid Extraction<br/>from Bounding Boxes"]
        H["Euclidean Distance<br/>d = sqrt((x2 - x1)^2 + (y2 - y1)^2)"]
    end

    %% ---------- STAGE 5 ----------
    subgraph S5["5. THRESHOLD EVALUATION"]
        I{"Distance less than<br/>Danger Zone Radius?"}
    end

    %% ---------- STAGE 6 ----------
    subgraph S6["6. BRANCHING LOGIC"]
        J["DANGER: Trigger Emergency Stop<br/>Red Boundary, Warning Text, Audio Beep"]
        K["SAFE: Standard Tracking<br/>Green / Blue Bounding Boxes"]
    end

    %% ---------- STAGE 7 ----------
    subgraph S7["7. FRONTEND OUTPUT"]
        L["Final Frame Rendering"]
        M["Streamlit Web Dashboard<br/>Real-Time Monitoring"]
    end

    %% ---------- FLOW ----------
    A --> B --> C --> D --> E --> F --> G --> H --> I
    I -- "YES (Breach)" --> J
    I -- "NO (Safe)" --> K
    J --> L
    K --> L
    L --> M

    %% ---------- STYLING ----------
    classDef input fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    classDef process fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#4a148c
    classDef ai fill:#e8eaf6,stroke:#283593,stroke-width:2px,color:#1a237e
    classDef math fill:#fff8e1,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef decision fill:#fff3e0,stroke:#ef6c00,stroke-width:3px,color:#bf360c
    classDef danger fill:#ffebee,stroke:#c62828,stroke-width:3px,color:#b71c1c
    classDef safe fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px,color:#1b5e20
    classDef output fill:#e0f7fa,stroke:#00838f,stroke-width:2px,color:#006064

    class A input
    class B,C process
    class D,E,F ai
    class G,H math
    class I decision
    class J danger
    class K safe
    class L,M output

    linkStyle 9 stroke:#c62828,stroke-width:3px
    linkStyle 10 stroke:#2e7d32,stroke-width:3px
```

### Text Workflow

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
(Is derived distance < Danger Zone Radius?)
           |
           +-----------------------+
           |                       |
         [YES]                    [NO]
           |                       |
[Trigger Emergency Stop]  [Maintain Standard Tracking]
(Red Visual Border,       (Render Green/Blue Bounding Boxes)
 Alert Text, Audio Beep)           |
           |                       |
           +-----------------------+
           |
           v
[Frontend Rendering via Streamlit Interface]
```

## Key Features

- **Dual Entity Classification:** Accurately isolates human workers from industrial vehicles within the same temporal frame.
- **Dynamic Spatial Tracking:** Real-time geometric distance tracking between the centroid coordinates of active bounding boxes.
- **Customizable Parameter Controls:** Adjustable threshold for the Danger Zone Radius via the frontend web dashboard.
- **Immediate Hazard Alerting:** Instantaneous visual feedback (thick boundary lines, warning overlays) and auditory alerts upon perimeter breach.
- **Optimized Interactive Dashboard:** A user-friendly Streamlit web interface permitting seamless video uploads and real-time inference monitoring.

## Technology Stack

- **Programming Language:** Python 3.13
- **Computer Vision Framework:** OpenCV
- **Deep Learning Architecture:** PyTorch, YOLOv8 (Ultralytics)
- **Object Tracking:** ByteTrack
- **Frontend Development:** Streamlit
- **Mathematical Operations:** Python Standard Math Library

## Project Structure

```text
RoboSight_Guard/
├── Video/                # Directory containing test CCTV footage
├── dataset/              # Custom dataset and configurations
│   └── data.yaml         # YOLO dataset configuration file
├── runs/                 # YOLOv8 training outputs, graphs, and weights
├── step2_tracking.py     # Initial script for base YOLOv8 object tracking
├── step3_math.py         # Core backend logic for distance and alert triggers
├── step4_train.py        # Script utilized for custom model training phase
├── step5_dashboard.py    # Final Streamlit web application integration
├── yolov8m.pt            # Pre-trained YOLOv8 Medium model weights
└── .gitignore            # Repository exclusion parameters
```

## Challenges and Limitations

- **Hardware Dependency:** The system currently relies on local CPU/GPU processing. Inference speeds are bound by the hardware limitations of the host machine, particularly during real-time 1080p stream analysis.
- **2D Plane Assumption:** Euclidean distance is calculated on a 2D camera plane. Extreme perspective distortion or severely angled cameras may result in skewed distance metrics (e.g., objects appearing closer vertically than they are physically).
- **Severe Occlusion:** If a worker is entirely obscured behind heavy machinery or stacked pallets for extended frames, the tracker may momentarily lose the entity ID until they re-enter the field of view.

## Future Implementations

- **Edge Device Deployment:** Migrating the inference engine to edge computing hardware such as NVIDIA Jetson Nano for localized, low-latency processing without relying on a central server.
- **3D Depth Estimation:** Integrating stereo-vision or depth-mapping models to calculate real-world 3D distance rather than 2D pixel-based distance, significantly improving collision accuracy.
- **Cloud Logging and Analytics:** Automating the capture of near-miss events and logging timestamps, incident snapshots, and frequency metrics to a cloud database (e.g., Firebase or AWS) for managerial safety audits.
- **Multi-Camera Aggregation:** Stitching feeds from multiple warehouse cameras to maintain a singular tracking ID for a worker moving across different zones.

## System Outputs & Visual Documentation

### Standard Tracking (Safe Zone)

Base identification and tracking logic without proximity breach (Reference: `step2_tracking.py`).

<img width="487" height="377" alt="Standard tracking 1" src="https://github.com/user-attachments/assets/528af156-9d39-4014-bd6a-b5d695ef0e6a" />
<img width="913" height="526" alt="Standard tracking 2" src="https://github.com/user-attachments/assets/7a1a9b9d-8c65-4ff4-81d9-e84ffcb8ac15" />
<img width="487" height="377" alt="Standard tracking 3" src="https://github.com/user-attachments/assets/f790587f-81a7-4ba6-b059-fd8131faf4d6" />

### Emergency Alert Triggered (Danger Zone)

Euclidean threshold breach resulting in visual collision warnings (Reference: `step3_math.py`).

<img width="1797" height="932" alt="Danger zone 1" src="https://github.com/user-attachments/assets/59a45117-f581-48d0-b89c-dbeeab7e5dd6" />
<img width="1917" height="922" alt="Danger zone 2" src="https://github.com/user-attachments/assets/14418208-c1fc-43e8-a386-94f41ad176c1" />
<img width="1917" height="995" alt="Danger zone 3" src="https://github.com/user-attachments/assets/c591ea21-dee7-4463-9115-997976b16f87" />
<img width="1917" height="1035" alt="Danger zone 4" src="https://github.com/user-attachments/assets/6a8c46a2-a734-4d6c-8099-29a0c9d03f72" />
<img width="1912" height="1057" alt="Danger zone 5" src="https://github.com/user-attachments/assets/9ea7a843-4e2f-4ebc-9fec-3983859fa499" />
<img width="1917" height="975" alt="Danger zone 6" src="https://github.com/user-attachments/assets/2a423837-cdf6-4821-8206-d79cde4ed966" />
<img width="1142" height="682" alt="Danger zone 7" src="https://github.com/user-attachments/assets/9864ff1f-9aa2-486a-ab75-dddd52163838" />
<img width="1902" height="1016" alt="Danger zone 8" src="https://github.com/user-attachments/assets/7776adf5-0823-462a-8b8f-ea3d2798a53b" />
<img width="1876" height="993" alt="Danger zone 9" src="https://github.com/user-attachments/assets/1cd3f7a0-1fa3-4114-941e-8bf556ade930" />
<img width="1425" height="697" alt="Danger zone 10" src="https://github.com/user-attachments/assets/a07dc044-590c-47a4-ae25-8b1e9294954d" />
<img width="1218" height="785" alt="Danger zone 11" src="https://github.com/user-attachments/assets/23642b0e-fc89-4008-89f2-5f5e0176c2fe" />
<img width="942" height="895" alt="Danger zone 12" src="https://github.com/user-attachments/assets/ab906f39-d105-4848-800d-ffa7eefcd760" />
<img width="1071" height="820" alt="Danger zone 13" src="https://github.com/user-attachments/assets/990ddfbd-44a9-4473-8be8-46dbd1e4b9ae" />
<img width="1442" height="640" alt="Danger zone 14" src="https://github.com/user-attachments/assets/3f4a0956-7e4c-43a1-abce-dbe3cbcc7645" />
<img width="57" height="80" alt="Danger zone 15" src="https://github.com/user-attachments/assets/3acd5889-e3c1-4fd2-ab14-ba0a93b63f18" />

### Web Dashboard Interface

The final production-ready frontend control panel featuring frame-skipping optimizations (Reference: `step5_dashboard.py`).

<img width="183" height="202" alt="Dashboard 1" src="https://github.com/user-attachments/assets/c75685a0-ab39-46be-a68b-c8912d25960d" />
<img width="1797" height="932" alt="Dashboard 2" src="https://github.com/user-attachments/assets/bfb71e5c-1d57-4616-aa89-eaea6be1e26e" />
<img width="1917" height="922" alt="Dashboard 3" src="https://github.com/user-attachments/assets/3f89172f-e631-44b1-bc1e-2e27a6f82f6d" />
<img width="1917" height="995" alt="Dashboard 4" src="https://github.com/user-attachments/assets/9f0e4287-0015-4965-bb0a-dd7663d4b36b" />
<img width="1917" height="1035" alt="Dashboard 5" src="https://github.com/user-attachments/assets/901f2abb-949b-4a37-aff3-fa6dde70a6f2" />
<img width="1912" height="1057" alt="Dashboard 6" src="https://github.com/user-attachments/assets/3166f3f7-1a3c-4973-b0a3-94585f46651f" />
<img width="1917" height="975" alt="Dashboard 7" src="https://github.com/user-attachments/assets/6f7887e2-a15d-4e26-8d2b-89bdd6c5c2b2" />
<img width="1142" height="682" alt="Dashboard 8" src="https://github.com/user-attachments/assets/5de4f046-9de3-4464-aba7-085481c36853" />
<img width="1902" height="1016" alt="Dashboard 9" src="https://github.com/user-attachments/assets/e8077a16-e479-4d9e-aec0-b1bdb04ed7a8" />
<img width="1876" height="993" alt="Dashboard 10" src="https://github.com/user-attachments/assets/6ae3d4c0-88b6-4288-ac1f-09e6c7e85c42" />

---

Developed by **Ali Asjad**
Computer Vision Engineer | BS Artificial Intelligence
