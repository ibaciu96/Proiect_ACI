from networkx.classes import function
from implementation_first.image import read_image
from PIL import Image, ImageDraw
from implementation_first.individual import Individual
from random import random
from time import time
from termcolor import colored
from implementation_first.shape import Color, Point2D
from copy import deepcopy
from random import randint

WHITE = Color(red=255, green=255, blue=255, alpha=255)
BLACK = Color(red=0, green=0, blue=0, alpha=255)
MODE = 'RGBA'
ELLIPSE = 'ellipse'
RECTANGLE = 'rectangle'
POLYGON = 'polygon'
PIXEL_TH = 1
ZINDEX_TH = .3


def do_show_image(g: int) -> bool:
    """
    Boolean if a image is printed.
    :param g: generation number
    :return: boolean value
    """
    if g in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]:
        return True
    return False


def run_once(f: function) -> function:
    """
    Run once method.
    :param f: function
    :return: wrapper
    """
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


class Method:
    def __init__(self, method_name: str, original_image_name: str, shapes_type: str, population_size: int,
                 generations_no: int, number_of_shapes: int = 0):
        """
        Object initializer.
        :param method_name: method name
        :param original_image_name: image file name
        :param shapes_type: type of shapes used
        :param population_size: number of individuals in populations
        :param generations_no: number of generations
        """
        self.population = []
        self.fitness_option = ''
        self.method_name = method_name
        self.original_image_name = original_image_name
        self.shapes_type = shapes_type
        self.population_size = population_size
        self.generations_no = generations_no
        self.number_of_shapes = number_of_shapes
        self.candidate = None
        self.background = BLACK
        self.__read_image__()

    def __read_image__(self):
        """
        Read image data and set width, height and original pixels.
        """
        a, (w, h), i = read_image(image_name=self.original_image_name)
        self.original_image_has_alpha = a
        self.image_width = w
        self.image_height = h
        self.original_image = i

    def __image__(self, file_name: str, candidates=None):
        """
        Draw image from worst to best and draw image from best to worst.
        :param file_name: name of output file
        """
        """(r, g, b, a) = self.background.rgba
        bkg = Image.new(mode=MODE, size=(self.image_width, self.image_height), color=(r, g, b, a))
        image = Image.new(mode=MODE, size=(self.image_width, self.image_height), color=(r, g, b, a))
        draw_image = ImageDraw.Draw(im=image, mode=MODE)
        shapes = deepcopy(self.candidate) if candidates == None else deepcopy(candidates)

        # shapes.sort(key=lambda x: x.z_index)
        for shape in shapes:
            (r, g, b, a) = shape.color.rgba
            if shape.name == ELLIPSE:
                draw_image.ellipse(xy=shape.bounding_box, fill=(r, g, b, a))
            if shape.name == RECTANGLE:
                draw_image.rectangle(xy=shape.bounding_box, fill=(r, g, b, a))
            if shape.name == POLYGON:
                draw_image.polygon(xy=shape.vertices, fill=(r, g, b, a))
            bkg = Image.alpha_composite(bkg, image)

        bkg.save(self.method_name+'_wtb_'+file_name)"""

        (r, g, b, a) = self.background.rgba
        bkg = Image.new(mode=MODE, size=(self.image_width, self.image_height), color=(r, g, b, a))
        image = Image.new(mode=MODE, size=(self.image_width, self.image_height), color=(r, g, b, a))
        draw_image = ImageDraw.Draw(im=image, mode=MODE)
        shapes = deepcopy(self.candidate) if candidates == None else deepcopy(candidates)
        shapes.reverse()
        for shape in shapes:
            (r, g, b, a) = shape.color.rgba
            if shape.name == ELLIPSE:
                draw_image.ellipse(xy=shape.bounding_box, fill=(r, g, b, a))
            if shape.name == RECTANGLE:
                draw_image.rectangle(xy=shape.bounding_box, fill=(r, g, b, a))
            if shape.name == POLYGON:
                draw_image.polygon(xy=shape.vertices, fill=(r, g, b, a))
            bkg = Image.alpha_composite(bkg, image)

        bkg.save(self.method_name + '_btw_' + file_name)

    @run_once
    def print_100_time(self, start: int):
        """
        Print that will be run once to determine how many seconds 100 generations take.
        :param start: start time
        """
        stop = time()
        print(colored('For 100 generations average time is  %d seconds.' % (stop - start), 'magenta'))

    def __evolve__(self, best_no: float = .2, changes_no: int = 2, mutation_probability: float = .1,
                   image_width: int = None, image_height: int = None):
        """
        Evolve current population.
        :param best_no: percentage of best candidates
        :param changes_no: number of attributes to exchange and number of attributes in case of mutation
        :param mutation_probability: probability of a mutation
        """
        assert not(changes_no < 0 or changes_no > 3), 'Number of changes must be in [0, 3]!'

        # Get best population best_no %
        keep = 0.9
        initial_size = len(self.population)
        new_population = deepcopy(self.population[:int(len(self.population) * keep)])
        """fitnesses = [x.fitness for x in self.population]
        max_fitness = sum(fitnesses)

        while len(new_population) < initial_size:
            point1 = uniform(0, max_fitness)
            point2 = uniform(0, max_fitness)
            index1 = 0
            index2 = 0
            some_sum = 0
            gotIndex1 = False
            gotIndex2 = False
            for index in range(0, len(fitnesses)):
                some_sum += fitnesses[index]
                if some_sum >= point1 and not gotIndex1:
                    index1 = index
                    gotIndex1 = True
                if some_sum >= point2 and not gotIndex2:
                    index2 = index
                    gotIndex2 = True
                if gotIndex1 and gotIndex2: break

            parent1 = deepcopy(self.population[index1])
            parent2 = deepcopy(self.population[index2])

            child1, child2 = self.__crossover__(individual1=parent1, individual2=parent2, no_attributes_to_change=changes_no)
            # Mutation
            if mutation_probability > random():
                child1 = self.__mutate__(individual=child1, no_attributes_to_change=changes_no)
            if mutation_probability > random():
                child2 = self.__mutate__(individual=child2, no_attributes_to_change=changes_no)

            new_population.append(child1)
            new_population.append(child2)

        # Population update
        self.population = deepcopy(new_population)"""

        # Pool for offsprings
        crossover_population = deepcopy(self.population[:int(len(self.population) * keep)])
        copy = deepcopy(self.population)
        # Add one more individual for odd number
        if len(crossover_population) % 2 == 1:
            last = deepcopy(crossover_population[-1])
            crossover_population.append(last)

        while len(new_population) < initial_size:
            index1 = randint(0, len(crossover_population) - 1)
            parent1 = deepcopy(crossover_population[index1])
            index2 = randint(0, len(crossover_population) - 1)
            parent2 = deepcopy(crossover_population[index2])

            # Crossover
            child1, child2 = self.__crossover__(individual1=parent1, individual2=parent2, no_attributes_to_change=changes_no)
            if image_height is not None and image_width is not None:
                child1.center = Point2D(x=randint(0, image_width), y=randint(0, image_height))
                child2.center = Point2D(x=randint(0, image_width), y=randint(0, image_height))
            # Mutation
            if mutation_probability > random():
                child1 = self.__mutate__(individual=child1, no_attributes_to_change=changes_no)
            if mutation_probability > random():
                child2 = self.__mutate__(individual=child2, no_attributes_to_change=changes_no)

            new_population.append(child1)
            new_population.append(child2)

        # Population update
        self.population = deepcopy(new_population)


    def __fitness__(self, individual: Individual) -> float:
        """
        Fitness function.
        :param individual: individual on which fitness is computed
        :return: fitness value
        """
        return .0

    def __mutate__(self, individual: Individual, no_attributes_to_change: int = 2) -> Individual:
        """
        Mutation function.
        :param individual: Individual that will be mutated
        :param no_attributes_to_change: number of mutations that will be made
        :return: mutated individual
        """
        return None

    def __crossover__(self, individual1: Individual, individual2: Individual, no_attributes_to_change: int = 2) -> (Individual, Individual):
        """
        Crossover between 2 individuals
        :param individual1: parent 1
        :param individual2: parent 2
        :param no_attributes_to_change: number of attributes exchanged
        :return: children
        """
        return None, None

    def run(self, fitness_option: str, keep_best: float = .4, changes: int = 2,
            mutation_probability: float = .1, mutation_step: int = 1500, th_number: int = 0):
        """
        Run method for method.
        :param fitness_option: fitness function type
        :param keep_best: percentage of best individuals to keep
        :param changes: number of genes mutated
        :param mutation_probability: mutation probability
        :param mutation_step: after how many generation a mutation should happen
        :param th_number: thread id
        """
        pass
