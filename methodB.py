from image import ShapesImage
from method import do_show_image, Method, MODE, ELLIPSE, RECTANGLE, POLYGON, PIXEL_TH
from termcolor import colored
from random import sample, choice
from PIL import Image, ImageDraw, ImageChops
from time import time
import numpy as np


# Second method: a population is made of images with lists of shapes.
class MethodB(Method):
    def __fitness__(self, individual: ShapesImage) -> float:
        """
        Fitness function.
        :param individual: individual on which fitness is made
        :return: fitness value
        """
        (r, g, b, a) = individual.background.rgba
        bkg = Image.new(mode=MODE, size=(self.image_width, self.image_height), color=(r, g, b, a))
        shape_image = Image.new(mode=MODE, size=(self.image_width, self.image_height), color=(r, g, b, a))
        draw_image = ImageDraw.Draw(im=shape_image)

        individual.shapes.sort(key=lambda x: x.z_index)
        for shape in individual.shapes:
            (r, g, b, a) = shape.color.rgba
            if not self.original_image_has_alpha:
                a = 255
            if self.shapes_type == ELLIPSE:
                draw_image.ellipse(xy=shape.bounding_box, fill=(r, g, b, a))
            if self.shapes_type == RECTANGLE:
                draw_image.rectangle(xy=shape.bounding_box, fill=(r, g, b, a))
            if self.shapes_type == POLYGON:
                draw_image.polygon(xy=shape.vertices, fill=(r, g, b, a))
            bkg = Image.alpha_composite(bkg, shape_image)

        diff = ImageChops.difference(image1=self.original_image, image2=bkg).convert('L')
        return (np.array(diff).flatten() < PIXEL_TH).sum()

    def __mutate__(self, individual: ShapesImage, no_attributes_to_change: int = 2) -> ShapesImage:
        """
        Mutation function.
        :param individual: individual to mutate
        :param no_attributes_to_change: number of genes to mutate
        :return: mutated individual
        """
        individual.mutate(max_width=self.image_width, max_height=self.image_height, no_attributes_to_change=2)
        return individual

    def __crossover__(self, individual1: ShapesImage, individual2: ShapesImage, no_attributes_to_change: int = 2) -> (ShapesImage, ShapesImage):
        """
        Crossover between images.
        :param individual1: first image
        :param individual2: second image
        :param no_attributes_to_change: number of genes to mutate if needed
        :return:
        """
        subpop1 = sample(individual1.shapes, int(individual1.size/2))
        subpop2 = sample(individual2.shapes, int(individual2.size/2))
        diffpop1 = list(set(individual1.shapes) - set(subpop1))
        diffpop2 = list(set(individual2.shapes) - set(subpop2))

        individual1.shapes = subpop2[:] + diffpop1[:]
        individual2.shapes = subpop1[:] + diffpop2[:]

        return individual1, individual2

    def run(self, fitness_option: str, keep_best: float = .2, changes: int = 2,
            mutation_probability: float = .1, mutation_step: int = 1500, th_number: int = 0):
        """
        Rum method for method B.
        :param fitness_option: fitness function type
        :param keep_best: percentage of best individuals to keep
        :param changes: number of genes to mutate
        :param mutation_probability: mutation probability
        :param mutation_step: after how many generation a mutation should happen
        :param th_number: thread id
        """
        print('Thread - {%d} -> In method B!' % th_number)
        self.fitness_option = fitness_option
        input_file_name = self.shapes_type + '_' + self.original_image_name.replace('.png', '')

        print(colored('Started generations with shape ' + self.shapes_type, 'blue'))

        # Generate first generation
        for _ in range(self.population_size):
            image = ShapesImage(width=self.image_width, height=self.image_height, shapes_type=self.shapes_type, num_of_shapes=self.number_of_shapes)
            self.population.append(image)

        # Print a random individual in the first generation
        candidate = choice(self.population)
        self.candidate = candidate.shapes
        self.background = candidate.background
        self.__image__(input_file_name + '_initial_population.png')
        print(colored('Done random generation with shape ' + self.shapes_type, 'green'))

        # Start the evolution process
        start = time()
        for generation in range(1, self.generations_no + 1):
            print(generation)
            # Sort by fitness
            self.population.sort(key=lambda x: self.__fitness__(x))

            # Evolve
            self.__evolve__(best_no=keep_best, changes_no=changes, mutation_probability=mutation_probability)

            # Show the best individual if needed
            if do_show_image(g=generation):
                self.candidate = self.population[0].shapes
                self.background = self.population[0].background
                self.__image__(file_name=input_file_name+'_step_%d.png' % generation)

            # Tracker print
            if generation % 100 == 0:
                self.print_100_time(start=start)
                best_fitness = self.__fitness__(self.population[0])
                worst_fitness = self.__fitness__(self.population[-1])
                print("Thread - {:2} -> Generation: {:10}| Best: {:10.2f}| Worst: {:10.2f}".format(th_number, generation, best_fitness, worst_fitness))

        # Print best candidate at the end
        self.candidate = self.population[0].shapes
        self.background = self.population[0].background
        self.__image__(input_file_name + '_final_population.png')

        print(colored('Done last generation with shape ' + self.shapes_type, 'green'))
