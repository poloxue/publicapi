import time

from chalice.app import Chalice

from chalicelib.image_service import ImageService

app = Chalice(app_name="publicapi")

start_time = time.time()


@app.route("/")
def index():
    return {"hello": "world"}


@app.route("/uptime", methods=["GET"])
def uptime():
    return f"uptime: {time.time() - start_time}"


image_svc = ImageService()


@app.route("/image/random/{category}", methods=["GET"])
def random_image(category):
    return {"image": image_svc.random_image(category)}
