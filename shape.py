from termcolor import colored
from random import randint, random, sample, uniform, gauss
from individual import Individual
import numpy as np
import math

BB = [int, int, int, int]
Pixel = (int, int, int, int)
MAX_WH = 50
MIN_WH = 30
COLOR_MIN_ALPHA = 30
COLOR_MAX_ALPHA = 60


# 2D point object.
class Point2D:
    def __init__(self, x: int, y: int):
        """
        Object initializer.
        :param x: x coordinate
        :param y: y coordinate
        """
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """
        String formatter.
        :return: object formatted as string
        """
        return "(x: %d, y: %d)" % (self.x, self.y)


# Color object with RGBA components.
class Color:
    def __init__(self, red: int, green: int, blue: int, alpha: float):
        """
        Object initializer.
        :param red: red value
        :param green: green value
        :param blue: blue value
        :param alpha: alpha value
        """
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __str__(self) -> str:
        """
        String formatter.
        :return: object formatted as string
        """
        return "(r: %d, g: %d, b: %d, a: %.2f)" \
               % (self.red, self.green, self.blue, self.alpha)

    @property
    def rgba(self) -> Pixel:
        """
        Get RGBA components as ints.
        :return: RGBA components
        """
        return self.red, self.green, self.blue, self.alpha

    @staticmethod
    def random_color():
        return Color(red=randint(0, 255),
                     green=randint(0, 255),
                     blue=randint(0, 255),
                     alpha=randint(COLOR_MIN_ALPHA, COLOR_MAX_ALPHA))


# Size object (width and height or major radios and minor radius).
class Size:
    def __init__(self, width: int, height: int):
        """
        Object initializer.
        :param width: width or minor radius
        :param height: height or major radius
        """
        self.width = width
        self.height = height

    def __str__(self) -> str:
        """
        String formatter.
        :return: object formatted as string
        """
        return "(w: %d, h: %d)" % (self.width, self.height)


# Shape object.
class Shape(Individual):
    def __init__(self, center: Point2D, color: Color, size: Size, z_index: float):
        """
        Object initializer.
        :param center: object center
        :param color: object color
        :param size: width and height or minor radius and major radius
        :param z_index: z index of object in figure
        """
        self.name = 'shape'
        self.center = center
        self.color = color
        self.size = size
        self.z_index = z_index
        self.vertices_no = 0
        self.vertices = []
        self.fitness = 0

    def __str__(self) -> str:
        """
        String formatter.
        :return: object formatted as string
        """
        return "Name:\t" + colored(self.name, 'green') + \
               "\nCenter:\t" + str(self.center) + \
               "\nColor:\t" + str(self.color) + \
               "\nSize:\t" + str(self.size) + \
               "\nZ_idx:\t" + str(self.z_index)

    @property
    def bounding_box(self, image_width: int = 256, image_height: int = 256) -> BB:
        """
        Return bounding box of a shape with left-bottom corner and right-top corner.
        :return: bounding box
        """
        if self.name == 'polygon':
            radius = int(math.sqrt((self.size.width/2) ** 2 + (self.size.height/2) ** 2))
            return [max(0, self.center.x - radius), max(0, self.center.y - radius),
                    min(image_width, self.center.x + radius), min(image_height, self.center.y + radius)]
        else:
            return [max(0, self.center.x - self.size.width/2), max(0, self.center.y - self.size.height/2),
                    min(image_width, self.center.x + self.size.width/2), min(image_height, self.center.y + self.size.height/2)]

    def mutate(self, max_width: int, max_height: int, no_attributes_to_change: int = 2):
        """
        Mutate no_attributes_to_change attributes of a shape.
        :param max_width: shape width or minor radius
        :param max_height: shape height or major radius
        :param no_attributes_to_change: number of attributes to mutate
        """
        attributes = [randint(0, 1), randint(0, 1), randint(0, 1), randint(0, 1), randint(0, 1)]

        for idx in range(len(attributes)):
            if idx == 0 and attributes[idx] == 1:
                self.center = Point2D(x=randint(0, max_width), y=randint(0, max_height))
            if idx == 1 and attributes[idx] == 1:
                self.color = Color.random_color()
            if idx == 2 and attributes[idx] == 1:
                self.size.width = randint(MIN_WH, MAX_WH)
            if idx == 3 and attributes[idx] == 1:
                self.size.height = randint(MIN_WH, MAX_WH)
            if idx == 4 and attributes[idx] == 1:
                self.z_index = random()

    @property
    def area(self) -> float:
        """
        Shape area.
        :return: area size
        """
        return self.size.width * self.size.height


# Ellipse shape object.
class Ellipse(Shape):
    def __init__(self, center: Point2D, color: Color, size: Size, z_index: float):
        """
        Object initializer for ellipses.
        :param center: ellipse center
        :param color: ellipse color
        :param size: ellipse size
        :param z_index: ellipse z_index
        """
        super().__init__(center=center, color=color, size=size, z_index=z_index)
        self.name = 'ellipse'

    @property
    def area(self) -> float:
        """
        Ellipse area
        :return: area
        """
        return math.pi * super().area


