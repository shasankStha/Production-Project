from ultralytics import YOLO

model = YOLO('yolov8n.pt')

def trainLivelinessModel():
    model.train(data="DataSet/SplitData/data.yaml", epochs=10)

if __name__ == '__main__':
    trainLivelinessModel()