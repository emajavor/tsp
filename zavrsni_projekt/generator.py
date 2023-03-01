from random import randint

final_coords_generated = {}

def generate_coordinates(n):
    coordinates = []

    while len(coordinates) < n:
        rand = (randint(50, n+450), randint(110,n+300))
        if rand not in coordinates:
            coordinates.append(rand)

    for i in range(1, len(coordinates)+1):
        final_coords_generated[i] = (coordinates[i-1][0], coordinates[i-1][1])
    
    return final_coords_generated