# Rectangle shape object.
class Rectangle(Shape):
    def __init__(self, center: Point2D, color: Color, size: Size, z_index: float):
        """
        Object initializer for rectangles.
        :param center: rectangle center
        :param color: rectangle color
        :param size: rectangle size
        :param z_index: rectangle z_index
        """
        super().__init__(center=center, color=color, size=size, z_index=z_index)
        self.name = 'rectangle'

    @property
    def area(self) -> float:
        """
        Rectangle area.
        :return: area
        """
        return super().area


# Polygon shape objet.
class Polygon(Shape):
    def __init__(self, center: Point2D, color: Color, size: Size, z_index: float, vertices_no: int):
        """
        Object initializer for polygons.
        :param center: center of polygon
        :param color: color
        :param size: width and height
        :param z_index: z index
        :param vertices_no: number of vertices
        """
        super().__init__(center=center, color=color, size=size, z_index=z_index)
        self.name = 'polygon'
        self.vertices_no = vertices_no
        self.vertices = self.__generate_vertices__()

    def __generate_vertices__(self, spikiness: float = 0.1):
        """
        Generate self.vertices_no vertices for a polygon.
        :param spikiness: how much variance there is in the angular spacing of vertices. [0,1] will map to [0, 2pi/self.vertices_no]
        :return: list of polygon vertices
        """
        irregularity = randint(0, 1)
        radius = int(math.sqrt((self.size.width/2) ** 2 + (self.size.height/2) ** 2))
        irregularity = self.__clip__(irregularity, 0, 1) * 2 * math.pi / self.vertices_no
        spk = self.__clip__(spikiness, 0, 1) * radius

        # generate n angle steps
        angle_steps = []
        lower = (2 * math.pi / self.vertices_no) - irregularity
        upper = (2 * math.pi / self.vertices_no) + irregularity
        sum_v = 0
        for i in range(self.vertices_no):
            tmp = uniform(lower, upper)
            angle_steps.append(tmp)
            sum_v = sum_v + tmp

        # normalize the steps so that point 0 and point n+1 are the same
        k = sum_v / (2 * math.pi)
        for i in range(self.vertices_no):
            angle_steps[i] = angle_steps[i] / k

        # now generate the points
        points = []
        angle = uniform(0, 2 * math.pi)
        for i in range(self.vertices_no):
            r_i = self.__clip__(gauss(radius, spk), 0, 2 * radius)
            x = self.center.x + r_i * math.cos(angle)
            y = self.center.y + r_i * math.sin(angle)
            points.append((int(math.ceil(x)), int(math.ceil(y))))

            angle = angle + angle_steps[i]

        return points

    @staticmethod
    def __clip__(x: float, min_val: int, max_val: int) -> float:
        """
        Clip a value to bounds.
        :param x: value
        :param min_val: lower bound
        :param max_val: upper bound
        :return: bounded value
        """
        if min_val > max_val:
            return x
        elif x < min_val:
            return min_val
        elif x > max_val:
            return max_val
        else:
            return x

    def mutate(self, max_width: int, max_height: int, no_attributes_to_change: int = 2):
        """
        Mutate no_attributes_to_change attributes of a shape.
        :param max_width: shape width or minor radius
        :param max_height: shape height or major radius
        :param no_attributes_to_change: number of attributes to mutate
        """
        change = randint(1, 5)
        attributes = sample(range(0, 5), change)

        for attribute in attributes:
            if attribute == 0:
                self.center = Point2D(x=randint(0, max_width), y=randint(0, max_height))
            if attribute == 1:
                self.color = Color.random_color()
            if attribute == 2:
                self.size.width = randint(MIN_WH, MAX_WH)
                self.size.height = randint(MIN_WH, MAX_WH)
                self.vertices = self.__generate_vertices__()
            if attribute == 3:
                self.z_index = random()

    @property
    def area(self):
        """
        Polygon area approximation.
        :return: area
        """
        xy = list(zip(*self.vertices))
        x = np.array(xy[0])
        y = np.array(xy[1])
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def random_shape(shape_type: str, max_width: int, max_height: int) -> Shape:
    """
    Generate a random shape of given type.
    :param shape_type: shape type
    :param max_width: max width of shape
    :param max_height: max height of shape
    :return: random generated shape
    """
    center = Point2D(x=randint(0,  max_width), y=randint(0, max_height))
    color = Color(red=randint(0, 255),
                  green=randint(0, 255),
                  blue=randint(0, 255),
                  alpha=randint(COLOR_MIN_ALPHA, COLOR_MAX_ALPHA))
    size = Size(width=randint(MIN_WH, MAX_WH), height=randint(MIN_WH, MAX_WH))
    z_index = random()
    if shape_type == 'ellipse':
        return Ellipse(center=center, color=color, size=size, z_index=z_index)
    elif shape_type == 'rectangle':
        return Rectangle(center=center, color=color, size=size, z_index=z_index)
    elif shape_type == 'polygon':
        return Polygon(center=center, color=color, size=size, z_index=z_index, vertices_no=3)
    else:
        assert("Invalid shape")
