from PIL.Image import Image
from method import do_show_image, Method, MODE, ELLIPSE, RECTANGLE, POLYGON, PIXEL_TH, ZINDEX_TH
from shape import random_shape, Shape, COLOR_MIN_ALPHA, COLOR_MAX_ALPHA
from PIL import Image, ImageDraw, ImageChops
from random import sample
from termcolor import colored
from time import time
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

WIDTH = 0
HEIGHT = 1


# First method: a population is made of shapes.
class MethodC(Method):
    def __fitness__(self, individual: Shape) -> float:
        """
        Fitness function.
        :param individual: the shape on which we compute the fitness value
        :return: fitness value
        """
        shape_image = Image.open('intermediate.png')
        draw_image = ImageDraw.Draw(im=shape_image)

        # Draw shape
        (r, g, b, a) = individual.color.rgba
        if self.shapes_type == ELLIPSE:
            draw_image.ellipse(xy=individual.bounding_box, fill=(r, g, b, a))
        elif self.shapes_type == RECTANGLE:
            draw_image.rectangle(xy=individual.bounding_box, fill=(r, g, b, a))
        elif self.shapes_type == POLYGON:
            draw_image.polygon(xy=individual.vertices, fill=(r, g, b, a))

        # Difference in pixels
        (x1, y1, x2, y2) = individual.bounding_box
        bounding_box = (int(x1), int(y1), int(x2), int(y2))
        diff_image = ImageChops.difference(image1=self.original_image.crop(bounding_box), image2=shape_image.crop(bounding_box)).convert('RGB')

        try:
            return np.square(np.array(diff_image)).sum()
        except ArithmeticError:
            return .0

    def __mutate__(self, individual: Shape, no_attributes_to_change: int = 2) -> Shape:
        """
        Mutate a shape.
        :param individual: mutated shape
        :param no_attributes_to_change: number of attributes to mutate
        """
        individual.mutate(max_width=self.image_width, max_height=self.image_height, no_attributes_to_change=no_attributes_to_change)
        return individual

    def __crossover__(self, individual1: Shape, individual2: Shape, no_attributes_to_change: int = 2) -> (Shape, Shape):
        """
        Crossover genes between two shapes.
        :param individual1: first shame
        :param individual2: second shape
        :param no_attributes_to_change: number of attributes to change between values
        :return: new offsprings
        """
        attributes = sample(range(0, 4), no_attributes_to_change)

        for attribute in attributes:
            if attribute == 0:
                aux = individual1.center
                individual1.center = individual2.center
                individual2.center = aux
            if attribute == 1:
                aux = individual1.color
                individual1.color = individual2.color
                individual2.color = aux
            if attribute == 2:
                aux = individual1.size
                individual1.size = individual2.size
                individual2.size = aux
            if attribute == 3:
                aux = individual1.z_index
                individual1.z_index = individual2.z_index
                individual2.z_index = aux

        return individual1, individual2

    def run(self, fitness_option: str, keep_best: float = .1, changes: int = 2,
            mutation_probability: float = .1, mutation_step: int = 1500, th_number: int = 0):
        """
        Run method.
        :param keep_best: percentage of how many individuals to keep
        :param changes: number of attributes to exchange and mutate
        :param mutation_probability: mutation probability
        :param mutation_step: after how many generation a mutation should happen
        :param fitness_option: type of fitness formula
        :param th_number: thread id
        """
        print('Thread - {%d} -> In method A!' % th_number)
        self.fitness_option = fitness_option

        print(colored('Started generations with shape ' + self.shapes_type, 'blue'))
        input_file_name = self.shapes_type + '_' + self.original_image_name.replace('.png', '')

        # Generate a random population of shapes
        for _ in range(self.population_size):
            shape = random_shape(shape_type=self.shapes_type, max_width=self.image_width, max_height=self.image_height)
            self.population.append(shape)

        self.candidate = self.population
        self.__image__(input_file_name + '_initial_population.png')
        print(colored('Done random generation with shape ' + self.shapes_type, 'green'))

        # Run generations_no generations
        (r, g, b, a) = self.background.rgba
        self.best_image = Image.new(mode=MODE, size=(self.image_width, self.image_height), color=(r, g, b, a))
        self.best_image.save('intermediate.png')
        start = time()
        best_all_time = []
        fitness = np.vectorize(lambda x: self.__fitness__(x))
        for generation in range(1, self.generations_no + 1):
            # Sort based on fitness
            order = np.argsort(fitness(np.array(self.population)), kind='mergesort')
            self.population = list(np.array(self.population)[order])

            individual = self.population.pop(0)
            best_all_time.append(individual)
            self.__image__('intermediate.png', candidates=best_all_time)

            # Evolve
            mp = mutation_probability if generation % mutation_step == 0 else 0
            self.__evolve__(best_no=keep_best, changes_no=changes, mutation_probability=mp)
            # Show partial population
            if do_show_image(g=generation):
                self.candidate = self.population
                self.__image__('intermediate.png', candidates=best_all_time)

            # Tracker
            if generation % 100 == 0:
                self.print_100_time(start=start)
                best_fitness = self.__fitness__(self.population[0])
                worst_fitness = self.__fitness__(self.population[-1])
                print("Thread - {:2} -> Generation: {:10}| Best: {:10.2f}| Worst: {:10.2f}".format(th_number, generation, best_fitness, worst_fitness))

        # Show final result
        self.candidate = self.population
        self.__image__('intermediate.png', candidates=best_all_time)

        print(colored('Done last generation with shape ' + self.shapes_type, 'green'))
