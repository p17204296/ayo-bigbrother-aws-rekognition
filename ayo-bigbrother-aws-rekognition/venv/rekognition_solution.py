import boto3
from pprint import pprint

if __name__ == "__main__":
    #   Name of S3 Bucket
    bucket = "shinaalukoayo.tech"
    #   Image filename
    pic = "IMG_0731.JPG"

#   define client service to use rekognition service
client = boto3.client('rekognition')

#   Define response to detect labels with a max of 10
response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': pic}}, MaxLabels=10)

#   Print results
print("Detected labels for " + pic)

pprint(response)
