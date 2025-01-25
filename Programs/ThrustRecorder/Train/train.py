from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolo11n.pt")

    model.train(data=".\\Train\\dataset\\data.yaml", epochs=400, batch=16, workers=8, device='cuda')