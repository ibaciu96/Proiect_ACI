from PIL.Image import Image
from method import do_show_image, Method, MODE, ELLIPSE, RECTANGLE, POLYGON, PIXEL_TH, ZINDEX_TH
from shape import random_shape, Shape, COLOR_MIN_ALPHA, COLOR_MAX_ALPHA
from PIL import Image, ImageDraw, ImageChops
from random import sample
from termcolor import colored
from time import time
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import random

WIDTH = 0
HEIGHT = 1


# First method: a population is made of shapes.
class MethodA(Method):
    def __fitness__(self, individual: Shape) -> float:
        """
        Fitness function.
        :param individual: the shape on which we compute the fitness value
        :return: fitness value
        """
        (r, g, b, a) = self.background.rgba
        shape_image = Image.new(mode=MODE, size=(self.image_width, self.image_height), color=(r, g, b, 0))
        draw_image = ImageDraw.Draw(im=shape_image)

        # Draw shape
        (r, g, b, a) = individual.color.rgba
        a = 255
        if self.shapes_type == ELLIPSE:
            draw_image.ellipse(xy=individual.bounding_box, fill=(r, g, b, a))
        elif self.shapes_type == RECTANGLE:
            draw_image.rectangle(xy=individual.bounding_box, fill=(r, g, b, a))
        elif self.shapes_type == POLYGON:
            draw_image.polygon(xy=individual.vertices, fill=(r, g, b, a))

        # Difference in pixels
        (x1, y1, x2, y2) = individual.bounding_box
        bounding_box = (int(x1), int(y1), int(x2), int(y2))
        image1 = self.original_image.crop(bounding_box)
        image2 = shape_image.crop(bounding_box)
        # image1.alpha_composite(image2)

        diff_image = ImageChops.difference(image1, image2).convert('RGB')

        try:
            return np.sqrt(np.array(diff_image).sum(axis=0)).sum()
        except ArithmeticError:
            return .0

    def __mutate__(self, individual: Shape, no_attributes_to_change: int=2) -> Shape:
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
        value = random.random()
        if value < 0.5:
            aux = individual1.color
            individual1.color = individual2.color
            individual2.color = aux
        if value >= 0.5 and value < 0.75:
            aux = individual1.size
            individual1.size = individual2.size
            individual2.size = aux
        if value > 0.75 and value < 1:
            if individual1.name == POLYGON:
                max_vertices = random.randint(0, individual1.vertices_no + 1)
                fst1 = individual1.vertices[:max_vertices]
                snd1 = individual1.vertices[max_vertices:]
                fst2 = individual2.vertices[:max_vertices]
                snd2 = individual2.vertices[max_vertices:]
                individual1.vertices = fst1 + snd2
                individual2.vertices = fst2 + snd1
                aux = individual1.center
                individual1.center = individual2.center
                individual2.center = aux
            else:
                aux = individual1.center
                individual1.center = individual2.center
                individual2.center = aux
        """aux = individual1.z_index
        individual1.z_index = individual2.z_index
        individual2.z_index = aux"""

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
        self.best_fintesses = []
        self.worst_fitnesses = []
        print('Thread - {%d} -> In method A!' % th_number)
        self.fitness_option = fitness_option

        print(colored('Started generations with shape ' + self.shapes_type, 'blue'))
        input_file_name = self.shapes_type + '_' + self.original_image_name.replace('.png', '')

        # Generate a random population of shapes
        for _ in range(self.population_size):
            shape = random_shape(shape_type=self.shapes_type, max_width=self.image_width, max_height=self.image_height)
            self.population.append(shape)

        self.candidate = deepcopy(self.population)
        self.__image__(input_file_name + '_initial_population.png')
        print(colored('Done random generation with shape ' + self.shapes_type, 'green'))

        # Run generations_no generations
        start = time()
        for generation in range(1, self.generations_no + 1):
            # Sort based on fitness
            self.population.sort(key=lambda x: self.__fitness__(x))

            # Show partial population
            if do_show_image(g=generation):
                self.candidate = deepcopy(self.population)
                self.candidate.reverse()
                self.__image__(file_name=input_file_name+'_step_%d.png' % generation)

            # Tracker
            if generation % 100 == 0:
                self.print_100_time(start=start)
                best_fitness = self.__fitness__(self.population[0])
                worst_fitness = self.__fitness__(self.population[-1])
                print("Thread - {:2} -> Generation: {:10}| Best: {:10.2f}| Worst: {:10.2f}".format(th_number, generation, best_fitness, worst_fitness))

            if generation % 1000 == 0:
                best_fitness = self.__fitness__(self.population[0])
                worst_fitness = self.__fitness__(self.population[-1])
                self.best_fintesses.append(best_fitness)
                self.worst_fitnesses.append(worst_fitness)
                plt.clf()
                plt.plot([1000 * x for x in list(range(0, len(self.best_fintesses)))], self.best_fintesses, label="Best fitness")
                plt.plot([1000 * x for x in list(range(0, len(self.worst_fitnesses)))], self.worst_fitnesses, label="Worst fitness")
                plt.xlabel('Generation no')
                plt.ylabel('Fitness')
                plt.title('Evolution of best and worst fitness')
                plt.legend()
                plt.show()

            # Evolve
            # mp = mutation_probability if generation % mutation_step == 0 else 0
            self.__evolve__(best_no=keep_best, changes_no=changes, mutation_probability=mutation_probability,
                            image_width=self.image_width, image_height=self.image_height)

        # Show final result
        self.candidate = deepcopy(self.population)
        self.candidate.reverse()
        self.__image__(input_file_name + '_final_population.png')

        print(colored('Done last generation with shape ' + self.shapes_type, 'green'))
