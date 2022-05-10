import boto3
from pprint import pprint
from botocore.exceptions import ClientError
from os import environ
import json
import graphical_utils as gu

if __name__ == "__main__":
    #   AWS Region
    region = "us-east-1"
    #   Name of S3 Bucket
    bucket = "big-brother-face-id"
    #   Image filename
    pic = "IMG_0116.jpg"
    #   Collection ID
    collection_id = 'big-brother-collection'
    # Collection ARN: aws:rekognition:us-east-1:171330417321:collection/big-brother-collection - for reference

    #   define client service to use rekognition service
    client = boto3.client('rekognition', region_name=region)


class AWSFaceRecognition:

    # def __init__(self, aConfig, aConfigID, aLogger):
    #     self.configID = aConfigID
    #     self.logger = aLogger

    #     videoanalyticsHome = os.getenv('VIDEO_ANALYTICS_HOME')

    #     # **** ObjectCLassifier config options
    #     logoConfig = aConfig['AWSFaceRecognition']

    # def processFrame(self, aDataBus, aMessageBus):
    #     frame = aDataBus['frame']
    #     detections = aDataBus['detections']

    # ------  Create Collection ID  ------

    def create_collection(collection_id):

        # Create a collection
        print('Creating collection:' + collection_id)
        create_collection_response = client.create_collection(CollectionId=collection_id)
        print('Collection ARN: ' + create_collection_response['CollectionArn'])
        print('Status code: ' + str(create_collection_response['StatusCode']))
        print('Done...')

    #   -- Define response to detect labels with a max of 10 --

    def detect_labels(pic, max_Labels):

        response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': pic}}, MaxLabels=max_Labels)

        #   Print results
        print("Detected labels for " + pic)
        print()   
        for label in response['Labels']:
            print ("Label: " + label['Name'])
            print ("Confidence: " + str(label['Confidence']))
            print ("Instances:")
            for instance in label['Instances']:
                print ("  Bounding box")
                print ("    Top: " + str(instance['BoundingBox']['Top']))
                print ("    Left: " + str(instance['BoundingBox']['Left']))
                print ("    Width: " +  str(instance['BoundingBox']['Width']))
                print ("    Height: " +  str(instance['BoundingBox']['Height']))
                print ("  Confidence: " + str(instance['Confidence']))
                print()

            print ("Parents:")
            for parent in label['Parents']:
                print ("   " + parent['Name'])
            print ("----------")
            print ()
        return len(response['Labels'])

    #   DetectFaces operation to determine if an image captured by the camera is suitable for processing by the SearchFacesByImage operation

    def detect_faces(target_file):

        imageTarget = open(target_file, 'rb')
        detection_count = 0

        response = client.detect_faces(Image={'Bytes': imageTarget.read()},
                                       Attributes=['ALL'])

        print('Detected faces for ' + photo)
        for faceDetail in response['FaceDetails']:

            detection_count = detection_count + 1
            print(f'\nFace Number: {detection_count}')

            print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
                  + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')

            print('Here are the other attributes:')
            print(json.dumps(faceDetail, indent=4, sort_keys=True))

            # Access predictions for individual face details and print them
            faceBoundingBox= faceDetail['BoundingBox']
            print("BoundingBox: " + str(faceBoundingBox))

            faceLandmarks = faceDetail['Landmarks']
            print("Landmarks: " + str(faceLandmarks))

            print("Gender: " + str(faceDetail['Gender']))
            print("Emotions: " + str(faceDetail['Emotions'][0]))

        return len(response['FaceDetails'])

    # ----- Index faces - add faces to a collection ----

    def add_faces_to_collection(pic):

        # Store all image files
        # all_pics = bucket.objects.all()
        # for pic_object in all_pics.objects.all():
        #     print(pic_object.key)

        index_faces_response = client.index_faces(CollectionId=collection_id,
                                                  Image={'S3Object': {'Bucket': bucket, 'Name': pic}},
                                                  ExternalImageId=pic,
                                                  MaxFaces=10,
                                                  QualityFilter="AUTO",
                                                  DetectionAttributes=['ALL'])

        print('Results for ' + pic)

        print('Faces indexed:')
        for faceRecord in index_faces_response['FaceRecords']:
            print('  Face ID: ' + faceRecord['Face']['FaceId'])
            print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

        print('Faces not indexed:')
        for unindexedFace in index_faces_response['UnindexedFaces']:
            print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
            print(' Reasons:')
            for reason in unindexedFace['Reasons']:
                print('   ' + reason)

        return len(index_faces_response['FaceRecords'])

    # ----- Index faces - List faces in a collection ----

    def list_faces_in_collection(max_results):

        # max_results = 10
        faces_count = 0
        tokens = True

        list_faces_response = client.list_faces(CollectionId=collection_id,
                                                MaxResults=max_results)

        print('Faces in collection ' + collection_id)

        while tokens:

            faces = list_faces_response['Faces']

            for face in faces:
                print(face)
                faces_count += 1
            if 'NextToken' in list_faces_response:
                nextToken = list_faces_response['NextToken']
                list_faces_response = client.list_faces(CollectionId=collection_id,
                                                        NextToken=nextToken, MaxResults=max_results)
            else:
                tokens = False
        return faces_count

    # ----- Index faces - Search faces in a collection by images ----

    def search_faces_by_image(input_img, threshold, max_faces):

        search_faces_response = client.search_faces_by_image(CollectionId=collection_id,
                                                             Image={'S3Object': {'Bucket': bucket, 'Name': input_img}},
                                                             FaceMatchThreshold=threshold,
                                                             MaxFaces=max_faces)

        faceMatches = search_faces_response['FaceMatches']
        print('Matching faces')
        for match in faceMatches:
            print('FaceId:' + match['Face']['FaceId'])
            print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            print

        return faceMatches

    # ----- Index faces - Search faces in a collection by faceid ----
    def search_faces_by_face_id(face_id):
        threshold = 10
        max_faces=2
    
        search_faces_response=client.search_faces(CollectionId=collection_id,
                                    FaceId=face_id,
                                    FaceMatchThreshold=threshold,
                                    MaxFaces=max_faces)

                            
        face_matches=search_faces_response['FaceMatches']
        if face_matches:
            print ('Matching faces')
            for match in face_matches:
                    print ('FaceId:' + match['Face']['FaceId'])
                    print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
                    print
            return len(face_matches)
        else:
            print(f"No Matches Found in {collection_id}")

    #  ------ Compare Faces ------

    def compare_face_to_image(source_image, target_image):

        compare_face_response = client.compare_faces(
            SimilarityThreshold=90,
            SourceImage={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': f'{source_image}.jpg',
                },
            },
            TargetImage={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': f'{target_image}.jpg',
                },
            },
        )

        return compare_face_response


