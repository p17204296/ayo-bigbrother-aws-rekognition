import boto3
from pprint import pprint
import helper_img

client = boto3.client('rekognition')

#   image file
img_url = 'https://p17204296.github.io/flexi_hires-front-end/images/videography@1x.jpg'

#   Reference helper_img file
img_bytes = helper_img.get_image_from_url(img_url)

#   Detect All labels from the image
result = client.detect_labels(Image={'Bytes': img_bytes})

#   Print result
pprint("View image details below:")

for label in result['Labels']:
    print(f"Name: {label['Name']}; Confidence Score: {label['Confidence']}")



