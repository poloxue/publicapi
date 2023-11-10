import time

from chalice.app import Chalice

from chalicelib.image_controller import ImageController

app = Chalice(app_name="publicapi")

start_time = time.time()


@app.route("/")
def index():
    return {"hello": "world"}


@app.route("/uptime", methods=["GET"])
def uptime():
    return f"uptime: {time.time() - start_time}"


image_ctrl = ImageController()


@app.route("/image/random", methods=["GET"])
def random_image():
    return {"image": image_ctrl.random_image()}
