
tour_nearest_neighbour = []
cost_nearest_neighbour = []


def NearestNeighbour(node, weights, graph_len):
    
    weights_from_certain_node = {}
    if len(tour_nearest_neighbour) >= graph_len:
        return

    for key, value in weights.items():
        if (key[0] == node and key[1] not in tour_nearest_neighbour) or (key[1] == node and key[0] not in tour_nearest_neighbour):
            weights_from_certain_node[(key[0], key[1])] = value

    tour_nearest_neighbour.append(node)

    if len(tour_nearest_neighbour) != graph_len:
        closest_nodes = min(weights_from_certain_node, key=weights_from_certain_node.get)
        cost = weights_from_certain_node[closest_nodes]
        cost_nearest_neighbour.append(cost)

        if closest_nodes[0] == node:
            NearestNeighbour(closest_nodes[1], weights, graph_len)
        NearestNeighbour(closest_nodes[0], weights, graph_len)