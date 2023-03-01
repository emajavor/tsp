import pygame_widgets
import pygame
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
from asyncore import write

from algorithms import choose_algorithm
import os
pygame.init()


WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSP visualization!")
pygame_icon = pygame.image.load('.\Assets\pin.png')
pygame.display.set_icon(pygame_icon)

SOLVING_COLOR = (240, 240, 240)
SOLVING_FONT = pygame.font.SysFont('corbel', 40)
DISTANCE_FONT = pygame.font.SysFont('corbel', 30)
LINE_COLOR = (230, 230, 230)

DARK_BLUE = (21,20,60)

LOCATION_IMAGE = pygame.image.load(
    os.path.join('Assets', 'pin.png'))
LOCATION_PIN = pygame.transform.scale(
    LOCATION_IMAGE, (40, 40))
LOCATION_IMAGE2 = pygame.image.load(
    os.path.join('Assets', 'starting_pin.png'))
STARTING_PIN = pygame.transform.scale(
    LOCATION_IMAGE2, (40, 40))

image_map = pygame.image.load('.\Assets\map.png')

dropdown_alg = Dropdown(
    WIN, 20, 10, 145, 40, name='Algorithm          ▼',
    choices=[
        'Greedy',
        'Nearest Neighbour',
        '2-opt',
    ],
    borderRadius=3, colour=pygame.Color('light blue'), values=['Greedy', 'Nearest Neighbour', '2-opt'], direction='down', textHAlign='left',
    font=pygame.font.SysFont('arial', 20)
)

dropdown_metric = Dropdown(
    WIN, 200, 10, 145, 40, name='Metric               ▼',
    choices=[
        'L1-metric',
        'L2-metric',
    ],
    borderRadius=3, colour=pygame.Color('light blue'), values=['L1-metric', 'L2-metric'], direction='down', textHAlign='left',
    font=pygame.font.SysFont('arial', 20)
)

dropdown_routes = Dropdown(
    WIN, 380, 10, 145, 40, name='Route               ▼',
    choices=[
        'eil51',
        'eil76',
        'eil101',
        'kroA100',
        'kroC100',
        'kroD100',
        'Generate Route'
    ],
    borderRadius=3, colour=pygame.Color('light blue'), values=['eil51',
                                                               'eil76',
                                                               'eil101',
                                                               'kroA100',
                                                               'kroC100',
                                                               'kroD100',
                                                               'Generated Route'], 
    direction='down', textHAlign='left', font=pygame.font.SysFont('arial', 20)
)

def start():

    info_for_visualization = choose_algorithm(dropdown_alg.getSelected(), dropdown_metric.getSelected(), dropdown_routes.getSelected())
    
    if info_for_visualization == []:
        return

    print(dropdown_alg.getSelected())
    print(dropdown_metric.getSelected())
    print(dropdown_routes.getSelected())


    final_coords = info_for_visualization[2]
    graph_len = info_for_visualization[3] 
    ALGORITHM_IN_USE = info_for_visualization[0]
    list_of_visited_nodes = info_for_visualization[1][0]


    draw_coords(final_coords, graph_len, ALGORITHM_IN_USE)

    if(dropdown_alg.getSelected() == 'Greedy'):
        draw_greedy(list_of_visited_nodes, final_coords)

    if(dropdown_alg.getSelected() == 'Nearest Neighbour'):
        draw_nearest_neighbour(list_of_visited_nodes, final_coords)

    if(dropdown_alg.getSelected() == '2-opt'):
        for updated_tours in list_of_visited_nodes:
            draw_local_search(ALGORITHM_IN_USE, final_coords, graph_len, updated_tours)
            pygame.time.delay(500)
        list_of_visited_nodes = list_of_visited_nodes[-1]

    best_dst = info_for_visualization[1][1]
    opt_dist = info_for_visualization[4]
    distance_text = DISTANCE_FONT.render(f"Best distance : {best_dst}", 1, SOLVING_COLOR)
    WIN.blit(distance_text, (10,80))

    if(opt_dist != 0):
        opt_text = DISTANCE_FONT.render(f"Optimal distance : {opt_dist}", 1, SOLVING_COLOR)
        WIN.blit(opt_text, (600,80))
    else:
        opt_dist = "Not provided"

    pygame.display.update()

    info_txt = (f"Route: {dropdown_routes.getSelected()}\n"
                 + f"Best distance: {best_dst}\n"
                 + f"Optimal distance: {opt_dist}\n"
                 + f"Algorithm: {dropdown_alg.getSelected()}\n"
                 + f"Metric: {dropdown_metric.getSelected()}\n"
                 + f"Number of points: {graph_len}\n")


    path_list = []
    for index, elem in enumerate(list_of_visited_nodes, start=1):
        if index % 10 == 0:
            path_list.append(str(elem) + "\n ")
        else:
            path_list.append(str(elem))


    with open("Route.txt", "w") as outfile:
            outfile.write(info_txt)
            outfile.write('Coordinates:')
            for key,value in final_coords.items():
                outfile.write('\n'+str(key)+': '+str(value))
            outfile.write(f"\nPath:\n{' -> '.join(path_list)}")


    wait_for_click = True
    while(wait_for_click):
        for event_wait in pygame.event.get():
                if event_wait.type == pygame.MOUSEBUTTONDOWN:
                    wait_for_click = False
                    main()

    #pygame.time.delay(3000)


