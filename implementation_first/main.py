from argparse import ArgumentParser
from implementation_first.methodA import MethodA
from implementation_first.methodB import MethodB
from implementation_first.method import Method
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
    def __init__(self, th_id: int, prob: float, method_ab: Method):
        """
        Thread init.
        :param th_id: thread id
        :param prob: genetic algorithm probability of mutation
        :param method_ab: method to use
        """
        super().__init__()
        print(colored('Thread %d initialized with method of type %s' % (th_id, str(type(method_ab))), 'cyan'))
        self.th_id = th_id
        self.p = prob
        self.g = 3 # deprecated
        self.method = method_ab
        self.f = ""
        self.ms = 1500 # deprecated

    def run(self):
        """
        Method run for thread.
        """
        self.method.run(fitness_option=self.f, mutation_probability=self.p, mutation_step=self.ms, changes=self.g, th_number=self.th_id)


def main(file: str, shape_name: str, method_name: str,
         max_pop: int, shapes_no: int, generations_no: int,
         mutation: float, run_all: bool):
    """
    Main function.
    :param file: resource image
    :param shape_name: shape used
    :param method_name: type of method used
    :param max_pop: max populations
    :param shapes_no: max shapes in population
    :param generations_no: max generation
    :param mutation: mutation probability
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
            else:
                method_abc = MethodB(method_name=_method, original_image_name=file, shapes_type=_shape,
                                    population_size=max_pop, generations_no=generations_no,
                                    number_of_shapes=shapes_no)
                print(type(method_abc))
            MyThread(th_id=thread_index, prob=mutation, method_ab=method_abc).start()


# Main call
if __name__ == "__main__":
    np.seterr(divide='ignore', invalid='ignore')
    os.system('rm *.png')

    parser = ArgumentParser()
    parser.add_argument("--file", type=str, default="flower.jpg", help="File to read map from.")
    parser.add_argument("--shape", type=str, default="rectangle", help="Type of shape.")
    parser.add_argument("--method", type=str, default="A", help="Method to use.")
    parser.add_argument("--population", type=int, default=300, help="Number of individuals in a population for case B")
    parser.add_argument("--shapes", type=int, default=2000, help="Number of shapes in a image or number of individuals in a population for method A.")
    parser.add_argument("--generations", type=int, default=100_000, help="Number of generations.")
    parser.add_argument("--mutation_probability", type=float, default=.1, help="Probability of mutation.")
    parser.add_argument("--run_all", type=bool, default=False, help="Run all methods and shapes.")
    args = parser.parse_args()

    main(file=args.file, shape_name=args.shape, method_name=args.method, max_pop=args.population, shapes_no=args.shapes,
         generations_no=args.generations, mutation=args.mutation_probability, run_all=args.run_all)