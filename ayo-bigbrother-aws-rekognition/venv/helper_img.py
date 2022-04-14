import requests  # import request module


# Get raw image data from a given URL
def get_image_from_url(img_url):
    #   Requests module to get URL
    resp = requests.get(img_url)
    #   Store request contents in img_bytes
    img_bytes = resp.content
    #   return content
    return img_bytes
