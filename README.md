# My AWS Rekognition Project
To create a video analytics plug-in that performs Face recognition using AWS online “Rekognition” service. The idea would be that a large business could train a cloud based recognition model with the faces of a large number of employees. A camera running edge face detection can be used to detect and identify people in view of the camera. Big Brother Service!!! Applications could be intruder detection that is able to recognise security guards or employees that are permitted to enter a zone.

(1)	Start by building stand along program that can take a cropped image of a face and identify from a group of people. The AWS face recognition service will need training with images of several people so that it can return a Face ID for the person it thinks it can see in the image. I’ve not looked at this at all but if you google “AWS Rekognition face recognition” to get started and see what is involved

(2) Once the stand-along program is working you need to build a pipeline plug-in that does the following
               - Look for face detection bounding boxes in the detection list and get the position and tracking ID
- Keep a dictionary of tracker id values for faces
- For faces with high confidence value do AWS face recognition using a cropped image around the detection
- Retain positive matches in dictionary for that tracked object
- Update label with face ID for as long as that object is tracked
- Throttle number of requests per ID (e.g. wait at least 1 second before trying again)

Recognition should be done asynchronously in background process that updates the lookup table of tracking ID to face ID
