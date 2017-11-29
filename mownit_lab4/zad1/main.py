import matplotlib.pyplot as plt
import numpy as np
import random
import math

#functions for simulated anneal
def value_function(state):
    value = 0
    for i in range(0, len(state)):
        value += np.sqrt(sum((x - y)**2 for x, y in zip(state[i], state[(i+1)%len(state)])))
    return value


def swap_function(state):
    a = random.randint(1, len(state) - 1)
    b = random.randint(1, len(state) - 2)
    if b == a:
        b+=1
    new_state = state[:]
    new_state[a], new_state[b] = new_state[b], new_state[a]
    # second type of swap, uncomment below and comment above to change
    # a = np.random.randint(1, len(state) - 2)
    # new_state = state[:]
    # new_state[a], new_state[a + 1] = new_state[a + 1], new_state[a]
    return new_state


#simulated annealing
def sim_ann(iterations, maximum_temperature, cities):
    current_state = cities
    best_found_state = cities
    current_temperature = maximum_temperature
    anneal_progress = [(0, value_function(current_state))]  #for showing the progress of anneal
    #annealing iterations
    for i in range(0, iterations):
        next_state = swap_function(current_state)
        current_value = value_function(current_state)
        next_value = value_function(next_state)
        probability = probability_function(next_value, current_value, current_temperature, maximum_temperature)
        if current_value > next_value or random.random() < probability:
            current_state = next_state
            anneal_progress.append((i, next_value))
            if value_function(best_found_state) > next_value:
                best_found_state = next_state
        current_temperature = cooling_function(current_temperature)

    anneal_progress.append((iterations, value_function(best_found_state)))
    connect_cities(anneal_progress, 'blue')
    plt.show()
    return best_found_state


#distribution functions
def generate_location_uniform(amount, size):
    x = np.random.uniform(0, size, amount)
    y = np.random.uniform(0, size, amount)
    list = []
    for a in zip(x, y):
        list.append(a)
    return list


def generate_location_gaussian(amount, size):
    x = np.random.normal(0, size, amount)
    y = np.random.normal(0, size, amount)
    list = []
    for a in zip(x, y):
        list.append(a)
    return list


def generate_location_clouds(amount, size):
    mesh_scale = size/12
    list = []
    lower_bound = (1, 5, 9)
    upper_bound = (3, 7, 11)
    pairs = []
    for a in zip(lower_bound, upper_bound):
        pairs.append(a)
    for i in pairs:
        for j in pairs:
            for k in range(0, amount):
                x = random.random()*(i[1]*mesh_scale - i[0]*mesh_scale) + i[0]*mesh_scale
                y = random.random()*(j[1]*mesh_scale - j[0]*mesh_scale) + j[0]*mesh_scale
                list.append((x, y))
    random.shuffle(list)
    return list


#utility functions
def connect_cities(cities, color):
    x, y = zip(*cities)
    plt.plot(x, y, 'ro')
    for i in range(0, len(cities) - 1):
        plt.plot([cities[i][0], cities[(i + 1)][0]], [cities[i][1], cities[(i + 1)][1]], linewidth=1, c=color)


def plot_connect_ends(cities, color):
    i = len(cities) - 1
    plt.plot([cities[i][0], cities[0][0]], [cities[i][1], cities[0][1]], lw=1, c=color)


def probability_function(new_value, old_value, current_temperature, maximum_temperature):
    return np.exp(math.sqrt(maximum_temperature)*(old_value - new_value)/current_temperature)


#cooling parameter
def cooling_function(t):
    return t*0.9995


def main():
    ##setting up parameters for annealing
    iterations = 7000
    highest_temperature = 9000
    points_amount = 20 # total for unform and gaussian, per cloud for 9 cloud distribution
    square_size = 12
    # cities = generate_location_uniform(points_amount, square_size)
    cities = generate_location_gaussian(points_amount, square_size)
    # cities = generate_location_clouds(points_amount, square_size)
    connect_cities(cities, 'green')
    plt.show()
    cities = sim_ann(iterations, highest_temperature, cities)
    connect_cities(cities, 'green')
    plot_connect_ends(cities, 'blue')
    plt.show()

main()