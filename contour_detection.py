import cv2
import numpy as np

# Read the image
image = cv2.imread("glazen.jpeg")

if image is None:
    print("Error: Image not found!")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Optional: Blur to reduce noise before edge detection
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use Canny to detect edges
edges = cv2.Canny(blurred, 20, 50)

# Save and show the edges
cv2.imwrite("glazen_edges.jpg", edges)
cv2.imshow("Edges", edges)

# Find contours
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a copy of the image to draw contours
contour_image = image.copy()

# Draw all contours for visualization
cv2.drawContours(contour_image, contours, -1, (255, 0, 0), 2)

# Save and show the contours
cv2.imwrite("glazen_contours.jpg", contour_image)
cv2.imshow("Contours", contour_image)

# Iterate over all contours
for contour in contours:
    # Compute the bounding box of the contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # Filter out very small boxes (likely noise)
    if w * h > 9000:
        # Draw the rectangle around the contour
        cv2.rectangle(
            image, 
            (x, y), 
            (x + w, y + h), 
            (0, 255, 0), 
            2
        )

        # Place a label with object height
        cv2.putText(
            image,
            f"Object (h = {h}px)",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

# Save and show the output image with detected objects
cv2.imwrite("glazen_contour.jpg", image)
cv2.imshow("Detected Objects", image)

# Wait until a key is pressed, then close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()
