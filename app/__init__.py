from flask import Flask, jsonify
from io import BytesIO


from flask import send_file, request, abort

from app.BL.Exceptions import URLNotFound
from app.BL.resize_image import fetch_and_resize
app = Flask(__name__)

#import cloudinary.error_hanlders

@app.route('/thumbnail')
def get_resized_image():
    url = request.args.get('url')
    if not url:
        return abort(400)
    width = request.args.get('width')
    if not width or not width.isnumeric():
        return abort(400)
    height = request.args.get('height')
    if not height or not height.isnumeric():
        return abort(400)
    im = fetch_and_resize(url,int(width),int(height))
    return serve_pil_image(im)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.errorhandler(URLNotFound)
def handle_url_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run(debug=True)