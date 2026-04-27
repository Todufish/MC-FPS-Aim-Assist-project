from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO(r"weights\yolov12\yolo12n.pt")
    model.train(data="data.yaml", 
                epochs=100, 
                batch=4, 
                workers=4 
                )

