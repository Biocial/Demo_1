import cv2
import face_recognition
import os
import mysql.connector
from datetime import datetime
from Crypto.Cipher import AES
import hashlib

password = "123456".encode()
key = hashlib.sha256(password).digest()
mode = AES.MODE_CBC
IV = "abcdefghijklmnop"


def pad_message(msg):
    while len(msg) % 16 != 0:
        msg = msg + " "
    return msg


def insertdata(name, encodings):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    name = pad_message(name)

    cipher = AES.new(key, mode, IV)

    con = mysql.connector.connect(host="localhost", user="root", password="", database="python")

    cursor = con.cursor()
    val = (cipher.encrypt(name), float(encodings), dt_string)
    query = "insert into faceencodings values(%s, %s, %s);"
    cursor.execute(query, val)
    con.commit()
    cursor.close()
    con.close()


path = "images"
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    currentImage = cv2.imread(f'{path}/{cl}')
    images.append(currentImage)
    classNames.append(os.path.splitext(cl)[0])


def encoding(images):
    list1 = []
    i = 0
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        i = i + 1
        list1.append(encode)
    return list1


def signup():
    listings = encoding(images)
    i = 0
    for encode in listings:
        insertdata(classNames[i], encode[0])
        i = i + 1

    return listings


def cls():
    return classNames
