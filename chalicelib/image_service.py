import time
import random
import requests
from collections import defaultdict


class ImageService:
    def __init__(self):
        self._sha = None
        self._images = defaultdict(list)

        self._timeout = 60
        self._timestamp = 0

    def last_sha(self):
        last_timestamp = time.time()
        if last_timestamp - self._timestamp < self._timeout:
            return self._sha

        self._timestamp = last_timestamp
        data = requests.get(
            "https://api.github.com/repos/poloxue/public_images/branches/main"
        ).json()
        return data["commit"]["commit"]["tree"]["sha"]

    def get_images(self, category):
        last_sha = self.last_sha()
        if self._sha == last_sha:
            return self._images[category]

        self._images[category] = []
        self._sha = last_sha
        data = requests.get(
            f"https://api.github.com/repos/poloxue/public_images/git/trees/{last_sha}?recursive=1"
        ).json()

        for file in data["tree"]:
            fpath = file["path"]
            subdir = fpath.split("/")[0]
            if fpath.lower().endswith((".png", "jpg", "jpeg", "webp")):
                self._images[subdir].append(
                    f"https://cdn.jsdelivr.net/gh/poloxue/public_images@latest/{file['path']}"
                )
        return self._images[category]

    def random_image(self, category):
        images = self.get_images(category)
        if images:
            return random.choice(images)
