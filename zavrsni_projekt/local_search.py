
def LocalSearch(tour_local_search, cost_local_search, weights):
        visited_nodes_and_final_cost = []
        updated_tours = []
        updated_tours.append(tour_local_search)
        improvement = True
        while(improvement):
                improvement = False
                for i in range(1, len(tour_local_search)-2):
                        for j in range(i+1, len(tour_local_search)):
                                        curr_cost = []
                                        if j-i == 1: continue
                                        curr_tour = tour_local_search[:]
                                        curr_tour[i:j] = tour_local_search[j-1:i-1:-1]
                        
                                        for m in range(0, len(curr_tour)-1):
                                                if (curr_tour[m], curr_tour[m+1]) in weights.keys():
                                                        curr_cost.append(weights[(curr_tour[m], curr_tour[m+1])])
                                                else:
                                                        curr_cost.append(weights[(curr_tour[m+1], curr_tour[m])])
                                        

                                        if(sum(curr_cost) < sum(cost_local_search)):
                                                tour_local_search = curr_tour[:]
                                                cost_local_search = curr_cost[:]
                                                updated_tours.append(tour_local_search)
                                                improvement = True 

        visited_nodes_and_final_cost.append(updated_tours)
        visited_nodes_and_final_cost.append(sum(cost_local_search))
        #print('\nVisited nodes:\n', tour_local_search)

        return visited_nodes_and_final_cost















