import cv2 as cv #imprt openCV

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

        cv.imshow('Video',frame)

        if cv.waitKey(20) & 0xFF == ord('d'):
            break

    capture.release()
    cv.destroyAllWindows()

# read_vid('video/VID_0226.mp4')


#Resize IMG

#Crop IMG
def crop_img(photo:str, top:int, bottom:int, left:int, right:int):

    cv_photo = cv.imread(photo)
    
    # region = photo[x,y]
    cropped = cv_photo[top:bottom, left:right]

    cv.imshow(f'Original image of {photo}', cv_photo)
    cv.imshow(f'Cropped image of {photo}', cropped)

    cv.waitKey(0)

# crop_img (test_img, 15, 200, 300, 600)
crop_img (test_img, 15, 200, 100, 310)

#{'BoundingBox': {'Width': 0.10718099772930145, 'Height': 0.21733799576759338, 
# 'Left': 0.6824349761009216, 'Top': 0.06727279722690582}