button_start = Button(
    WIN, 750, 10, 100, 40, text='START', hoverColour=(125, 125, 125), 
    margin=20, inactiveColour=(230,230,230), pressedColour=(125, 125, 125),
    radius=5, font=pygame.font.SysFont('arial', 20),
    textVAlign='centre', onClick=start
)
#--------------------

def draw_coords(final_coords, graph_len, ALGORITHM_IN_USE):

    #WIN.fill(DARK_BLUE)
    WIN.blit(image_map, (0,120))

    solving_text = SOLVING_FONT.render(f"Solving {graph_len} point problem", 1, SOLVING_COLOR)
    WIN.blit(solving_text, (10,10))
    algorithm_text = DISTANCE_FONT.render(f"Algorithm in use : {ALGORITHM_IN_USE}", 1, SOLVING_COLOR)
    WIN.blit(algorithm_text, (10,50))

    max_xd = 0
    max_yd = 0
    for i in range(1, len(final_coords)+1):
        max_xd = max(final_coords[i][0], max_xd)
        max_yd = max(final_coords[i][1], max_yd)

    for i in range(1, len(final_coords)+1):
            xd = final_coords[i][0]
            yd = final_coords[i][1]

            multiplier_x = 9
            multiplier_y = 6

            while((max_xd*multiplier_x>880) or (max_yd*multiplier_y>600)):
                multiplier_x = multiplier_x/1.6
                multiplier_y = multiplier_y/1.5
    
                
           

            # if((i == 1) and (dropdown_alg.getSelected() == 'Nearest Neighbour')):
            if (i==1):
                WIN.blit(STARTING_PIN, ((xd*multiplier_x)-20, (yd*multiplier_y)+80))
            else:
                 WIN.blit(LOCATION_PIN, ((xd*multiplier_x)-20, (yd*multiplier_y)+80))

            if(len(final_coords)) < 30:
                pygame.time.delay(150)
            else:
                pygame.time.delay(20)
            pygame.display.update()
    



def draw_greedy(list_of_visited_nodes2, final_coords):

    max_xd = 0
    max_yd = 0
    for i in range(1, len(final_coords)+1):
        max_xd = max(final_coords[i][0], max_xd)
        max_yd = max(final_coords[i][1], max_yd)


    pygame.time.delay(500)
    
    for j in range (0, len(list_of_visited_nodes2), 2):
        for i in range(1, len(final_coords)+1):  
            multiplier_x = 9
            multiplier_y = 6

            while((max_xd*multiplier_x>880) or (max_yd*multiplier_y>600)):
                multiplier_x = multiplier_x/1.6
                multiplier_y = multiplier_y/1.5  
            if [k for k, v in final_coords.items() if v == (final_coords[i][0], final_coords[i][1])] == [list_of_visited_nodes2[j]]:
                for m in range(1, len(final_coords)+1):  
                    if [k for k, v in final_coords.items() if v == (final_coords[m][0], final_coords[m][1])] == [list_of_visited_nodes2[j+1]]:
                        pygame.time.delay(200)
                        pygame.draw.aaline(WIN, LINE_COLOR, (final_coords[i][0]*multiplier_x, (final_coords[i][1]*multiplier_y)+120), (final_coords[m][0]*multiplier_x, (final_coords[m][1]*multiplier_y)+120))
                               

        pygame.display.update()

