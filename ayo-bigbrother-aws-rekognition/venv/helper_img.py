import requests  # import request module


# Get raw image data from a given URL
def get_image_from_url(img_url):
    #   Requests module to get URL
    resp = requests.get(img_url)
    #   Store request contents in img_bytes
    img_bytes = resp.content
    #   return content
    return img_bytes


# Get raw image data from a given filename
def get_image_from_file_name(img_file):
    with open(img_file, 'rb') as img_file:
        return img_file.read()
