

class ImageNotFound(Exception):

    def __init__(self, message, image_name):
        super().__init__(f"Image {image_name} not found!")