from ultralytics import YOLO

model = YOLO('yolov8m.pt')

if __name__ == '__main__':
    print("Training Shuru Ho Rahi Hai... Powerful i7 CPU par!")
    
    results = model.train(
        data='dataset/data.yaml', 
        epochs=10,       # 10 epochs jaldi ho jayenge
        imgsz=640,       
        batch=4,         # Load kam rakhne ke liye
        device='cpu',    # GPU error bypass karne ke liye
        plots=True       
    )
    
    print("Training Mukammal! Naya model 'runs/detect/train/weights/best.pt' mein save ho gaya hai.")