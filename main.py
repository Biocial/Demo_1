import SignUp
import cv2
import numpy as np
import face_recognition

encodeList = SignUp.signup()
classNames = SignUp.cls()

cap = cv2.VideoCapture(0)

while True:
    flag, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faceFrame = face_recognition.face_locations(img)
    faceEncode = face_recognition.face_encodings(img, faceFrame)

    for encodeFace, faceLoc in zip(faceEncode, faceFrame):
        matches = face_recognition.compare_faces(encodeList, encodeFace)
        dis = face_recognition.face_distance(encodeList, encodeFace)
        matchIndex = np.argmin(dis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x1, y2, x2 = faceLoc
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, name, (x2 + 10, y2 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

    cv2.imshow('cam', img)
    cv2.waitKey(1)
