from collections import defaultdict


class Graph:
 
    def __init__(self, vertices):

        self.number_of_nodes = 0
        self.V = vertices
        self.graph = defaultdict(list)
 
    def addEdge(self, v, w):

        self.number_of_nodes +=1
        self.graph[v].append(w)
        self.graph[w].append(v)
 
    def isCyclicUtil(self, v, visited, parent):

        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                if(self.isCyclicUtil(i, visited, v)):
                    return True
            elif parent != i:
                return True
        return False

    def delEdge(self,  u,  v):
     
        for i in range(len(self.graph[u])):
            if (self.graph[u][i] == v):
                self.graph[u].pop(i)
                break
     
        for i in range(len(self.graph[v])):
            if (self.graph[v][i] == u):
                self.graph[v].pop(i)
                break

    def prGraph(self):
     
        for v in range(self.V):
            print("vertex " + str(v), end = ' ')
            for x in self.graph[v]:
                print("-> " + str(x), end = '')
            print()
        print()

    def isCyclic(self):

        visited = [False]*(self.V)
        for i in range(self.V):
            if visited[i] == False:
                if(self.isCyclicUtil
                   (i, visited, -1)) == True:
                    return True
 
        return False


def GreedyAlgorithm(weights, graph_len):
    visited_nodes_and_final_cost = []
    list_of_visited_nodes2 = []
    final_cost2 = []
    g = Graph(graph_len)
    sorted_weights = {k: v for k, v in sorted(weights.items(), key=lambda item: item[1])}
    for key, value in sorted_weights.items():
        if (key[0] not in list_of_visited_nodes2 or key[1] not in list_of_visited_nodes2) and((list_of_visited_nodes2.count(key[0])<2) and (list_of_visited_nodes2.count(key[1]) <2)):
            list_of_visited_nodes2.append(key[0])
            list_of_visited_nodes2.append(key[1])
            final_cost2.append(value)
            g.addEdge(key[0]-1, key[1]-1) 
    for i in range(0, len(list_of_visited_nodes2), 2):
        del sorted_weights[(list_of_visited_nodes2[i], list_of_visited_nodes2[i+1])]



    for key, value in sorted_weights.items():
        g.addEdge(key[0]-1,key[1]-1)
        if(g.isCyclic() !=1) and (list_of_visited_nodes2.count(key[0]) ==1) and (list_of_visited_nodes2.count(key[1])==1):
            list_of_visited_nodes2.append(key[0])
            list_of_visited_nodes2.append(key[1])
            final_cost2.append(value)
        else:
            g.delEdge(key[0]-1,key[1]-1)
    connect = []
    for i in list_of_visited_nodes2:
        if list_of_visited_nodes2.count(i) == 1:
            connect.append(i)


    if (connect[1],connect[0]) in sorted_weights and (connect[0],connect[1]) in sorted_weights:
        if sorted_weights[(connect[0],connect[1])]< sorted_weights[(connect[1],connect[0])]:
            list_of_visited_nodes2.append(connect[0])
            list_of_visited_nodes2.append(connect[1])
            final_cost2.append(sorted_weights[(connect[0],connect[1])])
        else: 
            list_of_visited_nodes2.append(connect[1])
            list_of_visited_nodes2.append(connect[0])
            final_cost2.append(sorted_weights[(connect[1],connect[0])])
    else:
        if (connect[1],connect[0]) in sorted_weights:
            list_of_visited_nodes2.append(connect[1])
            list_of_visited_nodes2.append(connect[0])
            final_cost2.append(sorted_weights[(connect[1],connect[0])])
        else:
            list_of_visited_nodes2.append(connect[0])
            list_of_visited_nodes2.append(connect[1])
            final_cost2.append(sorted_weights[(connect[0],connect[1])])

    visited_nodes_and_final_cost.append(list_of_visited_nodes2)
    visited_nodes_and_final_cost.append(sum(final_cost2))

    return visited_nodes_and_final_cost
