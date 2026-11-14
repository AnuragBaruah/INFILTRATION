import math
import pygame


class Effects:
    """Level-owned temporary combat effects, positioned in world coordinates."""
    def __init__(self, screen_size):
        self.knife_frames = [pygame.image.load(f'images/blood_slash/blood_slash{i}.png').convert_alpha() for i in range(12)]
        self.bomb_image = pygame.image.load('images/blood.png').convert_alpha()
        self.effects = []
        self.screen_size = screen_size
        self.hurt_until_ms = 0

    def add_knife_hit(self, position):
        self.effects.append({'kind': 'knife', 'pos': pygame.Vector2(position), 'start': pygame.time.get_ticks()})

    def add_bomb_kill(self, position, bomb_position):
        direction = pygame.Vector2(position) - pygame.Vector2(bomb_position)
        if direction.length_squared() == 0:
            direction.update(1, 0)
        # Art points at 45 degrees counter-clockwise from +X; rotate it radially.
        source = pygame.Vector2(math.sqrt(0.5), -math.sqrt(0.5))
        angle = -source.angle_to(direction)
        image = pygame.transform.rotate(self.bomb_image, angle)
        image.set_alpha(255)
        self.effects.append({'kind': 'bomb', 'pos': pygame.Vector2(position), 'image': image, 'start': pygame.time.get_ticks()})

    def player_hurt(self):
        self.hurt_until_ms = pygame.time.get_ticks() + 90

    def update(self, now_ms=None):
        now_ms = pygame.time.get_ticks() if now_ms is None else now_ms
        alive = []
        for effect in self.effects:
            age = now_ms - effect['start']
            lifetime = 10000 if effect['kind'] == 'bomb' else 12 * 28
            if age < lifetime:
                alive.append(effect)
        self.effects = alive

    def _render_kind(self, screen, cam_x, cam_y, kind, now_ms):
        for effect in self.effects:
            if effect['kind'] != kind:
                continue
            age = now_ms - effect['start']
            if kind == 'knife':
                frame_index = min(11, age // 28)
                img = pygame.transform.smoothscale(self.knife_frames[frame_index], (64, 64))
            else:
                img = effect['image'].copy()
                img.set_alpha(max(0, int(255 * (1 - age / 10000))))
            rect = img.get_rect(center=(effect['pos'].x - cam_x, effect['pos'].y - cam_y))
            screen.blit(img, rect)

    def render_ground(self, screen, cam_x, cam_y, now_ms=None):
        now_ms = pygame.time.get_ticks() if now_ms is None else now_ms
        self._render_kind(screen, cam_x, cam_y, 'bomb', now_ms)

    def render(self, screen, cam_x, cam_y, now_ms=None):
        now_ms = pygame.time.get_ticks() if now_ms is None else now_ms
        self._render_kind(screen, cam_x, cam_y, 'knife', now_ms)

    def render_hurt_overlay(self, screen, now_ms=None):
        now_ms = pygame.time.get_ticks() if now_ms is None else now_ms
        remaining = self.hurt_until_ms - now_ms
        if remaining > 0:
            overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
            overlay.fill((255, 0, 0, int(120 * remaining / 90)))
            screen.blit(overlay, (0, 0))
