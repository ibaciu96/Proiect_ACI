# Use this file for methodA2, methodB2 and s methodC2

import matplotlib.pyplot as plt
from skimage.draw import random_shapes
from skimage.draw import ellipse
from skimage.draw import rectangle

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
import numpy as np
import random
from scipy.misc import imsave
from random import choices
import cv2

COLOUR_BLACK = (0, 0, 0, 255)
COLOUR_WHITE = (255, 255, 255, 255)
OFFSET = 10
POLYGONS = 50
POLY_MIN_POINTS = 3
POLY_MAX_POINTS = 5
POPULATION = 2000
POP_B = 50
PARENTS_ELIGIBILITY = 1900
MUTATION_CHANCE = 0.9
FREQ = 10
GEN = 1000000

EL_WIDTH = 20
EL_HEIGHT = 50

def load_image(infilename):
    img = cv2.imread(infilename)
    return img, img.shape

def save_image(img, outfilename):
    cv2.imwrite(outfilename, img)

def generate_z_index():
    return random.random()

def generate_colour():
    """
    generate random (r,g,b) colour.
    """
    return np.random.randint(256, size=3)

def generate_dimension(n):
    return random.randrange(0, n)

def generate_point(width, height):
    """
    generate random (x,y) coordinates in given range
    """
    x = random.randrange(0, width)
    y = random.randrange(0,height)
    return (x, y)


def child_fitness(child, original, cnt, type_shape='e'):
    if type_shape == 'e':
        rr, cc = ellipse(child[1][0], child[1][1], child[2], child[3], original.shape)
    else:
        rr, cc = rectangle(child[1], child[2], original.shape)

    score = 0
    s_np = np.asarray(child[0])
    o_np = np.asarray(original)
    if cnt.shape[0] == 0:
        cnt = np.zeros(original.shape, dtype=np.uint8)
        cnt.fill(1)

    score = np.sum(np.multiply(cnt[rr, cc], np.absolute(np.subtract(o_np[rr, cc], np.tile(s_np, (len(o_np[rr, cc]), 1))))))
    return 1 / score if score != 0 else 1