#  ------ END OF CLASS ------


# local input image - create a variable to store the filename of the image
photo = 'IMG_0256.jpg'

#  ------ EXAMPLE OF USING THE GRAPHICAL_UTILS ------
# # show the reference faces
print('Showing reference faces')
for face_info in AWSFaceRecognition.list_faces_in_collection(collection_id):
    # pprint(face)
    img_fname = str(face_info['ExternalImageId'])
    img = gu.create_pillow_img(gu.get_image(img_fname))
    gu.draw_box(img, face_info['BoundingBox']).show()

# now we can search faces
# create a variable to store the filename of the image
# img_fname = str(Path(FACE_SEARCH_DIR) / 'IMG_0256.jpg')

print('Searching collection for', photo)

# gu.create_pillow_img(img_fname).show()
# try to find the face in the collection
faces_info = AWSFaceRecognition.search_faces_by_image(photo,)


"""
Faces indexed:
  Face ID: 788054f8-e083-4ccb-b839-9ff024ca5fe7
  Location: {'Width': 0.08978036046028137, 'Height': 0.08837335556745529, 'Left': 0.6578381657600403, 'Top': 0.2394707351922989}
  Face ID: 804d4ad3-722e-4bb6-ae8d-ca42b3847442
  Location: {'Width': 0.08510416746139526, 'Height': 0.0901789739727974, 'Left': 0.2858472764492035, 'Top': 0.25558149814605713}
  Face ID: 1ec59e2a-3aba-42e7-9c5b-30f8bcccd75a
  Location: {'Width': 0.07962249964475632, 'Height': 0.0812126025557518, 'Left': 0.4861559271812439, 'Top': 0.20975834131240845}
  Face ID: 08b86e48-ca8f-428f-9db7-25c506652b86
  Location: {'Width': 0.077255479991436, 'Height': 0.07500091940164566, 'Left': 0.4510369598865509, 'Top': 0.3792579770088196}
Faces not indexed:
"""
# detect_faces_count = AWSFaceRecognition.detect_faces(photo)
# print("Faces detected: " + str(detect_faces_count))

list_faces_in_collection = AWSFaceRecognition.list_faces_in_collection(10)
"""
Faces in collection big-brother-collection
{'FaceId': '189bd6b4-8d85-400c-8e45-84de969141b2', 'BoundingBox': {'Width': 0.10718099772930145, 'Height': 0.21733799576759338, 'Left': 0.6824349761009216, 'Top': 0.06727279722690582}, 'ImageId': 'bf34bf70-4aa2-30e1-9732-d3cd78dfd94b', 'ExternalImageId': 'IMG_0116.jpg', 'Confidence': 99.98519897460938, 'IndexFacesModelVersion': '6.0'}
{'FaceId': '3d396f62-3180-4164-abb2-a25ca26ff85b', 'BoundingBox': {'Width': 0.10439900308847427, 'Height': 0.1935119926929474, 'Left': 0.4539799988269806, 'Top': 0.1475220024585724}, 'ImageId': 'bf34bf70-4aa2-30e1-9732-d3cd78dfd94b', 'ExternalImageId': 'IMG_0116.jpg', 'Confidence': 99.99099731445312, 'IndexFacesModelVersion': '6.0'}
{'FaceId': '7fc006e4-570f-4a4e-a2e6-4ecf1c39ee24', 'BoundingBox': {'Width': 0.11247800290584564, 'Height': 0.2099040001630783, 'Left': 0.19918599724769592, 'Top': 0.11340200155973434}, 'ImageId': 'bf34bf70-4aa2-30e1-9732-d3cd78dfd94b', 'ExternalImageId': 'IMG_0116.jpg', 'Confidence': 99.9822998046875, 'IndexFacesModelVersion': '6.0'}
"""

search_faces_by_face_id = AWSFaceRecognition.search_faces_by_face_id('3d396f62-3180-4164-abb2-a25ca26ff85b')

"""
#   Checks to see if only one face has been detected in the image
if detect_faces_count == 1:
    print("Image suitable for use in collection.")
else:
    print("Please submit an image with only one face.")

# pprint(compare_face_response)

faces_count = AWSFaceRecognition.list_faces_in_collection(collection_id)
print("\n faces count: " + str(faces_count))

indexed_faces_count = AWSFaceRecognition.add_faces_to_collection(bucket, pic, collection_id)
print("Faces indexed count: " + str(indexed_faces_count))

"""