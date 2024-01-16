import os
import pygame, pickle
from math import fabs
pygame.init()
pygame.font.init()
sf = pygame.font.SysFont('Arial', 15, bold  = True)
bf = pygame.font.SysFont('Arial', 20)

basicenemy = pygame.image.load('basicenemy.png')
weakenemy = pygame.image.load('weakenemy.png')
bomb = pygame.transform.scale(pygame.image.load('../images/bomb1.png'), (20, 20))


'''these 3 variables can be changed according to user's wish'''

speed = 20 #camera speed for W-A-S-D movement (pixels per frame)
min_pixel_accuracy = 80 #for the snapy motion
t = 15


'''
controls:

1. The main working handle is a big "plus" whose exact position is being displayed at all times.
2. To start a wall (horizontal or vertical) at the position of the working handle press "tab" once.
3. To draw a free rectangle, keep pressing "left-ctrl".
4. To end a wall/rectangle press "spacebar" once.
5. To be able to get snap-y motion of the working handle keep "left-shift" pressed.
6. To add a path-node at the location of the working handle press "left-alt"
7. To delete a wall or a node, hover over the same and press "1"
8. To add a mission sequence pointer, press "M"
9. To add basic enemy - press e, weak enemy - press b
10. Press enter to add player to the scene
11. To add bomb to scene - press 0 
'''



cam_x = 0
cam_y = 0
bottom_right = None
top_left = None
vertical_motion = 0 
horizontal_motion = 0
snap = False
marker_pos = [0,0]
freerect = False
walls = []
path_nodes = []
mission_pointers = []
bomb_positions = []
enemy_data = [] # each element will be as follows - [x, y, type] , type = 'b' or 'w'
player_data = () # it will be either an empty tuple or a tuple (x, y)
filename = ''
deletecheck = False


def reset_variables():
    global cam_x, cam_y, bottom_right, bomb_positions, player_data, top_left, enemy_data, marker_pos, walls, path_nodes, filename, deletecheck, mission_pointers
    cam_x = 0
    cam_y = 0
    bottom_right = None
    top_left = None
    marker_pos = [0,0]
    walls = []
    bomb_positions = []
    player_data = ()
    path_nodes = []
    mission_pointers = []
    enemy_data = []
    filename = ''
    deletecheck = False


def get_file_data(filename):
    global walls, path_nodes, mission_pointers, enemy_data, player_data, bomb_positions
    walls = []
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        sorted_walls = data['walls']
        path_nodes = data['path_nodes']
        mission_pointers = data['mission_pointers']
        enemy_data = data['enemy_data']
        player_data = data['player_data']
        bomb_positions = data['bomb_positions']
    for i in sorted_walls:
        for j in sorted_walls[i]:
            walls.append(j)


def createfile(filename):
    gx, gy = 0, 0
    for wall in walls:
        if wall['bottom_right'][0] // 1280 > gx:
            gx = wall['bottom_right'][0] // 1280
        if wall['bottom_right'][1] // 720 > gy:
            gy = wall['bottom_right'][1] // 720
    
    grid_sorted_walls = {}
    print('grid-sorting the walls :')
    count = 0
    for x in range(gx + 1):
        for y in range(gy + 1):
            count += 1
            grid_sorted_walls[(x, y)] = list()
            grid_rect = pygame.Rect(x*1280 - 10*t, y*720 - 10*t, 1280 + 10*t, 720 + 10*t)
            for wall in walls:
                wall_rect = pygame.Rect(wall['top_left'][0], wall['top_left'][1], wall['bottom_right'][0] - wall['top_left'][0], wall['bottom_right'][1] - wall['top_left'][1])
                if pygame.Rect.colliderect(grid_rect, wall_rect):
                    grid_sorted_walls[(x, y)].append(wall)
            print(f'\r{str(count / ((gx + 1) * (gy + 1)) * 100)[:5]} % completed', end = '')
    
    path_lines = list()
    if path_nodes:
        print('\nAnalysing Nodes to create path_lines :')
    count = 0
    for node1 in path_nodes:
        count += 1
        node1_paths = []
        c = list(path_nodes)
        c.remove(node1)
        for node2 in c:
            for wall in walls:
                wall_rect = pygame.Rect(wall['top_left'][0], wall['top_left'][1], wall['bottom_right'][0] - wall['top_left'][0], wall['bottom_right'][1] - wall['top_left'][1])
                if wall_rect.clipline(node1, node2):
                    break
            else:
                node1_paths.append(path_nodes.index(node2))
        print(f'\r{str(count / len(path_nodes) * 100)[:5]} % completed', end = '')
        path_lines.append(tuple(node1_paths))


    data = {
        'walls' : grid_sorted_walls, 'path_nodes' : path_nodes, 'path_lines' : path_lines, 
        'mission_pointers' : mission_pointers, 'enemy_data' : enemy_data, 'player_data' : player_data,
        'bomb_positions' : bomb_positions
    }
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    print()


