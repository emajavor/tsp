import re

def parse_opt_file(file):

    f_opt = open(f".\ALL_tsp.tar\{file}.opt.tour", "r")
    file_opt = f_opt.read()
    #opt_nodes = re.search('(?s)(?<=TOUR_SECTION)(.*$)',file_opt)
    distance_to_filter = re.search('(COMMENT).*\(.*?(\d+)',file_opt)

    opt_distance = distance_to_filter[2]
    # list_to_filter = re.split(r'\n',opt_nodes[0])

    # list_of_nodes_opt = []

    # for node in list_to_filter:
    #     if node == '' or node == 'EOF' or node == '-1':
    #         continue
    #     list_of_nodes_opt.append(int(node))

    return opt_distance


# list_of_nodes_opt -> ako zelimo i nacrtati optimalnu rutu