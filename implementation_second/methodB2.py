from implementation_second.common2 import *
from implementation_second.methodA2 import mutate_a, mutate_rectangle,generate_init_populationA, drawA

def fitness_funB(target_chrom, population, type_shape='e'):
    new_img = np.zeros(target_chrom.shape)
    shape_img = target_chrom.shape
    parents = sorted(population, key=lambda p: p[4])
    for child in parents:
        if type_shape == 'e':
            rr, cc = ellipse(child[1][0], child[1][1], child[2], child[3], shape_img)
        else:
            rr, cc = rectangle(child[1], child[2], shape_img)
        new_img[rr, cc] = child[0]
    return np.sum(np.abs(target_chrom - new_img))

def cross_overB(parent1, parent2):
    child = parent1[:(POPULATION /2)] + parent2[(POPULATION /2):]
    return child

def mutate_b(child, width, height, type_shape='e'):
    if type_shape == 'e':
        return [mutate_a(shape, width, height) for shape in child]
    else:
        return [mutate_rectangle(shape, width, height) for shape in child]


def evolutionB(parent, img, type_shape):
    #     population.sort(key=lambda p: fitness_funB(img, p))

    #     parents = population[:PARENTS_ELIGIBILITY]
    #     fitness = np.array([-fitness_funB(img, p) for p in population])
    #     fitness = np.interp(fitness, (fitness.min(), fitness.max()), (0, +1))
    #     fitness = fitness / np.sum(fitness)

    #     desired_len = len(population) - len(parents)
    children = []

    for i in range(199):
        print(i)
        child = mutate_b(parent, img.shape[1], img.shape[0], type_shape)
        children.append(child)

    children.sort(key=lambda p: fitness_funB(img, p, type_shape))
    return children[0]


def varB(img_name, type_shape='e'):
    img, size = load_image(img_name)
    shape_img = img.shape
    parent = generate_init_populationA(size[1], size[0], type_shape)

    scores = []
    for g in range(0, GEN):
        print("Gen:", g)
        best = evolutionB(parent, img, type_shape)
        print(g)
        if (g % FREQ == 0):
            #             population.sort(key=lambda p: fitness_funB(img, p))
            drawA(best, img_name, shape_img, g, type_shape)
        parent = best