def update_walls():
    global walls, top_left, bottom_right

    walls.append({'top_left' : top_left, 'bottom_right' : tuple(bottom_right)})


def update_and_render_world():
    global speed, cam_x, cam_y, bottom_right, t, freerect, walls, marker_pos, path_nodes, player_data, enemy_data

    cam_x += horizontal_motion * speed
    cam_y -= vertical_motion * speed
    bottom_right = list(marker_pos)
    if top_left and not freerect:
        if fabs(marker_pos[0] - top_left[0]) > fabs(marker_pos[1] - top_left[1]):
            bottom_right = [marker_pos[0], top_left[1] + t]
        else:
            bottom_right = [top_left[0] + t, marker_pos[1]]
    
    if deletecheck:
        dummy_walls = list(walls)
        for w in dummy_walls:
            if w['top_left'][0] < marker_pos[0] < w['bottom_right'][0] and w['top_left'][1] < marker_pos[1] < w['bottom_right'][1]:
                walls.remove(w)
        dummy_nodes = list(path_nodes)
        for n in dummy_nodes:
            if n[0] - 5 < marker_pos[0] < n[0] + 5 and n[1] - 5 < marker_pos[1] < n[1] + 5:
                path_nodes.remove(n)
        dummy_nodes = list(mission_pointers)
        for n in dummy_nodes:
            if n[0] - 5 < marker_pos[0] < n[0] + 5 and n[1] - 5 < marker_pos[1] < n[1] + 5:
                mission_pointers.remove(n)
        
        dummy_enemies = list(enemy_data)
        for e in dummy_enemies:
            if pygame.Rect.collidepoint(pygame.Rect([e[0], e[1], 30, 30]), marker_pos):
                enemy_data.remove(e)
        dummy_bombs = list(bomb_positions)
        for i in dummy_bombs:
            if pygame.Rect.collidepoint(pygame.Rect(i[0], i[1], 20, 20), marker_pos):
                bomb_positions.remove(i)
        
        if player_data and pygame.Rect.collidepoint(pygame.Rect([player_data[0], player_data[1], 50, 50]), marker_pos):
            player_data = ()

    for wall in walls:
        a1 = wall['top_left']
        a2 = wall['bottom_right']
        rect = a1[0] - cam_x, a1[1] - cam_y, a2[0] - a1[0], a2[1] - a1[1]
        pygame.draw.rect(screen, (0, 115, 168), rect)
    if top_left:
        a1 = top_left
        a2 = bottom_right
        rect = a1[0] - cam_x, a1[1] - cam_y, a2[0] - a1[0], a2[1] - a1[1]
        screen.blit(sf.render(f'{tuple(a1)} : {tuple(a2)}', 1, (255, 0, 0)), (rect[0], rect[1] - 30))
        pygame.draw.rect(screen, (120, 115, 168), rect)

    if player_data:
        pygame.draw.rect(screen, (255, 9, 255), (player_data[0] - cam_x, player_data[1] - cam_y, 50, 50))
    
    for en in enemy_data:
        if en[2] == 'basic':
            screen.blit(basicenemy, ((en[0] - cam_x, en[1] - cam_y, 30, 30)))
        else:
            screen.blit(weakenemy, ((en[0] - cam_x, en[1] - cam_y, 30, 30)))

    for node_index in range(len(path_nodes)):
        x, y = path_nodes[node_index]
        pygame.draw.rect(screen, (0, 255, 0), (x - 5 - cam_x,  y - 5 - cam_y,  10, 10))
        screen.blit(sf.render(f'{node_index}', 1, (255, 255, 255)), (x - 5 - cam_x,  y - 20 - cam_y))
    
    for p in range(len(mission_pointers)):
        x, y = mission_pointers[p]
        pygame.draw.rect(screen, (0, 0, 255), (x - 5 - cam_x,  y - 5 - cam_y,  10, 10))
        screen.blit(sf.render(f'{p}', 1, (255, 255, 255)), (x - 5 - cam_x,  y - 20 - cam_y))
    for p in bomb_positions:
        x, y = p
        screen.blit(bomb, (x - cam_x, y - cam_y))

    
    x, y = marker_pos[0] - cam_x, marker_pos[1] - cam_y
    screen.blit(bf.render(f'{tuple(marker_pos)}', 1, (255, 255, 255)), (x, y - 50))
    pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, 720), 1)
    pygame.draw.line(screen, (200, 200, 200), (0, y), (1280, y), 1)


