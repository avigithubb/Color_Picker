from flask import Flask, render_template, request, url_for
import numpy as np
from PIL import Image
from datetime import datetime
import os
import base64
from io import BytesIO


app = Flask(__name__)

def np_array_to_hex2(array):
    array = np.asarray(array, dtype='uint32')
    array = (1 << 24) + ((array[:, :, 0]<<16) + (array[:, :, 1]<<8) + array[:, :, 2])
    return [hex(x)[-6:] for x in array.ravel()]

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/show_color", methods=["GET", "POST"])
def show():
    if "img-file" not in request.files:
        return "No file is uploaded", 404
    img = request.files["img-file"]

    if img.filename == '':
        print("No file")
        return render_template("index.html")

    year = datetime.now().year

    my_img = Image.open(img)
    no_of_colors = request.form.get("ncolors")
    delta = request.form.get("delta")


    img_arr = np.array(my_img)
    nunique = img_arr.reshape(-1, img_arr.shape[2])
    more_unique = np.unique(nunique, axis=0)
    if delta == "":
        required_arr = (more_unique // 24) * 24
    else:
        required_arr = (more_unique // int(delta)) * int(delta)
    required_unique = np.unique(required_arr, axis=0)
    new_arr = []
    for i in range(len(required_unique)):
        new_arr.append([required_unique[i]])

    if no_of_colors == "":
        final_arr = np.array(new_arr[:10])
    else:
        final_arr = np.array(new_arr[:int(no_of_colors)])

    temp_img_path = os.path.join('static', 'temp_img.png')
    my_img.save(temp_img_path)

    hex_arr = np_array_to_hex2(final_arr)
    rgb = []
    for item in final_arr:
        rgb.append(tuple(item[0]))

    return render_template("index.html", img_colors=hex_arr, rgb=rgb, img_path=temp_img_path, year=year)

if __name__ == "__main__":
    app.run(debug=True)