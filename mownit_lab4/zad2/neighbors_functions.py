def get_four_neighbors(size, pixel):

    row, column = pixel

    #plus
    neighbors = set()
    if row > 0:
        neighbors.add((row-1, column))
    if row < size - 1:
        neighbors.add((row+1, column))
    if column > 0:
        neighbors.add((row, column-1))
    if column < size - 1:
        neighbors.add((row, column+1))
    return neighbors


def get_eight_neighbors(size, pixel):
    row, column = pixel

    #square 3x3
    neighbors = set()
    if row > 0:
        for col in range(max(column-1, 0), min(column+2, size)):
            neighbors.update({(row-1, col)})
    if row < size - 1:
        for col in range(max(column-1, 0), min(column+2, size)):
            neighbors.update({(row+1, col)})

    for col in range(max(column-1, 0), min(column+2, size)):
        if(row, col) != pixel:
            neighbors.update({(row, column)})

    return neighbors


def get_twelve_neighbors(size, pixel):
    row, column = pixel

    #rhombus 3x3
    neighbors = get_eight_neighbors(size, pixel)
    if row > 1:
        neighbors.add((row-2, column))
    if row < size - 2:
        neighbors.add((row+2, column))
    if column > 1:
        neighbors.add((row, column-2))
    if column < size - 2:
        neighbors.add((row, column+2))
    return neighbors
