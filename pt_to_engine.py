from ultralytics import YOLO

# Load the YOLO model
model = YOLO("best.pt")

# Export the model
model.export(format="engine")
