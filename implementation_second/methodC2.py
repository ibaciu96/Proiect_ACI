import copy
import json
import math
import random
import sys
import tempfile

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

MUTATION_CHANCE = 0.9
COLOUR_BLACK = (0, 0, 0, 255)
COLOUR_WHITE = (255, 255, 255, 255)
OFFSET = 10
POLYGONS = 50
POLY_MIN_POINTS = 3
POLY_MAX_POINTS = 5


def generate_z_index():
    return random.random()

def generate_point2(width, height):
    """
    generate random (x,y) coordinates in given range (+offset).
    """
    x = random.randrange(0 - OFFSET, width + OFFSET, 1)
    y = random.randrange(0 - OFFSET, height + OFFSET, 1)
    return (x, y)

def generate_colour2():
    """
    generate random (r,g,b,a) colour.
    """
    red = random.randrange(0, 256)
    green = random.randrange(0, 256)
    blue = random.randrange(0, 256)
    alpha = random.randrange(0, 256)
    #     print ([red, green, blue, alpha])
    return [red, green, blue, alpha]

def mutate_poly(poly, size):
    rand = random.random()

    if rand <= MUTATION_CHANCE:

        mutate = random.randrange(0, 3)
        if mutate == 0:
            print("changing colour")
            idx = random.randrange(0, 4)
            value = random.randrange(0, 256)
            #             print(poly)
            poly[mutate][idx] = value
            return poly
        if mutate == 1:
            print("changing point")
            idx = random.randrange(0, len(poly[1]))
            poly[mutate][idx] = generate_point2(size[0], size[1])
            return poly
        if mutate == 2:
            print("changing z-index")
            poly[mutate] = generate_z_index()
            return poly
    return poly

def draw(child, size, background=COLOUR_BLACK, show=False, save=False,
         generation=None):
    """
    paint all polygons onto an Image and show it.
    """
    img = Image.new('RGB', size, background)
    draw = Image.new('RGBA', size)
    pdraw = ImageDraw.Draw(draw)
    for polygon in child:
        colour = tuple(polygon[0])
        points = polygon[1]
        pdraw.polygon(points, fill=colour, outline=colour)
        img.paste(draw, mask=draw)

    if show:
        img.show()

    if save:
        temp_dir = tempfile.gettempdir()
        temp_name = u"000000{}".format(generation)[-10:]
        out_path = u"{}/{}.png".format(temp_dir, temp_name)
        # img = img.filter(ImageFilter.GaussianBlur(radius=3))
        img.save(out_path)
        print(u"saving image to {}".format(out_path))

    return img

def mutate(child, img_size):
    """
    mutate the individual.
    """
    # pick a random polygon
    #     print(child)
    polygons = copy.deepcopy(child)
    #     print(len(polygons))
    rand = random.randrange(0, len(polygons))

    random_polygon = polygons[rand]
    polygons[rand] = mutate_poly(polygons[rand], img_size)
    return polygons

def fitness(img_1, img_2):
    """
    fitness funtcion determines how much alike 2 images are.
    """
    fitness = 0.0
    for y in range(0, img_1.size[1]):
        for x in range(0, img_1.size[0]):
            r1, g1, b1 = img_1.getpixel((x, y))
            r2, g2, b2 = img_2.getpixel((x, y))
            # get delta per color
            d_r = r1 - r2
            d_b = b1 - b2
            d_g = g1 - g2
            # measure the distance between the colors in 3D space
            pixel_fitness = math.sqrt(d_r * d_r + d_g * d_g + d_b * d_b)
            # add the pixel fitness to the total fitness (lower is better)
            fitness += pixel_fitness
    return fitness

def generate_dna(img_size, dna_size=POLYGONS, fixed_colour=False):
    """
    generate an individual
    """
    polygons = []
    (width, height) = img_size

    for i in range(POLYGONS):
        nr_of_points = random.randrange(POLY_MIN_POINTS, POLY_MAX_POINTS + 1)
        points = []
        for j in range(nr_of_points):
            # generate a point (x,y) in 2D space and append it to points.
            point = generate_point2(width, height)
            points.append(point)

        # generate colour (r,g,b,a) for polygon
        # colour = COLOUR_BLACK if fixed_colour else generate_colour()
        colour = COLOUR_WHITE if fixed_colour else generate_colour2()
        polygon = []
        polygon.append(colour)
        polygon.append(points)
        polygon.append(generate_z_index())
        polygons.append(polygon)

    return polygons

def load_image(path):
    img = Image.open(path)
    return img

def varC(argv):
    path = argv[0]
    img = load_image(path)
    img_size = img.size
    dna = generate_dna(img_size, dna_size=POLYGONS, fixed_colour=False)
    print(dna)
    parent = draw(dna, img_size, show=False)
    fitness_parent = fitness(img, parent)

    generations = pic_nr = 0
    while True:
        dna_mutated = mutate(dna, img_size)
        child = draw(dna, img_size, show=False)
        fitness_child = fitness(img, child)
        if fitness_child < fitness_parent:
            dna = dna_mutated
            fitness_parent = fitness_child
            print(u"picking child w. fitness: {}".format(fitness_child))

        generations += 1
        if generations % 100 == 0:
            print(u"showing generation {}".format(generations))
            pic_nr += 1
            draw(dna, img_size, show=False, save=True, generation=pic_nr)