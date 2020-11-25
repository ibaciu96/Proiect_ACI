from argparse import ArgumentParser
from methodA import MethodA
from methodB import MethodB
from methodC import MethodC
from method import Method
from termcolor import colored
import numpy as np
import os
import threading

A = 'A'
B = 'B'
C = 'C'
METHODS = [A, B, C]
SHAPES = ['ellipse', 'rectangle', 'polygon']


# Thread class
class MyThread(threading.Thread):
    def __init__(self, th_id: int, fitness: str, prob: float, mutation_step: int, genes: float, method_ab: Method):
        """
        Thread init.
        :param th_id: thread id
        :param fitness: genetic algorithm fitness
        :param prob: genetic algorithm probability of mutation
        :param mutation_step: after how many generation the mutation should happen
        :param genes: number of genes to exchange
        :param method_ab: method to use
        """
        super().__init__()
        print(colored('Thread %d initialized with method of type %s' % (th_id, str(type(method_ab))), 'cyan'))
        self.th_id = th_id
        self.f = fitness
        self.p = prob
        self.ms = mutation_step
        self.g = genes
        self.method = method_ab

    def run(self):
        """
        Method run for thread.
        """
        self.method.run(fitness_option=self.f, mutation_probability=self.p, mutation_step=self.ms, changes=self.g, th_number=self.th_id)


def main(file: str, shape_name: str, method_name: str,
         max_pop: int, shapes_no: int, generations_no: int,
         mutation: float, mutation_step: int,
         genes: int, fitness: str, run_all: bool):
    """
    Main function.
    :param file: resource image
    :param shape_name: shape used
    :param method_name: type of method used
    :param max_pop: max populations
    :param shapes_no: max shapes in population
    :param generations_no: max generation
    :param mutation: mutation probability
    :param mutation_step: at how many generations mutation should happen
    :param genes: number of genes to exchange
    :param fitness: fitness type
    :param run_all: run all shapes and methods
    """
    assert shape_name in SHAPES, 'Invalid shape. User rectangle, ellipse or polygon!'
    assert method_name in METHODS, 'Invalid method. Use A or B!'

    if run_all:
        methods = METHODS
        shapes = SHAPES
    else:
        methods = [method_name]
        shapes = [shape_name]

    thread_index = 0
    for _method in methods:
        for _shape in shapes:
            thread_index += 1
            print('Thread - {%d}: Running method %s with shape %s for %d generations!' % (thread_index, _method, _shape, generations_no))
            if _method == A:
                method_abc = MethodA(method_name=_method, original_image_name=file, shapes_type=_shape,
                                    population_size=shapes_no, generations_no=generations_no)
            elif _method == B:
                method_abc = MethodB(method_name=_method, original_image_name=file, shapes_type=_shape,
                                    population_size=max_pop, generations_no=generations_no,
                                    number_of_shapes=shapes_no)
            else:
                method_abc = MethodC(method_name=_method, original_image_name=file, shapes_type=_shape,
                                    population_size=shapes_no, generations_no=generations_no)
                print(type(method_abc))
            MyThread(th_id=thread_index, fitness=fitness, prob=mutation, mutation_step=mutation_step, genes=genes, method_ab=method_abc).start()


# Main call
if __name__ == "__main__":
    np.seterr(divide='ignore', invalid='ignore')
    os.system('rm *.png')

    parser = ArgumentParser()
    parser.add_argument("--file", type=str, default="fallout.png", help="File to read map from.")
    parser.add_argument("--shape", type=str, default="ellipse", help="Type of shape.")
    parser.add_argument("--method", type=str, default="A", help="Method to use.")
    parser.add_argument("--population", type=int, default=300, help="Number of individuals in a population for case B")
    parser.add_argument("--shapes", type=int, default=300, help="Number of shapes in a image or number of individuals in a population for method A.")
    parser.add_argument("--generations", type=int, default=100_000, help="Number of generations.")
    parser.add_argument("--mutation_probability", type=float, default=.4, help="Probability of mutation.")
    parser.add_argument("--mutation_step", type=int, default=1500, help="After how many generation we should mutate.")
    parser.add_argument("--genes_to_change", type=int, default=3, help="Number of genes to exchange.")
    parser.add_argument("--fitness", type=str, default="", help="Fitness method. Deprecated.")
    parser.add_argument("--run_all", type=bool, default=False, help="Run all methods and shapes.")
    args = parser.parse_args()

    main(file=args.file, shape_name=args.shape, method_name=args.method, max_pop=args.population, shapes_no=args.shapes,
         generations_no=args.generations, mutation=args.mutation_probability, mutation_step=args.mutation_step,
         genes=args.genes_to_change, fitness=args.fitness, run_all=args.run_all)