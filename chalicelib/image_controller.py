import time
import random
import requests


class ImageController:
    def __init__(self):
        self._sha = None
        self._images = []

        self._timeout = 60
        self._timestamp = 0

    def last_sha(self):
        last_timestamp = time.time()
        if last_timestamp - self._timestamp < self._timeout:
            return self._sha

        self._timestamp = last_timestamp
        data = requests.get(
            "https://api.github.com/repos/poloxue/images/branches/main"
        ).json()
        return data["commit"]["commit"]["tree"]["sha"]

    def get_images(self):
        last_sha = self.last_sha()
        if self._sha == last_sha:
            return self._images

        self._images = []
        self._sha = last_sha
        data = requests.get(
            f"https://api.github.com/repos/poloxue/images/git/trees/{last_sha}"
        ).json()

        for file in data["tree"]:
            fpath = file["path"]
            if fpath.lower().endswith((".png", "jpg", "jpeg")):
                self._images.append(
                    f"https://cdn.jsdelivr.net/gh/poloxue/images@latest/{file['path']}"
                )
        return self._images

    def random_image(self):
        images = self.get_images()
        random_index = random.randint(0, len(images) - 1)
        return images[random_index]
