#!/usr/bin/env python3
from flask import Flask, jsonify, abort, request, make_response, url_for
import tempfile
from keras.preprocessing import image

app = Flask(__name__, static_url_path = "")

def read_image_as_tensor(filename, height, width):
  # CAVEAT: height and width might be swapped; did not verify.
  img = image.load_img(filename, target_size=(height, width))
  img_array = image.img_to_array(img) / 255.
  img_float = img_array.astype('float16')
  img_list = img_float.tolist()
  return img_list
 
@app.route('/pictures/', methods = ['POST'])
def convert_picture():
    picture_binary = request.data
    width = int(request.args.get('height'))
    height = int(request.args.get('width'))

    with tempfile.NamedTemporaryFile() as temp:
        temp.write(picture_binary)
        temp.seek(0)
        temp.flush()
        tensor = read_image_as_tensor(temp.name, height, width)

    return { "tensor": tensor }
    
if __name__ == '__main__':
    app.run(debug = True)