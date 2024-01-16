import pygame
pygame.font.init()
content = pygame.font.Font('./normal.ttf', 20)
pygame.mixer.init()

checkpoint_sound = pygame.mixer.Sound('./sounds/SFX/checkpoint.mp3')

sound_loader = pygame.mixer.Sound

white = (255, 255, 255)

# def func0(gameObj, levelObj = None) -> tuple['function', tuple, int]:

def create_messages(messages : tuple[str]):
    msgs = [(None, (0,0))]
    h = 0
    for i in messages:
        m = content.render(i, 1, white)
        h += m.get_height()
        msgs.append((m, (0,h)))
    return msgs

def render_messages(screen : pygame.Surface, messages : list[tuple[pygame.Surface | None , tuple[int,int]]]):
    for i in range(1, len(messages)):
        screen.blit(messages[i][0], messages[i-1][1])

def create_sound(filename : str):
    return pygame.mixer.Sound(filename)
def play_sound(channel : pygame.mixer.Channel, sound = checkpoint_sound):
    channel.play(sound)
