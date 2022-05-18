import face_recognition
import cv2
import time
import pickle
import imutils
import cv2 as cv  # imprt openCV
import os

# https://www.youtube.com/watch?v=oXlwWbU8l2o&ab_channel=freeCodeCamp.org

test_img = 'images/IMG_0116.jpg'
test_vid = 'video/VID_0226.mp4'

# Read IMG Files


def read_img(photo):

    img = cv.imread(photo)

    cv.imshow('Me', img)

    cv.waitKey(0)

# read_img('images/IMG_0116.jpg')

# Read VID Files


def read_vid(video):
    capture = cv.VideoCapture(video)

    while True:
        isTrue, frame = capture.read()

        cv.imshow('Video', frame)

        if cv.waitKey(20) & 0xFF == ord('d'):
            break

    capture.release()
    cv.destroyAllWindows()

# read_vid('video/VID_0226.mp4')


# Resize IMG

# Crop IMG
def crop_img(photo: str, top: int, bottom: int, left: int, right: int):

    cv_photo = cv.imread(photo)

    # region = photo[x,y]
    cropped = cv_photo[top:bottom, left:right]

    cv.imshow(f'Original image of {photo}', cv_photo)
    cv.imshow(f'Cropped image of {photo}', cropped)

    cv.waitKey(0)

# crop_img (test_img, 15, 200, 300, 600)
# crop_img (test_img, 15, 200, 100, 310)

# {'BoundingBox': {'Width': 0.10718099772930145, 'Height': 0.21733799576759338,
# 'Left': 0.6824349761009216, 'Top': 0.06727279722690582}
# -Jon example


# find path of xml file containing haarcascade file
cascPathface = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
# load the harcaascade in the cascade classifier
faceCascade = cv2.CascadeClassifier(cascPathface)
# load the known faces and embeddings saved in last file
data = pickle.loads(open('face_enc', "rb").read())

print("Streaming started")
video_capture = cv2.VideoCapture(0)
# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)

    # convert the input frame from BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # the facial embeddings for face in input
    encodings = face_recognition.face_encodings(rgb)
    names = []
    # loop over the facial embeddings incase
    # we have multiple embeddings for multiple fcaes
    for encoding in encodings:
       # Compare encodings with encodings in data["encodings"]
       # Matches contain array with boolean values and True for the embeddings it matches closely
       # and False for rest
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding)
        # set name =inknown if no encoding matches
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            # Find positions at which we get True and store them
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                # Check the names at respective indexes we stored in matchedIdxs
                name = data["names"][i]
                # increase count for the name we got
                counts[name] = counts.get(name, 0) + 1
            # set name which has highest count
            name = max(counts, key=counts.get)

        # update the list of names
        names.append(name)
        # loop over the recognized faces
        for ((x, y, w, h), name) in zip(faces, names):
            # rescale the face coordinates
            # draw the predicted face name on the image
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()


"""


cascPath=os.path.dirname(cv.__file__)+"/data/haarcascade_frontalface_default.xml"

def openCVLiveCapture():

    faceCascade = cv.CascadeClassifier(cascPath)
    video_capture = cv.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        ret, frames = video_capture.read()
        gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv.CASCADE_SCALE_IMAGE
        )
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Display the resulting frame
        cv.imshow('Video', frames)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()


"""

"""
rassp pie

import numpy as np
import cvcap = cv.VideoCapture(0)
    capture = cv.VideoCapture(video)

cap.set(3,640) # set Width
cap.set(4,480) # set Heightwhile(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1) # Flip camera vertically
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        breakcap.release()
cv2.destroyAllWindows()


"""
