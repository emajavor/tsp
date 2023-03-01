import re


def parse_file(file):

    f = open(f".\ALL_tsp.tar\{file}.tsp", "r")
    file = f.read()
    coords = re.search('(?s)(?<=NODE_COORD_SECTION)(.*$)',file)
    list_of_coords = re.split(r'\n',coords[0])

    final_coords = {}


    for element in list_of_coords:
        if element == '' or element == 'EOF':
            continue
        list_of_elements = element.split(' ')
        final_coords[int(list_of_elements[0])] = (int(list_of_elements[1]), int(list_of_elements[2]))

    

    return final_coords