def draw_nearest_neighbour(tour_nearest_neighbour, final_coords):

    max_xd = 0
    max_yd = 0
    for i in range(1, len(final_coords)+1):
        max_xd = max(final_coords[i][0], max_xd)
        max_yd = max(final_coords[i][1], max_yd)
            

            

    pygame.time.delay(500)

    for j in range (1, len(tour_nearest_neighbour)):
        for i in range(1, len(final_coords)+1):   
            multiplier_x = 9
            multiplier_y = 6

            while((max_xd*multiplier_x>880) or (max_yd*multiplier_y>600)):
                multiplier_x = multiplier_x/1.6
                multiplier_y = multiplier_y/1.5 
            if [k for k, v in final_coords.items() if v == (final_coords[i][0], final_coords[i][1])] == [tour_nearest_neighbour[j-1]]:
                for m in range(1, len(final_coords)+1):  
                    if [k for k, v in final_coords.items() if v == (final_coords[m][0], final_coords[m][1])] == [tour_nearest_neighbour[j]]:
                        pygame.time.delay(200)
                        pygame.draw.aaline(WIN, LINE_COLOR, (final_coords[i][0]*multiplier_x, (final_coords[i][1]*multiplier_y)+120), (final_coords[m][0]*multiplier_x, (final_coords[m][1]*multiplier_y)+120))
            
               

        pygame.display.update()


def draw_local_search(ALGORITHM_IN_USE, final_coords, graph_len, tour_local_search):

    WIN.fill(DARK_BLUE)
    WIN.blit(image_map, (0,120))

    solving_text = SOLVING_FONT.render(f"Solving {graph_len} point problem", 1, SOLVING_COLOR)
    WIN.blit(solving_text, (10,10))
    algorithm_text = DISTANCE_FONT.render(f"Algorithm in use : {ALGORITHM_IN_USE}", 1, SOLVING_COLOR)
    WIN.blit(algorithm_text, (10,50))

    
    #----------

    max_xd = 0
    max_yd = 0
    for i in range(1, len(final_coords)+1):
        max_xd = max(final_coords[i][0], max_xd)
        max_yd = max(final_coords[i][1], max_yd)
    

    for i in range(1, len(final_coords)+1):
            xd = final_coords[i][0]
            yd = final_coords[i][1]

            multiplier_x = 9
            multiplier_y = 6

            while((max_xd*multiplier_x>880) or (max_yd*multiplier_y>600)):
                multiplier_x = multiplier_x/1.6
                multiplier_y = multiplier_y/1.5
            

            if (i==1):
                WIN.blit(STARTING_PIN, ((xd*multiplier_x)-20, (yd*multiplier_y)+80))
            else:
                 WIN.blit(LOCATION_PIN, ((xd*multiplier_x)-20, (yd*multiplier_y)+80))

                
            #WIN.blit(LOCATION_PIN, ((xd*multiplier_x)-20, (yd*multiplier_y)+80))
    

    for j in range (1, len(tour_local_search)):
        for i in range(1, len(final_coords)+1):    
            if [k for k, v in final_coords.items() if v == (final_coords[i][0], final_coords[i][1])] == [tour_local_search[j-1]]:
                for m in range(1, len(final_coords)+1):  
                    if [k for k, v in final_coords.items() if v == (final_coords[m][0], final_coords[m][1])] == [tour_local_search[j]]:
                        pygame.draw.aaline(WIN, LINE_COLOR, (final_coords[i][0]*multiplier_x, (final_coords[i][1]*multiplier_y)+120), (final_coords[m][0]*multiplier_x, (final_coords[m][1]*multiplier_y)+120))
                             
               
    pygame.display.update()

    

def main():

    run = True
    while run:
        WIN.fill(DARK_BLUE)
        WIN.blit(image_map, (0,120))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        pygame_widgets.update(pygame.event.get())
        pygame.display.update()
    

if __name__ == "__main__":  
    main()

    