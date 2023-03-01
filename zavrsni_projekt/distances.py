import math

def EuclideanDistance(final_coords):
    weights = {}

    for i in range(1, len(final_coords)+1):
        for j in range (i+1, len(final_coords)+1):
                xd = final_coords[i][0] - final_coords[j][0]
                yd = final_coords[i][1] - final_coords[j][1]
                dij = (int)(math.sqrt( xd*xd + yd*yd) + 0.5)
                weights[(i,j)] = dij
    return weights


def ManhattanDistance(final_coords):
    weights = {}

    for i in range(1, len(final_coords)+1):
        for j in range (i+1, len(final_coords)+1):
                xd = abs(final_coords[i][0] - final_coords[j][0])
                yd = abs(final_coords[i][1] - final_coords[j][1])
                dij = (int)(xd + yd + 0.5)
                weights[(i,j)] = dij
    return weights