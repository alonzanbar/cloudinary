#!flask/bin/python
from io import StringIO, BytesIO
from flask import Flask, send_file, request
from BL.resize_image import fetch_and_resize

app = Flask(__name__)

@app.route('/thumbnail')
def get_resized_image():
    url = request.args.get('url')
    width = request.args.get('width')
    height = request.args.get('height')
    im = fetch_and_resize(url,width,height)
    return serve_pil_image(im)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)