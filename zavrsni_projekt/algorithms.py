from nearest_neighbour import cost_nearest_neighbour, tour_nearest_neighbour, NearestNeighbour
from greedy import GreedyAlgorithm
from local_search import LocalSearch
from distances import EuclideanDistance, ManhattanDistance
from file_parser import parse_file
from optimal_solution import parse_opt_file
from generator import generate_coordinates


def choose_algorithm(algorithm, metric, route):

    if algorithm == None or metric == None or route == None:
        return []
    
    if route == 'Generated Route':
        final_coords = generate_coordinates(25)
        opt_dist = 0
    else:
        opt_dist = parse_opt_file(route)
        final_coords = parse_file(route)
    

    graph_len = len(final_coords)
    weights = {}

    if metric == 'L1-metric':
        weights = ManhattanDistance(final_coords)
    if metric == 'L2-metric':
        weights = EuclideanDistance(final_coords)

    info_for_visualization = []
    visited_nodes_and_final_cost = []

    if algorithm == 'Nearest Neighbour':
        ALGORITHM_IN_USE = 'NEAREST NEIGHBOUR'  
        tour_nearest_neighbour.clear()
        cost_nearest_neighbour.clear()
        NearestNeighbour(1, weights, graph_len)
        if (tour_nearest_neighbour[0], tour_nearest_neighbour[-1]) in weights.keys():
            cost_nearest_neighbour.append(weights[(tour_nearest_neighbour[0], tour_nearest_neighbour[-1])])
        else:
            cost_nearest_neighbour.append(weights[(tour_nearest_neighbour[-1], tour_nearest_neighbour[0])])
        tour_nearest_neighbour.append(tour_nearest_neighbour[0])
        best_dst = sum(cost_nearest_neighbour)
        visited_nodes_and_final_cost.clear()
        visited_nodes_and_final_cost.append(tour_nearest_neighbour)
        visited_nodes_and_final_cost.append(best_dst)

    if algorithm == 'Greedy':
        visited_nodes_and_final_cost = GreedyAlgorithm(weights, graph_len)
        ALGORITHM_IN_USE = 'GREEDY ALGORITHM'

    if algorithm == '2-opt':
        ALGORITHM_IN_USE = 'LOCAL SEARCH 2-OPT'
        tour_nearest_neighbour.clear()
        cost_nearest_neighbour.clear()
        NearestNeighbour(1, weights, graph_len)
        if (tour_nearest_neighbour[0], tour_nearest_neighbour[-1]) in weights.keys():
            cost_nearest_neighbour.append(weights[(tour_nearest_neighbour[0], tour_nearest_neighbour[-1])])
        else:
            cost_nearest_neighbour.append(weights[(tour_nearest_neighbour[-1], tour_nearest_neighbour[0])])
        tour_nearest_neighbour.append(tour_nearest_neighbour[0])
        visited_nodes_and_final_cost.clear()
        visited_nodes_and_final_cost = LocalSearch(tour_nearest_neighbour, cost_nearest_neighbour, weights)

    info_for_visualization.append(ALGORITHM_IN_USE)
    info_for_visualization.append(visited_nodes_and_final_cost)
    info_for_visualization.append(final_coords)
    info_for_visualization.append(graph_len)
    info_for_visualization.append(opt_dist)

    return info_for_visualization

    