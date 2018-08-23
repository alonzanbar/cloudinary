from PIL import Image, ImageOps
import requests
from io import BytesIO
from http import HTTPStatus

from app.BL.Exceptions import URLNotFound, InternalServerError


def resize_image(im,w,h):
    desired_size = [w,h]

    old_size = im.size  # old_size[0] is in (width, height) format
    oversize = sum([max(0,desired_size[i]-old_size[i]) for i,x in enumerate(old_size)])
    if oversize>0:
        return im

    ratio  = [float(desired_size[i]) / old_size[i] for i,x in enumerate(old_size)]

    if ratio[0] * old_size[1] > desired_size[1]:
        sel_ratio = ratio[1]
    else:
        sel_ratio = ratio[0]

    new_size = tuple([int(x*sel_ratio) for x in old_size])
    im = im.resize(new_size, Image.ANTIALIAS)

    delta_w = desired_size[0] - new_size[0]
    delta_h = desired_size[1] - new_size[1]
    padding = (delta_w//2, delta_h//2, delta_w-(delta_w//2), delta_h-(delta_h//2))
    new_im = ImageOps.expand(im, padding)
    print (new_size)
    return new_im

def fetch_image(url):
    response = requests.get(url)
    if response.status_code!= HTTPStatus.OK:
        if response.status_code==HTTPStatus.NOT_FOUND:
            raise URLNotFound
        if response.status_code==HTTPStatus.INTERNAL_SERVER_ERROR:
            raise InternalServerError
        response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    return img

def fetch_and_resize(url,w,h):
    im = fetch_image(url)
    return resize_image(im,w,h)

if __name__=='__main__':
    im = fetch_image('https://res.cloudinary.com/demo/image/upload/w_250,h_250,c_mfit/sample.jpg')
    resize_image(im,300,250).show()