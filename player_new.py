import random
import pygame, game

pygame.mixer.init()


collision_tollerence = 10


class Player(pygame.Rect):
    def __init__(self, gameObj : game.Game, x : int, y : int, level_name = None):
        self.gameObj = gameObj
        self.side_length = 50
        pygame.Rect.__init__(self, x, y, self.side_length, self.side_length)
        self.speed = 500
        self.direction = pygame.Vector2()
        self.facing_direction = pygame.Vector2(0, -1)
        self.position = pygame.Vector2(self.x, self.y)
        self.render_pos = pygame.Vector2(650, 360)
        self.velocity = pygame.Vector2()
        self.horizontal_block_check = True
        self.vertical_block_check = True
        self.knife_equiped = True
        self.bomb_equiped = 0
        self.health = 130
        self.max_health = self.health
        self.base_img = pygame.transform.smoothscale(pygame.image.load('images/player.png'), self.size)
        self.img = self.base_img
        self.slash_frames = []
        self.slash_started_ms = None
        self.slash_duration_ms = 240
        self.slash_frame_index = 0
        self.slash_direction = self.facing_direction.copy()

        self.sfx_list_knife = (pygame.mixer.Sound('sounds/SFX/knife1.wav'), pygame.mixer.Sound('sounds/SFX/knife2.wav'), pygame.mixer.Sound('sounds/SFX/knifestab.wav'))
        for i in self.sfx_list_knife:
            i.set_volume(0.2)
    
    
    def direction_update(self):
        if not self.gameObj.INPUTS.get('controller_active'):
            direction = self.gameObj.INPUTS['mouse_pos'] - self.render_pos - (self.side_length//2, self.side_length//2)
            if direction.length_squared() > 0:
                self.facing_direction = direction.normalize()
                self.direction = direction
    
    def velocity_update(self):
        inputs = self.gameObj.INPUTS
        if inputs.get('controller_active'):
            move = inputs.get('movement_vector', pygame.Vector2()).copy()
            direction = inputs.get('facing_vector', move).copy()
            if direction.length_squared() > 0:
                self.facing_direction = direction.normalize()
            self.direction = direction
            self.velocity = move * self.speed
        else:
            D = inputs['movement']
            direction = inputs['mouse_pos'] - self.render_pos - (self.side_length // 2, self.side_length // 2)
            if direction.length_squared() > 0:
                self.direction = direction
                self.facing_direction = direction.normalize()
                direction.scale_to_length(self.speed)
                self.velocity = D * direction
            else:
                self.velocity.xy = (0, 0)
        self.vertical_block_check = True
        self.horizontal_block_check = True
    
    def blockage_check(self, walls : list[pygame.Rect]):
        if self.velocity == (0,0):
            return
        for wall in walls:
            if not (self.horizontal_block_check or self.vertical_block_check):
                return
            if not self.colliderect(wall):
                continue

            if self.horizontal_block_check and self.velocity.x > 0 and (self.right - wall.left <= collision_tollerence):
                self.horizontal_block_check = False
                self.velocity.x = 0

            elif self.horizontal_block_check and self.velocity.x < 0 and (wall.right - self.left <= collision_tollerence):
                self.horizontal_block_check = False
                self.velocity.x = 0

            if self.vertical_block_check and self.velocity.y > 0 and (self.bottom - wall.top <= collision_tollerence):
                self.vertical_block_check = False
                self.velocity.y = 0
            
            elif self.vertical_block_check and self.velocity.y < 0 and (wall.bottom - self.top <= collision_tollerence):
                self.vertical_block_check = False
                self.velocity.y = 0
    
    def position_update(self):
        self.position += self.velocity / self.gameObj.fps
        self.topleft = self.position.xy
    
    def draw_entity(self, cam_x, cam_y):
        plr = (self.x - cam_x, self.y - cam_y)
        self.render_pos = plr
        if self.direction.length_squared() > 0:
            self.facing_direction = self.direction.normalize()
        # Pygame's surface rotation and Vector2's screen-space angle use
        # opposite signs here; negate the angle so the sprite follows the
        # same direction as the player arrow.
        angle = -pygame.Vector2(0, -1).angle_to(self.facing_direction)
        rotated = pygame.transform.rotate(self.base_img, angle)
        rect = rotated.get_rect(center=(self.centerx - cam_x, self.centery - cam_y))
        self.gameObj.screen.blit(rotated, rect)

    def set_slash_frames(self, frames):
        self.slash_frames = frames

    def update_slash_animation(self, now_ms=None):
        if self.slash_started_ms is None:
            return
        if now_ms is None:
            now_ms = pygame.time.get_ticks()
        elapsed = now_ms - self.slash_started_ms
        if elapsed >= self.slash_duration_ms:
            self.slash_started_ms = None
            self.slash_frame_index = 0
            return
        self.slash_frame_index = min(
            len(self.slash_frames) - 1,
            int(elapsed * len(self.slash_frames) / self.slash_duration_ms),
        )

    def draw_slash_animation(self, cam_x, cam_y):
        if self.slash_started_ms is None or not self.slash_frames:
            return
        frame = self.slash_frames[self.slash_frame_index]
        # The supplied slash frames are drawn horizontally, pointing right.
        # Rotate a fresh frame copy toward the current facing direction.
        angle = -pygame.Vector2(1, 0).angle_to(self.slash_direction)
        rotated = pygame.transform.rotate(frame, angle)
        center = pygame.Vector2(self.centerx - cam_x, self.centery - cam_y)
        center += self.slash_direction * 35
        self.gameObj.screen.blit(rotated, rotated.get_rect(center=center))

    def knife_attack(self, others : list[pygame.Rect]):
        if not self.knife_equiped:
            return
        self.update_slash_animation()
        if self.slash_started_ms is not None and self.slash_frame_index < 3:
            return
        self.slash_started_ms = pygame.time.get_ticks()
        self.slash_frame_index = 0
        # Inflate by 20% of each current dimension (10 total pixels at 50x50).
        p = self.inflate(round(self.width * 0.2), round(self.height * 0.2))
        hit_targets = [target for target in others if p.colliderect(target)]
        if not hit_targets:
            self.slash_direction = self.facing_direction.copy()
            self.sfx_list_knife[random.randint(0,1)].play()
            return
        direction_sum = pygame.Vector2()
        for target in hit_targets:
            direction_sum += pygame.Vector2(target.center) - pygame.Vector2(self.center)
            target.health -= 10
        self.slash_direction = direction_sum.normalize() if direction_sum.length_squared() else self.facing_direction.copy()
        self.sfx_list_knife[2].play()
        return hit_targets
