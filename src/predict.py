# 评估训练好的模型
from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO(r"runs\detect\train14\weights\best.pt")
    model.predict(r"dataset\test\images", save=True)


