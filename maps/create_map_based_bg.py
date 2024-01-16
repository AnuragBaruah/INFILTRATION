import pygame, pickle, os

def main():
    mapname = input('Enter Name of the Map File : ').rstrip('.map')
    try:
        with open(mapname + '.map', 'rb') as f:
            data = pickle.load(f)
            walls_dict = data['walls']
    except FileNotFoundError:
        print(f'{mapname} : file not found')
        return 1
    os.system(f'md {mapname}-bgpics')
    bg_floor = input('Enter name of picture you would like to use as a floor background (type "none" for plain black floor) : ')
    if bg_floor == 'none': bg_floor = 'none.png'
    bg = pygame.image.load(bg_floor)    
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    for grid_val in walls_dict:
        screen.fill((0,0,0))
        screen.blit(bg, (0,0))
        gx, gy = grid_val
        for wall in walls_dict[grid_val]:
            x1, y1 = wall['top_left']
            x2, y2 = wall['bottom_right']
            w, h = x2 - x1, y2 - y1
            x, y = x1 - gx*1280, y1 - gy*720
            rect = (x, y, w, h)
            pygame.draw.rect(screen, (255, 0, 0), rect)
        pygame.display.update()
        pic_name = f'{mapname}-bgpics/{mapname}-{gx}-{gy}.png'
        pygame.image.save(screen, pic_name)
    return 0 

##top level
while __name__ == '__main__':
    r = main()
    if r == 0:
        break