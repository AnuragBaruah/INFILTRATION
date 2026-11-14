import pickle
import pygame, game, time
import scoring

pygame.font.init()
content_font = pygame.font.Font('normal.ttf', 35)
heading_font = pygame.font.Font('normal.ttf', 65)

##menu button command functions
def pass_cmd():
    pass

def new_game_button(menu):
    menu.gameObj.playing_level_index = 0
    menu.gameObj.isplaying = True

def resume_game_button(menu):
    menu.gameObj.isplaying = True

def next_level_button(menu):
    menu.gameObj.playing_level_index += 1
    menu.gameObj.isplaying = True

def start_level_button(menu, n):
    menu.gameObj.playing_level_index = n
    menu.gameObj.isplaying = True

def goto_levelselector(menu):
    menu.gameObj.return_menu_mode = menu.gameObj.menumode
    menu.gameObj.menumode = 'levelselector'

def back_from_levelselector(menu):
    menu.gameObj.menumode = getattr(menu.gameObj, 'return_menu_mode', 'startup')

def previous_level_page(menu):
    menu.page = max(0, menu.page - 1)
    menu._page_needs_rebuild = True

def next_level_page(menu):
    menu.page = min(menu.page_count - 1, menu.page + 1)
    menu._page_needs_rebuild = True

def quit_button(menu):
    menu.gameObj.isrunning = False