def user_input():
    global horizontal_motion, vertical_motion, player_data, enemy_data, snap, cam_y, cam_x, top_left, freerect, running, marker_pos, path_nodes, deletecheck
    deletecheck = False

    m = pygame.mouse.get_pos()
    marker_pos = [m[0] + cam_x, m[1] + cam_y]
    if snap:
        marker_pos[0], marker_pos[1] =  min_pixel_accuracy*(marker_pos[0] // min_pixel_accuracy), min_pixel_accuracy*(marker_pos[1] // min_pixel_accuracy)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                if top_left:
                    update_walls()
                    top_left = None
                else:
                    pass
            elif event.key == pygame.K_TAB:
                if not top_left:
                    top_left = tuple(marker_pos)
                else:
                    top_left = None
            elif event.key == pygame.K_LALT:
                path_nodes.append(tuple(marker_pos))
            elif event.key == pygame.K_1:
                deletecheck = True
            elif event.key == pygame.K_RETURN and not player_data:
                player_data = tuple(marker_pos)
            elif event.key == pygame.K_m:
                mission_pointers.append(tuple(marker_pos))
            elif event.key == pygame.K_b:
                enemy_data.append((marker_pos[0], marker_pos[1], 'basic'))
            elif event.key == pygame.K_e:
                enemy_data.append((marker_pos[0], marker_pos[1], 'weak'))
            elif event.key == pygame.K_0:
                bomb_positions.append(tuple(marker_pos))
    
        
    keys = pygame.key.get_pressed()
    horizontal_motion = int(keys[pygame.K_d] - keys[pygame.K_a])
    vertical_motion = int(keys[pygame.K_w] - keys[pygame.K_s])
    snap = keys[pygame.K_LSHIFT]
    freerect = keys[pygame.K_LCTRL]


def pygame_loop():
    pygame.mouse.set_visible(0)
    user_input()
    screen.fill((0,0,0))
    screen.blit(bg_reference_img, (5 - cam_x, 5 - cam_y))
    update_and_render_world()
    pygame.display.update()


def main():
    global screen, running, walls, filename, bg_reference_img
    menu_opt = input('press enter for new map, type filename without extension for saved map (type "exit" to end program): ') + '.map'
    if menu_opt == '.map':
        filename = input('enter a new filename (without extension, writing old filename will replace original file) : ') + '.map'
        nr = int(input('enter number of rows of grid : '))
        nc = int(input('enter number of columns of grid : '))
        img_file = input('enter name for a supporting image map for tracing (type name "none" if you don\'t want image) : ')
        bg_reference_img = pygame.transform.smoothscale(pygame.image.load(img_file), (nc*1280, nr*720))
        with open(filename + 'support', 'wb') as f:
            pickle.dump(img_file, f)
            pickle.dump(nc, f)
            pickle.dump(nr, f)
        for p in range(nc):
            walls.append({'top_left' : (1280*p, 0), 'bottom_right' : (1280*(p+1), t)})
            walls.append({'top_left' : (1280*p, nr*720 - t), 'bottom_right' : (1280*(p+1), nr*720)})
        for p in range(nr):
            walls.append({'top_left' : (0, 720*p), 'bottom_right' : (t, 720 + 720*p)})
            walls.append({'top_left' : (nc*1280 - t, 720*p), 'bottom_right' : (nc*1280, 720 + 720*p)})
    
    elif menu_opt == 'exit.map':
        return 1
    
    else:
        try:
            filename = menu_opt
            get_file_data(filename)
            with open(filename + 'support', 'rb') as f:
                img_file = pickle.load(f)
                nc = pickle.load(f)
                nr = pickle.load(f)
            bg_reference_img = pygame.transform.smoothscale(pygame.image.load(img_file), (nc*1280, nr*720))
        except:
            print(f'"{filename}" or "{filename}support" not found')
            return 0
    
    
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    c = pygame.time.Clock()

    running = True
    while running:
        c.tick(30)
        pygame_loop()
    pygame.quit()
    createfile(filename)
    return 1


def generate_code(n, level_name):
    python_code = f"""import pygame
from Levels import commonfunctions as CFS

## script for mission {level_name}

"""
    for i in range(n):
        python_code += f"""

## code for event {i} ::  
msg{i} = CFS.create_messages(
            (
                'Event {i} just got triggered',
                'This is automatic generation of message'
            )
        )
def func{i}(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg{i}), gameObj.fps * 10

"""
    return python_code


def make_level():
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        walls_dict = data['walls']
    level_name = filename[0:-4]
    folder = f"..\\Levels\\{level_name}\\{level_name}-bgpics"
    os.system(f'if not exist "{folder}" (md "{folder}")')
    bg = pygame.image.load(input('enter the name of picture for floor texture (type none.png for plain black) :: '))    
    wall_color = eval(input('enter RGB tuple for wall color'))
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    for grid_val in walls_dict:
        screen.fill((0,0,0))
        screen.blit(bg, (0,0))
        for wall in walls_dict[grid_val]:
            pygame.draw.rect(screen, wall_color, (
                (wall['top_left'][0] - grid_val[0] * 1280), 
                (wall['top_left'][1] - grid_val[1] * 720), 
                (wall['bottom_right'][0] - wall['top_left'][0]), 
                (wall['bottom_right'][1] - wall['top_left'][1]))
                )
        pygame.display.update()
        pygame.image.save(screen, f'{folder}/{level_name}-{grid_val[0]}-{grid_val[1]}.png')
    folder = folder.rstrip('-bgpics')
    with open(f'{folder}.map', 'wb') as f:
        pickle.dump(data, f)
    
    with open(f'../Levels/{level_name}.py', 'w') as f:
        f.write(generate_code(len(data['mission_pointers']), level_name))
    
    # with open(f'../Levels/Level-Names.txt', 'a') as f:
    #     f.write('\n' + level_name)
    
    level_names = []
    with open('../Levels/Level-Names.txt', 'r') as f:
        raw_data = f.read().split('\n')
    for i in raw_data:
        if i[0] != '#':
            level_names.append(i)
    with open(f'../Levels/Level-Names.txt', 'a') as f:
        if level_name not in level_names:
            f.write('\n' + level_name)
    level_names.append(level_name)
    with open('../Levels/__init__.py', 'w') as ff:
        level_names = []
        with open('../Levels/Level-Names.txt', 'r') as f:
            raw_data = f.read().split('\n')
        for i in raw_data:
            if i[0] != '#':
                level_names.append(i)
        ff.write(f'__all__ = {level_names}')
            
    pygame.quit()
    
    

while True:
    reset_variables()
    e = main()
    if e == 1:
        break
input('press enter to continue')
make_level()
input('done')



