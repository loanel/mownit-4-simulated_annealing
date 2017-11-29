import random
import matplotlib.pyplot as plt
import numpy as np
from zad2.neighbors_functions import *
from zad2.energy_functions import *

#draw functions
def show_image_animated(image, figure, size):
    plt.clf()
    subplot = figure.add_subplot(111)
    subplot.set_position([0, 0, 1, 1])
    subplot.set_axis_off()
    subplot.set_xlim(-1, size)
    subplot.set_ylim(-1, size)
    image = list(image)
    x = [pixel[1] for pixel in image]
    y = [pixel[0] for pixel in image]
    subplot.plot(x, y, 's', markersize=640 / size, markerfacecolor='k', markeredgewidth=0)
    figure.canvas.draw()


def show_image(image, size):
    figure = plt.figure(figsize=[8, 8])
    subplot = figure.add_subplot(111)
    subplot.set_position([0, 0, 1, 1])
    subplot.set_axis_off()
    subplot.set_xlim(-1, size)
    subplot.set_ylim(-1, size)
    image = list(image)
    x = [pixel[1] for pixel in image]
    y = [pixel[0] for pixel in image]
    subplot.plot(x, y, 's', markersize=640 / size, markerfacecolor='k', markeredgewidth=0)
    plt.show()


def create_image(size, density):
    set = []
    for i in range(size):
        for j in range(size):
            if density > random.random():
                set.append((i,j))
    return set


#assisting functions for sim_ann process
def get_image_energy(size, current_image, neighbors_function, energy_function):
    sum = 0
    for pixel in current_image:
        sum += energy_function(current_image, pixel, neighbors_function(size, pixel))
    return sum

#i'd rewrite this if i had more time but works for now
#im doing a double swap to on a single object to get its future energy if it were to be changed
#instead i could just create a copy of it and avoid the double swaps and future-not-future calculations
#this is improved in task 3
def get_next_image_energy(size, current_image, pixel_a, pixel_b, current_value, energy_function, neighbors_function):
    image_part = set(neighbors_function(size, pixel_a))
    image_part.union(set(neighbors_function(size, pixel_b)))
    image_part.union({pixel_a, pixel_b})
    old_image_part_energy = 0
    for pixel in image_part:
        old_image_part_energy += energy_function(current_image, pixel, neighbors_function(size, pixel))

    change_pixels(pixel_a, pixel_b, current_image)
    new_image_part_energy = 0
    for pixel in image_part:
        new_image_part_energy += energy_function(current_image, pixel, neighbors_function(size, pixel))
    change_pixels(pixel_a, pixel_b, current_image)
    return current_value - old_image_part_energy + new_image_part_energy


def change_pixels(pixel, pixel_2, image):
    if pixel not in image:
        image.remove(pixel_2)
        image.add(pixel)
    elif pixel_2 not in image:
        image.remove(pixel)
        image.add(pixel_2)


def generate_next_state(size, neighbors_function, image):
    pixel_a = random.sample(image, 1)[0]
    pixel_b = random.sample(neighbors_function(size, pixel_a), 1)[0]
    return pixel_a, pixel_b


def sim_ann(iterations, maximum_temperature,
            neighbors_function, energy_function,
            size, image):
    current_image = image
    best_image = image
    current_value = get_image_energy(size, current_image, neighbors_function, energy_function)
    best_value = current_value
    current_temperature = maximum_temperature

    # fig = plt.figure(figsize=[8, 8])  #uncomment for animation
    # plt.ion()

    for i in range(1, iterations):
        ## this is too complicated, i improved the pattern of the loop in task 3
        pixel_a, pixel_b = generate_next_state(size, neighbors_function, current_image)
        next_value = get_next_image_energy(size, current_image, pixel_a, pixel_b, current_value, energy_function, neighbors_function)
        probabilty = probability_function(maximum_temperature, next_value, current_value, current_temperature)
        if current_value >= next_value or random.random() <= probabilty:
            change_pixels(pixel_a, pixel_b, current_image)
            current_value = next_value
            if best_value > next_value:
                best_image = current_image.copy()
                best_value = next_value
        current_temperature = cooling_function(current_temperature)
        # if i%1000 == 0:
        #     print("Current temp = " + str(current_temperature) + ", current best =  " + str(best_value))
        # #uncomment for animation
        # plt.pause(0.001)
        # show_image_animated(current_image, fig, size)
        # plt.pause(0.001)
    return best_image



def probability_function(max_temp, new_value, old_value, current_temperature):
    return np.exp(max_temp*(old_value - new_value)/current_temperature)


def cooling_function(t):
    return t*0.7


def main():
    n = 100
    density = 0.4
    image = set(create_image(n, density))
    # show_image(image, n)

    maximum_temperature = 15000
    iterations = 50000
    neighbors_function = get_eight_neighbors
    energy_function = energy_two_plus
    result = sim_ann(iterations, maximum_temperature,
                     neighbors_function, energy_function,
                     n, image)
    show_image(result, n)


main()
