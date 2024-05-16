import cv2, threading
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0 
font = cv2.FONT_HERSHEY_SIMPLEX
face_match = False
reference_img = cv2.imread('data/data.jpg')

def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False
        

while True:

    ret, frame = cap.read()

    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(), )).start()
            except ValueError:
                pass
            counter += 1

    if face_match:
        cv2.putText(frame, "Match!", (20, 450), font, 2, (0, 255, 0), 3)
    else:
        cv2.putText(frame, "Not Match!", (20, 450), font, 2, (0, 255, 0), 3)
    cv2.imshow('CAM', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
