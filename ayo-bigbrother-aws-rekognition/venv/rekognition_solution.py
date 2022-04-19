import boto3
from pprint import pprint
from botocore.exceptions import ClientError
from os import environ

if __name__ == "__main__":
    #   Name of S3 Bucket
    bucket = "big-brother-face-id"
    #   Image filename
    pic = "IMG_0116.jpg"
    #   Collection ID
    collection_id = 'big-brother-collection'
    # Collection ARN: aws:rekognition:us-east-1:171330417321:collection/big-brother-collection - for reference

#   define client service to use rekognition service
client = boto3.client('rekognition')


# ------  Create Collection ID  ------

def create_collection(collection_id):
    client = boto3.client('rekognition')

    # Create a collection
    print('Creating collection:' + collection_id)
    create_collection_response = client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + create_collection_response['CollectionArn'])
    print('Status code: ' + str(create_collection_response['StatusCode']))
    print('Done...')


# create_collection(collection_id)  # - Only need to do this once

#   -- Define response to detect labels with a max of 10 --
# response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': pic}}, MaxLabels=10)

# #   Print results
# print("Detected labels for " + pic)

# pprint(response)


#  ------ Compare Faces ------

# compare_face_response = client.compare_faces(
#     SimilarityThreshold=90,
#     SourceImage={
#         'S3Object': {
#             'Bucket': bucket,
#             'Name': 'IMG_8908.jpg',
#         },
#     },
#     TargetImage={
#         'S3Object': {
#             'Bucket': bucket,
#             'Name': 'IMG_0730.jpg',
#         },
#     },
# )

# pprint(compare_face_response)


# ----- Index faces - add faces to a collection ----
""""
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


indexed_faces_count = add_faces_to_collection(bucket, pic, collection_id)
print("Faces indexed count: " + str(indexed_faces_count))

"""

"""
COMMENT:

Results for IMG_0116.jpg
Faces indexed:
  Face ID: 7fc006e4-570f-4a4e-a2e6-4ecf1c39ee24
  Location: {'Width': 0.11247807741165161, 'Height': 0.2099042683839798, 'Left': 0.19918620586395264, 'Top': 0.113402359187603}
  Face ID: 189bd6b4-8d85-400c-8e45-84de969141b2
  Location: {'Width': 0.1071811318397522, 'Height': 0.21733839809894562, 'Left': 0.6824353933334351, 'Top': 0.0672728419303894}
  Face ID: 3d396f62-3180-4164-abb2-a25ca26ff85b
  Location: {'Width': 0.10439929366111755, 'Height': 0.19351239502429962, 'Left': 0.45397958159446716, 'Top': 0.14752231538295746}
Faces not indexed:
Faces indexed count: 3

"""


# ----- Index faces - List faces in a collection ----

def list_faces_in_collection(collection_id):
    maxResults = 10
    faces_count = 0
    tokens = True

    list_faces_response = client.list_faces(CollectionId=collection_id,
                                            MaxResults=maxResults)

    print('Faces in collection ' + collection_id)

    while tokens:

        faces = list_faces_response['Faces']

        for face in faces:
            print(face)
            faces_count += 1
        if 'NextToken' in list_faces_response:
            nextToken = list_faces_response['NextToken']
            list_faces_response = client.list_faces(CollectionId=collection_id,
                                                    NextToken=nextToken, MaxResults=maxResults)
        else:
            tokens = False
    return faces_count


faces_count = list_faces_in_collection(collection_id)
print("\n faces count: " + str(faces_count))


# ----- Index faces - Search faces in a collection by images ----

input_img='IMG_0730.jpg'
threshold = 70
maxFaces=10

search_faces_response=client.search_faces_by_image(CollectionId=collection_id,
                            Image={'S3Object':{'Bucket':bucket,'Name':input_img}},
                            FaceMatchThreshold=threshold,
                            MaxFaces=maxFaces)
                            
faceMatches=search_faces_response['FaceMatches']
print ('Matching faces')
for match in faceMatches:
        print ('FaceId:' + match['Face']['FaceId'])
        print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print
