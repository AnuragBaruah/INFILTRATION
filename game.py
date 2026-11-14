import pickle
import pygame


# Edit this table to remap actions. Joystick buttons and axes use Pygame's
# standard Xbox-compatible layout; trigger axes may report either 0..1 or -1..1.
DEFAULT_BINDINGS = {
    'dead_zone': 0.22,
    'trigger_threshold': 0.55,
    'buttons': {
        'knife': 5,          # RB
        'plant_bomb': 0,     # A (bomb pickup remains automatic)
        'trigger_action': 3, # Y; currently reserved by gameplay
        'menu_confirm': 0,   # A
        'menu_back': 1,      # B
        'pause': 7,          # Start
    },
    'axes': {
        'move_x': 0, 'move_y': 1,
        'detonate': 5,       # RT on common XInput mappings
    },
    'hat': 0,
    'keys': {
        'move_forward': pygame.K_w, 'move_backward': pygame.K_s,
        'detonate': pygame.K_SPACE, 'pause': pygame.K_ESCAPE,
        'trigger_action': pygame.K_e, 'make_new_node': pygame.K_TAB,
        'menu_up': pygame.K_UP, 'menu_down': pygame.K_DOWN,
        'menu_left': pygame.K_LEFT, 'menu_right': pygame.K_RIGHT,
        'menu_confirm': pygame.K_RETURN, 'menu_back': pygame.K_ESCAPE,
    },
    'mouse': {'plant_bomb': 1, 'knife': 3},
}


