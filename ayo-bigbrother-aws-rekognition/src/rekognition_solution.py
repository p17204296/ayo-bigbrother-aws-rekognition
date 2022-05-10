import boto3
from pprint import pprint
from botocore.exceptions import ClientError
from os import environ
import json

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

    def add_faces_to_collection(bucket, pic, collection_id):

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

    def list_faces_in_collection(collection_id, max_results):

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

    def search_faces(input_img, threshold, max_faces):

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


# local input image
photo = 'images/IMG_0256.jpg'

detect_faces_count = AWSFaceRecognition.detect_faces(photo)
print("Faces detected: " + str(detect_faces_count))

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