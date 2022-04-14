import boto3
from pprint import pprint
import helper_img

client = boto3.client('rekognition')

#   image file
img_file = 'images/IMG_0116.JPG'

#   Reference helper_img file
img_bytes = helper_img.get_image_from_file_name(img_file)

#   Detect All labels from the image and collect all attributes
result = client.detect_faces(Image={'Bytes': img_bytes}, Attributes=['ALL'])

#   Print result
print("View image details below:")

pprint(result)

# for face in result['FaceDetails']:
#    print(f"Landmarks: {face['Landmarks']}; Confidence Score: {face['Confidence']}")



