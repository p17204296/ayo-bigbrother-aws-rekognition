import boto3
from pprint import pprint
import helper_img

client = boto3.client('rekognition')

#   image fil/home/ayo/PycharmProjects/ayo-bigbrother-aws-rekognition/ayo-bigbrother-aws-rekognition/venv/bin/pythone
# img_file = 'images/IMG_3974.jpg'

# #   Reference helper_img file
# img_bytes = helper_img.get_image_from_file_name(img_file/home/ayo/PycharmProjects/ayo-bigbrother-aws-rekognition/ayo-bigbrother-aws-rekognition/venv/bin/python)

# #   Detect All labels from the image and collect all attributes
# result = client.detect_faces(Image={'Bytes': img_bytes}, Attributes=['ALL']/home/ayo/PycharmProjects/ayo-bigbrother-aws-rekognition/ayo-bigbrother-aws-rekognition/venv/bin/python)

# #   Print result
# print("View image details below:")

# pprint(result)

# for face in result['FaceDetails']:
#    print(f"Landmarks: {face['Landmarks']}; Confidence Score: {face['Confidence']}")

#   -------- Compare Faces  ------------

#   source image file
source_img_file = 'images/IMG_8908.jpg'

#   target image file
target_img_file = 'images/IMG_0730.jpg' # for a match
# target_img_file = 'images/IMG_0731.jpg' # for no match

#   Reference helper_img file
source_img_bytes = helper_img.get_image_from_file_name(source_img_file)
target_img_bytes = helper_img.get_image_from_file_name(target_img_file)

compare_face_response = client.compare_faces(
    SimilarityThreshold=90,
    SourceImage={'Bytes': source_img_bytes},
    TargetImage={'Bytes': target_img_bytes}
)

pprint(compare_face_response)

if compare_face_response['FaceMatches']:
    for face in compare_face_response['FaceMatches']:
        print(f"\n Similarity Score of source:{ source_img_file} and target:{target_img_file} is: {face['Similarity']}")
else:
    print("no match")
