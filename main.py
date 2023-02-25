# Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
# face_utils for basic operations of conversion
from imutils import face_utils
from playsound import playsound
# Initializing the camera and taking the instance
Vid = cv2.VideoCapture(0)

# Initializing the face detector and landmark detector
front_face = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# status marking for current state
sleep = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)
face_frame = 0
# below code has a numpy linear algebra function which calculates the euclidean distance between two points
def Euc_distance(ptA, ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist

# Here the blinked function is used to detect that if the eye is closed or open
def blinked(a, b, c, d, e, f):
    up = Euc_distance(b, d) + Euc_distance(c, e)
    down = Euc_distance(a, f)
    ratio = up / (2.0 * down)

    # Checking if it is blinked
    if (ratio > 0.25):
        return 2
    elif (ratio > 0.21 and ratio <= 0.25):
        return 1
    else:
        return 0


while True:
    _, frame = Vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = front_face(gray)
    # detected face in faces array
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        landmarks = dlib_facelandmark(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # The numbers are actually the landmarks which will show eye
        left_blink = blinked(landmarks[36], landmarks[37],
                             landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43],
                              landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # Now judge what to do for the eye blinks
        if (left_blink == 0 or right_blink == 0):
            sleep += 1
            drowsy = 0
            active = 0
            if (sleep > 25):
                status = "SLEEPING !!!"
                color = (255, 0, 0)
                playsound('Sleeping alarm.wav')
        elif (left_blink == 1 or right_blink == 1):
            sleep = 0
            active = 0
            drowsy += 1
            if (drowsy > 20):
                status = "Drowsy !"
                color = (0, 0, 255)
                playsound('Drowsy alarm 1.wav')
        else:
            drowsy = 0
            sleep = 0
            active += 1
            if (active > 10):
                status = "Active :)"
                color = (0, 255, 0)

        cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 0), -1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Result of detector", face_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
