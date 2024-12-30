import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolo11x.pt")

def predict(chosen_model, img, classes=[], conf=0.5):
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)
    return results

def predict_and_detect(chosen_model, img, classes=[], conf=0.5, rectangle_thickness=2, text_thickness=1):
    results = predict(chosen_model, img, classes, conf=conf)
    for result in results:
        for box in result.boxes:
            # Get the bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # Convert from tensor to numpy
            width = int(x2 - x1)
            height = int(y2 - y1)
            
            # Draw the rectangle (bounding box)
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), rectangle_thickness)
            
            # Prepare the label with the class name and height
            label = f"{result.names[int(box.cls[0])]} ({height} px)"
            
            # Add the label above the bounding box
            cv2.putText(img, label,
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
    return img, results

# Read the image
image = cv2.imread("glazen.jpeg")

# Perform object detection and get the result image
result_img, _ = predict_and_detect(model, image, classes=[], conf=0.5)

# Show the result image
cv2.imshow("Image", result_img)

# Save the result image
cv2.imwrite("glazen_yolo.jpeg", result_img)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
