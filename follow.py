import cv2
import numpy as np

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Define the lower and upper boundaries of the person's color in HSV
person_lower = np.array([30, 150, 50])
person_upper = np.array([255, 255, 180])

# Function to detect person
def detect_person(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, person_lower, person_upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        return x + w // 2, y + h // 2  # Return center of the person
    return None

# Function to detect obstacles
def detect_obstacles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    obstacles = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        obstacles.append((x, y, w, h))
    return obstacles

def control_robot(person_pos, obstacles):
    # Simple proportional control to follow the person
    if person_pos:
        x, y = person_pos
        if x < 300:
            print("Turn left")
        elif x > 340:
            print("Turn right")
        else:
            print("Move forward")
    else:
        print("Searching for person")
    
    # Avoid obstacles
    for obs in obstacles:
        ox, oy, ow, oh = obs
        if ox < 320:
            print("Obstacle on the left, move right")
        elif ox > 320:
            print("Obstacle on the right, move left")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    person_pos = detect_person(frame)
    obstacles = detect_obstacles(frame)
    control_robot(person_pos, obstacles)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
