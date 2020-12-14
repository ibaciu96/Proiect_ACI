from PIL import Image
from implementation_first.individual import Individual
from implementation_first.shape import random_shape
from random import random
from implementation_first.shape import Color

Pixel = (int, int, int, int)
ALPHA = 3


def read_image(image_name: str) -> (bool, (int, int), Image):
    """
    Image reader function.
    :param image_name: name of the image file
    :return: boolean if image has alpha values, image size and full image
    """
    image = Image.open(fp='../ samples/'+image_name, mode='r').convert('RGBA')
    pixels = image.getdata()
    size = image.size
    has_alpha = __has_alpha__(pixels=pixels)

    return has_alpha, size, image


def __has_alpha__(pixels: [Pixel]) -> bool:
    """
    Check if image has multiple alpha values.
    :param pixels: list of pixels
    :return: true or false
    """
    alpha_values = list(set([pixel[ALPHA] for pixel in pixels]))

    if len(alpha_values) == 1:
        return False
    return True


# Images as individuals.
class ShapesImage(Individual):
    def __init__(self, width: int, height: int, shapes_type: str, num_of_shapes: int):
        """
        Object init.
        :param width: image width
        :param height: image height
        :param shapes_type: type if shapes used
        :param num_of_shapes: number of shapes in an image
        """
        self.shapes_type = shapes_type
        self.size = num_of_shapes
        self.width = width
        self.height = height
        self.shapes = [random_shape(shape_type=shapes_type, max_width=width, max_height=height)
                       for _ in range(num_of_shapes)]
        self.background = Color.random_color()

    def mutate(self, max_width: int, max_height: int, no_attributes_to_change: int = 2):
        """
        Mutation function for image.
        :param max_width: max width of shape
        :param max_height: min width of shape
        :param no_attributes_to_change: number of genes to mutate
        """
        if random() < .1:
            self.background = Color.random_color()
        for shape in self.shapes:
            if random() < .1:
                shape.mutate(max_width=max_width, max_height=max_height, no_attributes_to_change=no_attributes_to_change)