def draw_level_score(screen, result):
    if not result:
        return
    font = pygame.font.Font('normal.ttf', 28)
    best = result.get('best', {})
    rows = []
    if result.get('is_new_record'):
        rows.append('NEW HIGH SCORE!')
    rows.extend((
        f"TIME {scoring.format_time(result['time_seconds'])}     GHOSTS {result['ghosts_killed']}     PATROLS {result['patrols_killed']}",
        f"HEALTH LOST {result['health_lost']} / {result['starting_health']}     LEFT {result['health_remaining']}",
        f"SCORE {result['score']:,}    TIME +{result['time_bonus']:,}    COMBAT +{result['combat_bonus']:,}    HEALTH +{result['health_bonus']:,}",
    ))
    if best:
        rows.append(
            f"BEST {int(best.get('score', 0)):,}  |  {scoring.format_time(best.get('time_seconds', 0))}  |  "
            f"{int(best.get('ghosts_killed', 0))} ghosts  |  {int(best.get('health_remaining', 0))} HP left"
        )
    y = 155
    for row in rows:
        surface = font.render(row, 1, (67, 54, 51))
        screen.blit(surface, (640 - surface.get_width() // 2, y))
        y += 42

##ui sounds
pygame.mixer.init()
hover_sfx = pygame.mixer.Sound('sounds/SFX/hover.mp3')
hover_sfx.set_volume(0.09)
click_sfx1 = pygame.mixer.Sound('sounds/SFX/click.mp3')
locked_click_sfx = pygame.mixer.Sound('sounds/SFX/click.mp3')
locked_click_sfx.set_volume(0.02)
click_sfx = click_sfx1


class Menu_Button(object):
    def __init__(self, text, color1, color2, x, y, command = None, params = (), font_type = content_font, backcolor = None):
        if command == None:
            command = pass_cmd
            
        self.img1 = font_type.render(text, 1, color1)
        self.img2 = font_type.render(text, 1, color2, backcolor)
        self.img = self.img1
        a, b = self.img1.get_size()
        self.top_left_corner = (x, y)
        self.bottom_right_corner = (x + a, y + b)
        self.command = command
        self.params = params
        self.state = False

    def update_button_state(self):
        x, y = pygame.mouse.get_pos()
        old_state = self.state
        if self.top_left_corner[0] <= x <= self.bottom_right_corner[0] and self.top_left_corner[1] <= y <= self.bottom_right_corner[1]:
            self.state = True
            self.img = self.img2
        else:
            self.state = False
            self.img = self.img1
        if (not old_state) and (self.state):
            return 1
        if old_state and not self.state:
            return -1
        else:
            return 0

    def set_focused(self, focused):
        self.state = bool(focused)
        self.img = self.img2 if self.state else self.img1
        

class Locked_Button(Menu_Button):
    def __init__(self, text, color1, color2, x, y, font_type = content_font, backcolor = None):
        Menu_Button.__init__(self, text, color1, color2, x, y, pass_cmd, (), font_type, backcolor)
    
    def update_button_state(self):
        global click_sfx
        x, y = pygame.mouse.get_pos()
        old_state = self.state
        if self.top_left_corner[0] <= x <= self.bottom_right_corner[0] and self.top_left_corner[1] <= y <= self.bottom_right_corner[1]:
            self.state = True
            self.img = self.img2
        else:
            self.state = False
            self.img = self.img1
        if (not old_state) and (self.state):
            click_sfx = locked_click_sfx
            hover_sfx.set_volume(0.02)
            return 1
        if old_state and not self.state:
            click_sfx = click_sfx1
            hover_sfx.set_volume(0.09)
            return -1
        else:
            return 0
    



class Main_Menu(object):
    def __init__(self, gameObj : game.Game):
        self.gameObj = gameObj
        self.bg = pygame.image.load('images/main_menu_bg.png')
        self.bg = pygame.transform.scale(self.bg, gameObj.screen_size)
        self.buttons = [
                                    Menu_Button('NEW GAME', self.gameObj.color['dark'], self.gameObj.color['lightest'], 100, 100, new_game_button, (self,)),
                                    Menu_Button('EXIT GAME', self.gameObj.color['dark'], self.gameObj.color['lightest'], 100, 600, quit_button, (self,)),
                                    Menu_Button('LEVEL SELECTOR', self.gameObj.color['dark'], self.gameObj.color['lightest'], 100, 300, goto_levelselector, (self,))
                                  ]
        self.keep_track = False
        self.selected_index = next((i for i, b in enumerate(self.buttons) if not isinstance(b, Locked_Button)), 0)
        self._controller_focus = False
        self.navigation_grid = [[0], [2], [1]]

    def _move_selection(self, dx, dy):
        if not self.buttons or not getattr(self, 'navigation_grid', None):
            return
        for row, items in enumerate(self.navigation_grid):
            if self.selected_index not in items:
                continue
            col = items.index(self.selected_index)
            if dy:
                target_row = row + dy
                while 0 <= target_row < len(self.navigation_grid):
                    target_items = self.navigation_grid[target_row]
                    choices = [(abs(target_col-col), target_col, target)
                               for target_col, target in enumerate(target_items)
                               if target is not None and target < len(self.buttons)]
                    if choices:
                        _, _, self.selected_index = min(choices)
                        return
                    target_row += dy
            else:
                target_col = col + dx
                if 0 <= target_col < len(items):
                    target = items[target_col]
                    if target is not None and target < len(self.buttons):
                        self.selected_index = target
            return


    def update_menu(self):
        self.gameObj.screen.blit(self.bg, (0,0))
        inputs = self.gameObj.INPUTS
        controller = self.gameObj.controller_active
        focused_input = controller or any(inputs[key] for key in (
            'menu_up', 'menu_down', 'menu_left', 'menu_right', 'menu_confirm', 'menu_back'
        ))
        if focused_input:
            if inputs['menu_up']: self._move_selection(0, -1)
            elif inputs['menu_down']: self._move_selection(0, 1)
            elif inputs['menu_left']: self._move_selection(-1, 0)
            elif inputs['menu_right']: self._move_selection(1, 0)
            for i, button in enumerate(self.buttons):
                button.set_focused(i == self.selected_index)
            self._controller_focus = True
            if inputs['menu_confirm']:
                button = self.buttons[self.selected_index]
                self.gameObj.UI_channel.set_volume(0.02 if isinstance(button, Locked_Button) else 1)
                self.gameObj.UI_channel.play(locked_click_sfx if isinstance(button, Locked_Button) else click_sfx)
                if not isinstance(button, Locked_Button):
                    button.command(*button.params)
            if inputs['menu_back']:
                if getattr(self, 'islevelselector', False):
                    back_from_levelselector(self)
                elif self.gameObj.menumode == 'pause':
                    resume_game_button(self)
        else:
            if self._controller_focus:
                self._controller_focus = False
            self.gameObj.INPUTS['menu_back'] = False
        mt = 0
        for button in self.buttons:
            req_sfx = 0 if focused_input else button.update_button_state()
            if req_sfx == 1:
                self.gameObj.UI_channel.set_volume(1)
                self.gameObj.UI_channel.play(hover_sfx)
            elif req_sfx == -1:
                self.gameObj.UI_channel.set_volume(0.1)
                self.gameObj.UI_channel.play(hover_sfx)
            mt += button.state
            self.gameObj.screen.blit(button.img, button.top_left_corner)
            if button.state and not controller and not focused_input:
                pygame.mouse.set_cursor(11)
                if pygame.mouse.get_pressed()[0] and not self.keep_track:
                    self.gameObj.UI_channel.set_volume(1)
                    self.gameObj.UI_channel.play(click_sfx)
                    time.sleep(0.5)
                    button.command(*button.params)
        if mt == 0 and not controller:
            self.keep_track = pygame.mouse.get_pressed()[0]
            pygame.mouse.set_visible(1)
            pygame.mouse.set_cursor(0)


class Pause_Menu(Main_Menu):
    def __init__(self, gameObj : game.Game):
        Main_Menu.__init__(self, gameObj)
        self.bg = pygame.transform.smoothscale(pygame.image.load('images/level_clear.png'), self.gameObj.screen_size)
        img = heading_font.render(f'GAME PAUSED', 1, self.gameObj.color['dark'])
        self.bg.blit(img, (640 - img.get_width()//2, 60))
        self.buttons = [
            Menu_Button('RESUME GAME', self.gameObj.color['dark'], self.gameObj.color['lightest'], 100, 200, resume_game_button, (self,)),
            Menu_Button('LEVEL SELECTOR', self.gameObj.color['dark'], self.gameObj.color['lightest'], 100, 400, goto_levelselector, (self,)),
            Menu_Button('QUIT GAME', self.gameObj.color['dark'], self.gameObj.color['lightest'], 100, 600, quit_button, (self,))
        ]
        self.navigation_grid = [[0], [1], [2]]
        y = 300
        for btn in self.buttons:
            a, b = btn.img1.get_size()
            btn.top_left_corner = (640 - a//2, y)
            btn.bottom_right_corner = (640 - a//2 + a, y + b)
            y += 150


class Win_Menu(Main_Menu):
    def __init__(self, gameObj: game.Game, level_name : str):
        Main_Menu.__init__(self, gameObj)
        self.bg = pygame.transform.smoothscale(pygame.image.load('images/level_clear.png'), self.gameObj.screen_size)
        img = heading_font.render(f'{level_name} CLEARED', 1, self.gameObj.color['dark'])
        self.bg.blit(img, (40, 60))
        draw_level_score(self.bg, getattr(gameObj, 'level_result', None))
        self.buttons = [
            Menu_Button('NEXT LEVEL', self.gameObj.color['dark'], self.gameObj.color['lightest'], 120, 490, next_level_button, (self,)),
            Menu_Button('EXIT GAME', self.gameObj.color['dark'], self.gameObj.color['lightest'], 680, 490, quit_button, (self,)),
            Menu_Button('PLAY AGAIN', self.gameObj.color['dark'], self.gameObj.color['lightest'], 120, 595, resume_game_button, (self,)),
            Menu_Button('LEVEL SELECTOR', self.gameObj.color['dark'], self.gameObj.color['lightest'], 680, 595, goto_levelselector, (self,))
        ]
        self.navigation_grid = [[0, 1], [2, 3]]

class Game_Complete_Menu(Main_Menu):
    def __init__(self, gameObj: game.Game):
        Main_Menu.__init__(self, gameObj)

        self.buttons = [
            Menu_Button('NEW GAME', self.gameObj.color['dark'], self.gameObj.color['lightest'], 120, 520, new_game_button, (self,)),
            Menu_Button('EXIT GAME', self.gameObj.color['dark'], self.gameObj.color['lightest'], 680, 520, quit_button, (self,)),
            Menu_Button('LEVEL SELECTOR', self.gameObj.color['dark'], self.gameObj.color['lightest'], 120, 615, goto_levelselector, (self,))
        ]
        self.navigation_grid = [[0, 1], [2, None]]

        self.bg = pygame.transform.smoothscale(pygame.image.load('images/level_clear.png'), self.gameObj.screen_size)
        img = heading_font.render(f'FULL GAME COMPLETE', 1, self.gameObj.color['dark'])
        self.bg.blit(img, (40, 60))
        draw_level_score(self.bg, getattr(gameObj, 'level_result', None))


class Game_Over_Menu(Main_Menu):
    def __init__(self, gameObj : game.Game):
        Main_Menu.__init__(self, gameObj)
        self.bg = pygame.transform.smoothscale(pygame.image.load('images/level_clear.png'), self.gameObj.screen_size)
        img = heading_font.render(f'YOU JUST COULD NOT MAKE IT', 1, self.gameObj.color['dark'])
        self.bg.blit(img, (40, 60))
        self.buttons = [
            Menu_Button('TRY AGAIN', self.gameObj.color['dark'], self.gameObj.color['lightest'], 220, 420, resume_game_button, (self,)),
            Menu_Button('LEVEL SELECTOR', self.gameObj.color['dark'], self.gameObj.color['lightest'], 680, 420, goto_levelselector, (self,)),
            Menu_Button('EXIT GAME', self.gameObj.color['dark'], self.gameObj.color['lightest'], 220, 535, quit_button, (self,))
        ]
        self.navigation_grid = [[0, 1], [2, None]]


class Level_Selector_Menu(Main_Menu):
    PAGE_SIZE = 9

    def __init__(self, gameObj : game.Game, page=0):
        Main_Menu.__init__(self, gameObj)
        self.page = page
        self._page_needs_rebuild = False
        self._build_buttons()
        self.islevelselector = True

    @property
    def page_count(self):
        return max(1, (len(self.gameObj.level_names) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)

    def _build_buttons(self):
        self.bg = pygame.transform.smoothscale(pygame.image.load('images/level_clear.png'), self.gameObj.screen_size)
        heading = heading_font.render('LEVEL SELECTOR', 1, self.gameObj.color['dark'])
        self.bg.blit(heading, (40, 60))
        self.buttons = []
        with open('Max-Level-Unlocked', 'rb') as f:
            max_lev = pickle.load(f)
        first = self.page * self.PAGE_SIZE
        last = min(len(self.gameObj.level_names), first + self.PAGE_SIZE)
        page_items = last - first
        for local_index, level_index in enumerate(range(first, last)):
            col, row = local_index % 3, local_index // 3
            x, y = (55, 455, 855)[col], 170 + row * 120
            name = self.gameObj.level_names[level_index]
            if level_index <= max_lev:
                button = Menu_Button(name, self.gameObj.color['dark'], self.gameObj.color['lightest'], x, y,
                                     start_level_button, (self, level_index))
            else:
                button = Locked_Button(name, self.gameObj.color['light'], self.gameObj.color['light-2'], x, y)
            self.buttons.append(button)
        nav_y = 585
        self.buttons.append(Locked_Button('PREV PAGE', self.gameObj.color['light'], self.gameObj.color['light-2'], 55, nav_y)
                            if self.page == 0 else Menu_Button('PREV PAGE', self.gameObj.color['dark'], self.gameObj.color['lightest'], 55, nav_y, previous_level_page, (self,)))
        self.buttons.append(Locked_Button('NEXT PAGE', self.gameObj.color['light'], self.gameObj.color['light-2'], 455, nav_y)
                            if self.page + 1 >= self.page_count else Menu_Button('NEXT PAGE', self.gameObj.color['dark'], self.gameObj.color['lightest'], 455, nav_y, next_level_page, (self,)))
        self.buttons.append(Menu_Button('BACK', self.gameObj.color['dark'], self.gameObj.color['lightest'], 955, nav_y, back_from_levelselector, (self,)))
        page_text = content_font.render(f'PAGE {self.page + 1} / {self.page_count}', 1, self.gameObj.color['dark'])
        self.bg.blit(page_text, (640 - page_text.get_width() // 2, 650))
        self.selected_index = 0
        level_rows = [[i if i < page_items else None for i in range(row * 3, row * 3 + 3)] for row in range(3)]
        footer = [page_items, page_items + 1, page_items + 2]
        self.navigation_grid = level_rows + [footer]

    def update_menu(self):
        if self._page_needs_rebuild:
            self._page_needs_rebuild = False
            self._build_buttons()
        Main_Menu.update_menu(self)



        
