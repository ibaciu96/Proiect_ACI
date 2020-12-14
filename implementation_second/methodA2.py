from implementation_second.common2 import *

def mutate_a(child, width, height):
    """
    """
    rand = random.random()

    if rand <= MUTATION_CHANCE:

        mutate = random.randrange(0, 5)
        if mutate == 0:
            child[mutate] = generate_colour()
            return child
        if mutate == 1:
            child[mutate] = generate_point(width, height)
            return child
        if mutate == 2:
            child[mutate] = generate_dimension(EL_WIDTH)
            return child
        if mutate == 3:
            child[mutate] = generate_dimension(EL_HEIGHT)
            return child
        if mutate == 4:
            child[mutate] = generate_z_index()
            return child
    return child


def mutate_rectangle(child, width, height):
    """
    """
    rand = random.random()

    if rand <= MUTATION_CHANCE:

        mutate = random.randrange(0, 3)
        if mutate == 0:
            child[mutate] = generate_colour()
            return child
        if mutate == 1:
            child[mutate] = generate_point(width, height)
            return child
        if mutate == 2:
            child[mutate] = generate_point(width, height)
            return child
    return child


def cross_overA(parent1, parent2):
    child = []
    indx = np.random.randint(2, size=5)
    parents = [parent1, parent2]
    for atribute in range(5):
        child.append(parents[indx[atribute]][atribute])

    return child

def generate_init_populationA(width, height, shape_type='e'):
    population = []
    if shape_type == 'e':
        for i in range(POPULATION):
            child = []
            child.append(generate_colour())
            child.append(generate_point(width, height))
            child.append(generate_dimension(EL_WIDTH))
            child.append(generate_dimension(EL_HEIGHT))
            child.append(generate_z_index())
            population.append(child)
    else:
        for i in range(POPULATION):
            child = []
            child.append(generate_colour())
            child.append(generate_point(width, height))
            child.append(generate_point(width, height))
            population.append(child)
    return population

def drawA(population, img_name, shape_img, gen, type_shape='e'):
    new_img = np.zeros(shape_img, np.uint8)
    parents = sorted(population, key=lambda p: p[4])
    for child in parents:
        if type_shape == 'e':
            rr, cc = ellipse(child[1][0], child[1][1], child[2], child[3], shape_img)
        else:
            rr, cc = rectangle(child[1], child[2], shape_img)
        new_img[rr, cc] = child[0]
    save_image(new_img, "imgs/" + str(gen) + ".png")


def evolutionA(population, img, type_shape):
    counter = np.zeros(img.shape)
    for p in population:
        rr, cc = ellipse(p[1][0], p[1][1], p[2], p[3], img.shape)
        counter[rr, cc] += 1
    population.sort(key=lambda p: child_fitness(p, img, counter))

    parents = population[:PARENTS_ELIGIBILITY]

    fitness = np.array([child_fitness(p, img, counter) for p in population])

    desired_len = len(population) - len(parents)
    children = []

    for i in range(desired_len):

        [parent1, parent2] = choices(population, weights=fitness, k=2)
        child = cross_overA(parent1, parent2)
        if type_shape == 'e':
            child = mutate_a(child, img.shape[0], img.shape[1])
        else:
            child = mutate_rectangle(child, img.shape[0], img.shape[1])
        children.append(child)

    parents.extend(children)
    return parents


def varA(img_name, type_shape='e'):
    img, size = load_image(img_name)
    shape_img = img.shape
    population = generate_init_populationA(size[0], size[1], type_shape)

    for g in range(0, GEN):
        print("Gen:", g)
        population = evolutionA(population, img, type_shape)
        if (g % FREQ == 0):
            drawA(population, img_name, shape_img, g, type_shape)