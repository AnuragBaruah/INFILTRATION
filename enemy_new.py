import pickle
import random
import pygame, player_new


# Route points closer than this tend to make patrols flip direction repeatedly
# because their collision boxes overlap both points at once.
MIN_PATROL_NODE_DISTANCE = 72

class Enemy_Basic(player_new.Player):
    def __init__(self, gameObj, x, y, level_name):
        player_new.Player.__init__(self, gameObj, x, y, level_name)
        self.ischasing = False
        self.chase_timer = 0
        self.normal_speed = 300
        self.chasing_speed = 450
        self.speed = self.normal_speed
        self.satisfied = 0
        self.health = 30
        self.vector_to_player = pygame.Vector2()
        with open(f'Levels/{level_name}/{level_name}.map', 'rb') as f:
            data = pickle.load(f)
        self.path_nodes = data['path_nodes']
        self.path_lines = data['path_lines']
        self.reset_nodes()
        self.base_img = pygame.transform.smoothscale(pygame.image.load('images/enemyb.png'), self.size)
        self.img = self.base_img
        self.draw_facing_arrow = False

        self.sfx_list_knife = (pygame.mixer.Sound('sounds/SFX/enemyknife1.wav'), pygame.mixer.Sound('sounds/SFX/enemyknife2.wav'), pygame.mixer.Sound('sounds/SFX/enemyknifestab.wav'))
        for i in self.sfx_list_knife:
            i.set_volume(0.2)
    
    def reset_nodes(self):
        # Ignore malformed, duplicate, and near-duplicate links in authored maps.
        # Keep the original node indices so enemy spawn locations still select
        # the same part of the patrol route.
        node_count = len(self.path_nodes)
        clean_lines = []
        for source, neighbors in enumerate(self.path_lines):
            valid = []
            for target in neighbors:
                if not 0 <= target < node_count or target == source:
                    continue
                if pygame.Vector2(self.path_nodes[source]).distance_to(self.path_nodes[target]) >= MIN_PATROL_NODE_DISTANCE:
                    valid.append(target)
            clean_lines.append(tuple(dict.fromkeys(valid)))
        self.path_lines = clean_lines

        m_min = 100000
        self.node_from = -1
        for i in range(len(self.path_nodes)):
            v = self.position - self.path_nodes[i]
            m = v.magnitude()
            if m < m_min:
                m_min = m
                self.node_from = i
        t = list(self.path_lines[self.node_from])
        if not t:
            t = [i for i, node in enumerate(self.path_nodes)
                 if i != self.node_from and pygame.Vector2(self.path_nodes[self.node_from]).distance_to(node) >= MIN_PATROL_NODE_DISTANCE]
        self.node_to = random.choice(t) if t else self.node_from
    
    def change_patrolling_direction(self):
        self.node_from = self.node_to
        t = list(self.path_lines[self.node_to])
        if not t:
            t = [i for i, node in enumerate(self.path_nodes)
                 if i != self.node_to and pygame.Vector2(self.path_nodes[self.node_to]).distance_to(node) >= MIN_PATROL_NODE_DISTANCE]
        self.node_to = random.choice(t) if t else self.node_from

    def patrolling(self):
        if self.node_to == self.node_from or not self.path_nodes:
            self.velocity.xy = (0, 0)
            return
        if self.collidepoint(self.path_nodes[self.node_to]):
            self.change_patrolling_direction()
        self.direction = self.path_nodes[self.node_to] - self.position
        if self.direction.length_squared() == 0:
            self.velocity.xy = (0, 0)
        else:
            self.direction.scale_to_length(self.speed)
            self.velocity = self.direction.copy()

    def chase_direction_update(self):
        self.direction = self.vector_to_player.copy()

    def chase_velocity_update(self):
        self.speed = self.chasing_speed
        self.direction = self.vector_to_player.copy()
        self.direction.scale_to_length(self.speed)
        self.velocity = self.direction.copy()

    def velocity_update(self, other, walls):
        if self.chase_timer and not self.satisfied:
            self.chase_velocity_update()
            if self.vector_to_player.magnitude() < 100:
                self.knife_attack(other)
            self.chase_timer -= 1
        else:
            self.speed = self.normal_speed
            self.patrolling()
            if self.satisfied:
                self.satisfied -= 1 

    def update_anger_state(self, other : player_new.Player):
        self.vector_to_player = other.position - self.position
        if not self.chase_timer:
            if self.vector_to_player.magnitude() < 400:
                self.chase_timer = 20
    
    def knife_attack(self, other : pygame.Rect):
        if self.colliderect(other):
            self.sfx_list_knife[2].play()
            self.satisfied = 100
            other.health -= 1
            self.sfx_list_knife[random.randint(0,1)].play()
            return
        else:
            self.sfx_list_knife[random.randint(0,1)].play()


class Enemy_Weak(Enemy_Basic):
    def __init__(self, gameObj, x, y, level_name):
        Enemy_Basic.__init__(self, gameObj, x, y, level_name)
        self.health = 50
        self.speed = self.chasing_speed
        self.path_nodes = [self.path_nodes[self.node_from], self.path_nodes[self.node_to]]
        self.path_lines = [(1,), (0,)]
        self.node_from = 0
        self.node_to = 1
        self.base_img = pygame.transform.smoothscale(pygame.image.load('images/enemyw.png'), self.size)
        self.img = self.base_img
    
    def velocity_update(self, other, walls):
        self.vector_to_player = other.position - self.position
        self.patrolling()
        self.blockage_check(walls)
        if self.vector_to_player.magnitude() < 100:
            self.knife_attack(other)