class Game(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.joystick.init()
        # Device-added SDL events can fail conversion in some Pygame/Windows
        # builds. We read joystick state directly and detect count changes instead.
        joystick_events = (
            'JOYAXISMOTION', 'JOYBALLMOTION', 'JOYHATMOTION', 'JOYBUTTONDOWN',
            'JOYBUTTONUP', 'JOYDEVICEADDED', 'JOYDEVICEREMOVED',
        )
        pygame.event.set_blocked([getattr(pygame, name) for name in joystick_events if hasattr(pygame, name)])
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen_size = self.screen.get_size()
        pygame.display.set_icon(pygame.image.load('images/icon.ico'))
        pygame.display.set_caption('THE INFILTRATION')
        self.isrunning = True
        self.isplaying = False
        self.menumode = 'startup'
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.color = {
            'red': (255, 0, 0), 'blue': (0, 0, 255), 'green': (0, 255, 0), 'hlt_green': (46, 163, 54),
            'grey': (80, 80, 80), 'white': (255, 255, 255), 'offwhite': (200, 200, 200),
            'seaBlue': (100, 200, 200), 'lightgrey': (120, 120, 120), 'black': (0, 0, 0),
            'lightest': (247, 240, 245), 'light': (222, 203, 183), 'light-2': (200, 181, 161),
            'mid': (143, 133, 125), 'dark': (92, 85, 82), 'darkest': (67, 54, 51)
        }
        self.screen.fill(self.color['black'])
        self.bindings = DEFAULT_BINDINGS
        self.joysticks = {}
        self._signed_trigger_axes = {}
        self.controller_active = False
        self._trigger_down = False
        self._button_down = set()
        self._menu_down = set()
        self._discover_joysticks()
        self.INPUTS = self._empty_inputs()
        self.make_new_node = False

        self.music_channel = pygame.mixer.Channel(0)
        self.UI_channel = pygame.mixer.Channel(1)
        self.mission_pass_channel = pygame.mixer.Channel(2)
        self.player_SFX_attack = pygame.mixer.Channel(3)

        self.level_ids = []
        self.level_names = []
        with open('Levels/Level-Names.txt', 'r') as f:
            for line in f.read().splitlines():
                if line and not line.startswith('#'):
                    if '|' in line:
                        level_id, display_name = line.split('|', 1)
                    else:
                        # Backward compatibility for pre-title campaign files.
                        level_id = display_name = line
                    self.level_ids.append(level_id.strip())
                    self.level_names.append(display_name.strip())
        self.playing_level_index = 0
        try:
            with open('Max-Level-Unlocked', 'rb'):
                pass
        except FileNotFoundError:
            with open('Max-Level-Unlocked', 'wb') as f:
                pickle.dump(0, f)

    @staticmethod
    def _empty_inputs():
        return {
            'movement': 0, 'movement_vector': pygame.Vector2(), 'facing_vector': pygame.Vector2(),
            'mouse_pos': pygame.Vector2(), 'trigger_action': False, 'plant_bomb': False,
            'knife': False, 'detonate': False, 'pause': False,
            'menu_up': False, 'menu_down': False, 'menu_left': False, 'menu_right': False,
            'menu_confirm': False, 'menu_back': False, 'controller_active': False,
        }

    def _discover_joysticks(self):
        for index in range(pygame.joystick.get_count()):
            try:
                self._open_joystick(index)
            except pygame.error:
                continue
        self._refresh_controller_mode()

    def _open_joystick(self, device_index):
        try:
            joy = pygame.joystick.Joystick(device_index)
            joy.init()
            instance_id = joy.get_instance_id()
            self.joysticks[instance_id] = joy
            trigger_axis = self.bindings['axes']['detonate']
            self._signed_trigger_axes[instance_id] = (
                joy.get_numaxes() > trigger_axis and joy.get_axis(trigger_axis) < -0.5
            )
        except (pygame.error, KeyError, SystemError, IndexError):
            # SDL can briefly report an add event for an index that has already
            # disappeared during a fast Bluetooth reconnect.
            return

    def _refresh_controller_mode(self):
        active = bool(self.joysticks)
        self.controller_active = active
        pygame.mouse.set_visible(not self.isplaying)

    def _handle_device_event(self, event):
        if event.type == pygame.JOYDEVICEADDED:
            # SDL device indices are transient and can be reused on reconnect.
            # Re-enumerate the current list instead of retaining the event index.
            self._discover_joysticks()
        elif event.type == pygame.JOYDEVICEREMOVED:
            removed = self.joysticks.pop(event.instance_id, None)
            self._signed_trigger_axes.pop(event.instance_id, None)
            if removed is not None:
                try:
                    removed.quit()
                except (pygame.error, SystemError):
                    pass
        self._refresh_controller_mode()

    def _events(self):
        events = pygame.event.get()
        self._sync_joysticks()
        for event in events:
            if event.type == pygame.QUIT:
                self.isplaying = False
                self.isrunning = False
        return events

    def _sync_joysticks(self):
        connected = pygame.joystick.get_count()
        if connected != len(self.joysticks):
            for joy in self.joysticks.values():
                try:
                    joy.quit()
                except (pygame.error, SystemError):
                    pass
            self.joysticks.clear()
            self._signed_trigger_axes.clear()
            self._button_down.clear()
            self._menu_down.clear()
            self._trigger_down = False
            self._discover_joysticks()
        else:
            self._refresh_controller_mode()

    @staticmethod
    def _pressed_edge(name, now, previous):
        return name in now and name not in previous

    def _controller_state(self):
        if not self.joysticks:
            return pygame.Vector2(), set(), set(), False
        # Use the first currently connected device, keyed by instance ID rather than
        # a transient OS device index, so reconnects do not retain stale indices.
        instance_id, joy = next(iter(self.joysticks.items()))
        axis = self.bindings['axes']
        x = joy.get_axis(axis['move_x']) if joy.get_numaxes() > axis['move_x'] else 0.0
        y = joy.get_axis(axis['move_y']) if joy.get_numaxes() > axis['move_y'] else 0.0
        vec = pygame.Vector2(x, y)
        dead = self.bindings['dead_zone']
        if vec.length() <= dead:
            vec.xy = (0, 0)
        else:
            magnitude = min(1.0, (vec.length() - dead) / (1.0 - dead))
            vec.scale_to_length(magnitude)
        buttons = set()
        for action, index in self.bindings['buttons'].items():
            if joy.get_numbuttons() > index and joy.get_button(index):
                buttons.add(action)
        hat_x, hat_y = joy.get_hat(self.bindings['hat']) if joy.get_numhats() else (0, 0)
        directions = set()
        if hat_y > 0: directions.add('menu_up')
        if hat_y < 0: directions.add('menu_down')
        if hat_x < 0: directions.add('menu_left')
        if hat_x > 0: directions.add('menu_right')
        trigger = False
        ti = axis['detonate']
        if joy.get_numaxes() > ti:
            raw = joy.get_axis(ti)
            # Pygame/XInput commonly exposes triggers as -1..1; some SDL mappings
            # expose 0..1. Normalize both to a pressed value in 0..1.
            value = (raw + 1.0) / 2.0 if self._signed_trigger_axes.get(instance_id, False) else raw
            trigger = value >= self.bindings['trigger_threshold']
        return vec, buttons, directions, trigger

    def poll_menu_input(self):
        """Poll hot-plug events and produce one-frame menu actions."""
        events = self._events()
        self._refresh_controller_mode()
        inputs = self._empty_inputs()
        inputs['controller_active'] = self.controller_active
        inputs['mouse_pos'].xy = pygame.mouse.get_pos()
        if self.controller_active:
            _, buttons, directions, _ = self._controller_state()
            inputs['menu_up'] = self._pressed_edge('menu_up', directions, self._menu_down)
            inputs['menu_down'] = self._pressed_edge('menu_down', directions, self._menu_down)
            inputs['menu_left'] = self._pressed_edge('menu_left', directions, self._menu_down)
            inputs['menu_right'] = self._pressed_edge('menu_right', directions, self._menu_down)
            inputs['menu_confirm'] = self._pressed_edge('menu_confirm', buttons, self._button_down)
            inputs['menu_back'] = self._pressed_edge('menu_back', buttons, self._button_down)
            self._menu_down = directions
            self._button_down = buttons
        else:
            key_actions = self.bindings['keys']
            for event in events:
                if event.type != pygame.KEYDOWN:
                    continue
                for action in ('menu_up', 'menu_down', 'menu_left', 'menu_right', 'menu_confirm', 'menu_back'):
                    if event.key == key_actions[action]:
                        inputs[action] = True
            self._menu_down = set()
            self._button_down = set()
        self.INPUTS = inputs
        return inputs

    def user_input(self):
        self.INPUTS = self._empty_inputs()
        self.make_new_node = False
        events = self._events()
        self._refresh_controller_mode()
        if self.controller_active:
            move, buttons, _, trigger = self._controller_state()
            self.INPUTS['movement_vector'] = move
            self.INPUTS['facing_vector'] = move.copy()
            self.INPUTS['knife'] = self._pressed_edge('knife', buttons, self._button_down)
            self.INPUTS['plant_bomb'] = self._pressed_edge('plant_bomb', buttons, self._button_down)
            self.INPUTS['trigger_action'] = self._pressed_edge('trigger_action', buttons, self._button_down)
            self.INPUTS['detonate'] = trigger and not self._trigger_down
            self.INPUTS['pause'] = self._pressed_edge('pause', buttons, self._button_down) or self._pressed_edge('menu_back', buttons, self._button_down)
            self._trigger_down = trigger
            self._button_down = buttons
        else:
            key_actions = self.bindings['keys']
            mouse_actions = self.bindings['mouse']
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == key_actions['pause']: self.INPUTS['pause'] = True
                    elif event.key == key_actions['detonate']: self.INPUTS['detonate'] = True
                    elif event.key == key_actions['make_new_node']: self.make_new_node = True
                    elif event.key == key_actions['trigger_action']: self.INPUTS['trigger_action'] = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == mouse_actions['plant_bomb']: self.INPUTS['plant_bomb'] = True
                    elif event.button == mouse_actions['knife']: self.INPUTS['knife'] = True
            keys = pygame.key.get_pressed()
            self.INPUTS['movement'] = int(keys[key_actions['move_forward']]) - int(keys[key_actions['move_backward']])
            self.INPUTS['mouse_pos'].xy = pygame.mouse.get_pos()
            self._trigger_down = False
            self._button_down = set()
        self.INPUTS['controller_active'] = self.controller_active
        if self.INPUTS['pause']:
            self.isplaying = False
            self.menumode = 'pause'
