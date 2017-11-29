def energy_two_plus(image, pixel, neighbors):
    energy = 0
    if pixel not in image:
        return 0
    for neighbor in image.intersection(neighbors):
        if abs(pixel[0] - neighbor[0]) + abs(pixel[1] - neighbor[1]) == 1:
            energy += -1
        else:
            energy += 1
    return energy

def energy_two_cross(image, pixel, neighbors):
    energy = 0
    if pixel not in image:
        return 0
    for neighbor in image.intersection(neighbors):
        if abs(pixel[0] - neighbor[0]) + abs(pixel[1] - neighbor[1]) == 2:
            energy += -1
        else:
            energy += 1
    return energy

def energy_two_column_only(image, pixel, neighbors):
    energy = 0
    if pixel not in image:
        return 0
    for neighbor in image.intersection(neighbors):
        if abs(pixel[0] - neighbor[0]) == 1:
            energy += -1
        else:
            energy += 1
    return energy

#only with 12
def distant_pair(image, pixel, neighbors):
    energy = 0
    if pixel not in image:
        return 0
    for neighbor in image.intersection(neighbors):
        if abs(pixel[0] - neighbor[0]) == 2 or abs(pixel[1] - neighbor[1]) == 2:
            energy += -1
        else:
            energy += 1
    return energy
