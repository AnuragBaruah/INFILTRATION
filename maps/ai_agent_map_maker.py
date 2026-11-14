"""Generate the authored campaign with the runtime schema used by the map editor.

Run from the repository root: ``python maps/ai_agent_map_maker.py``.
Source maps and .mapsupport files are kept in maps/ for future editing.
"""
from __future__ import annotations

import pickle
import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame


ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "maps"
LEVELS = ROOT / "Levels"
CELL_W, CELL_H, BORDER = 1280, 720, 15
MIN_PATROL_NODE_DISTANCE = 72


def level(name, size, style, purpose, messages, *, weak=0, ghosts=0, bombs=0,
          knife=False, checkpoint_count=4, bomb_cluster=False, health=130):
    return {
        "name": name, "size": size, "style": style, "purpose": purpose,
        "messages": messages, "weak": weak, "ghosts": ghosts, "bombs": bombs,
        "knife": knife, "checkpoint_count": checkpoint_count,
        "bomb_cluster": bomb_cluster, "health": health,
    }


# These entries specify distinct play patterns and world sizes. The campaign
# starts with four focused tutorials, then moves into longer mixed challenges.
CAMPAIGN = [
    level("Move", (1, 1), "open", "tutorial", [
        ("MOVE: KB/MOUSE W/S relative to cursor | CONTROLLER left stick.",),
        ("Face the direction you want to travel.", "The blue arrow points to the next green marker."),
        "Follow the green markers in order to clear the route.",
    ], checkpoint_count=3),
    level("Patrol", (1, 1), "lanes", "tutorial", [
        ("MOVE: KB/MOUSE W/S relative to cursor | CONTROLLER left stick.", "Patrols hurt on contact; they follow fixed routes."),
        ("Wait for a patrol to turn, then cross behind it.", "A weak patrol will not chase through the maze."),
        "Keep moving and use the side gap to reach extraction.",
    ], weak=2, checkpoint_count=3),
    level("Knife", (1, 1), "arena", "tutorial", [
        ("MOVE: KB/MOUSE W/S + cursor | CONTROLLER left stick.", "SLASH: KB/MOUSE right mouse | CONTROLLER RB."),
        "Get close before slashing; knife range is short.",
        "A weak patrol needs several hits. Time attacks between passes.",
    ], weak=1, knife=True, checkpoint_count=3),
    level("Bombs", (1, 1), "arena", "tutorial", [
        ("MOVE: KB/MOUSE W/S + cursor | CONTROLLER left stick.", "Walk over a bomb pickup to collect it."),
        ("PLANT: KB/MOUSE left mouse | CONTROLLER A.", "DETONATE: KB/MOUSE Space | CONTROLLER RT."),
        "Plant, run clear of the blast, then detonate the ghost pack.",
    ], ghosts=2, bombs=1, checkpoint_count=3),

    level("Slalom", (2, 1), "zigzag", "movement", [
        "The weak patrols fill the straight route.", "Cut through the alternating openings.",
        "You must reverse direction twice before the exit.",
    ], weak=7, checkpoint_count=4, health=100),
    level("Ghosts", (2, 2), "rooms", "wall chasers", [
        "Ghosts chase when you get close and can pass through walls.",
        "A wall will not protect you. Keep changing direction.",
        "Cross the four rooms and use the long outer loop to escape.",
    ], ghosts=5, checkpoint_count=5, health=115),
    level("Crosswind", (2, 1), "lanes", "patrol timing", [
        "Eight patrols cross the hall on offset routes.", "Use the gaps between their passes.",
        "A short pause can open a safer crossing than a straight dash.",
    ], weak=8, checkpoint_count=4, health=85),
    level("Detour", (2, 2), "switchback", "route reading", [
        "The direct line is blocked in every room.", "Read the wall openings before committing.",
        "Reach the far corner by alternating top and bottom passages.",
    ], weak=4, ghosts=2, checkpoint_count=5),
    level("Maze", (3, 2), "labyrinth", "map memory", [
        "A large maze hides the route between checkpoints.", "The arrow shows direction, not a safe path.",
        "Remember each opening as you cross the six sectors.",
    ], weak=7, checkpoint_count=6, health=100),
    level("DeadReckon", (3, 2), "spiral", "wall chasers and memory", [
        "Ghosts cross walls and close from behind.", "The patrol routes are only in the central halls.",
        "Remember the outer passage; it is the safest way back.",
    ], weak=4, ghosts=5, checkpoint_count=6, health=105),
    level("Pressure", (2, 2), "crossfire", "mixed threats", [
        "Patrols hold the narrow lanes while ghosts cross walls.", "Do not stop in the center room.",
        "Use the upper loop to split the threats, then double back.",
    ], weak=6, ghosts=4, bombs=1, checkpoint_count=5, health=105),
    level("LongHall", (3, 1), "corridor", "movement endurance", [
        "The hall is long and patrols block each crossing.", "Change lanes at every second opening.",
        "Save enough health for the far end; there is no shortcut back.",
    ], weak=11, checkpoint_count=5, health=85),
    level("Ambush", (2, 2), "ambush", "wall chaser timing", [
        "Ghosts wait behind the walls near the objective route.", "They can cut through every barrier.",
        "Bait them into the open, then break away around the next room.",
    ], ghosts=8, checkpoint_count=5, health=95),
    level("Lockdown", (3, 2), "rooms", "large mixed route", [
        "Patrols guard the doors. Ghosts ignore the walls.", "The shortest route crosses the exposed center.",
        "Use the outer halls to reset the chase before the last marker.",
    ], weak=8, ghosts=5, checkpoint_count=6, health=90),
    level("Bloodbath", (2, 2), "arena", "bomb cluster", [
        "Collect the bombs before entering the hostile yard.", "Let the ghosts gather, then plant and escape.",
        "One blast can clear a cluster. Never detonate beside the bomb.",
    ], ghosts=14, bombs=4, checkpoint_count=5, bomb_cluster=True, health=100),
    level("TwinFuses", (2, 1), "arena", "bomb chain", [
        "A dense ghost pack is waiting in the central yard.", "Carry both bombs into the long lane.",
        "Plant, run to the far cover, then detonate. Repeat for stragglers.",
    ], ghosts=10, bombs=3, checkpoint_count=4, bomb_cluster=True, health=95),
    level("Gauntlet", (2, 2), "lanes", "patrol obstacle", [
        "Twelve weak patrols cross the route without chasing.", "Every opening is watched from one side.",
        "Use the side pockets to wait out a bad crossing.",
    ], weak=12, checkpoint_count=5, health=75),
    level("Courtyard", (3, 2), "pillars", "knife combat", [
        "Fourteen patrols hold the pillar courts. No bombs here.", "Knife range is short; slash as a patrol enters reach.",
        "Pick off guards between passes, then cross the open court.",
    ], weak=14, knife=True, checkpoint_count=6, health=95),
    level("NoWayOut", (2, 2), "choke", "bomb escape", [
        "The ghosts will converge on the narrow bridge.", "Collect the bombs on the way in.",
        "Plant at the choke, retreat through the side gate, then detonate.",
    ], ghosts=12, bombs=4, checkpoint_count=5, bomb_cluster=True),
    level("Lost", (3, 2), "deadends", "navigation memory", [
        "Six sectors, three dead ends, and a looping outer wall.", "The arrow cannot show which doorway is open.",
        "Mark the route in your head before you sprint for the exit.",
    ], weak=9, ghosts=2, checkpoint_count=6, health=90),
    level("LastPatrol", (2, 2), "crossing", "patrol timing", [
        "The patrols overlap at the final crossing.", "Use the waiting bays; do not fight in the lanes.",
        "The last marker sits beyond the longest patrol loop.",
    ], weak=14, checkpoint_count=5, health=70),
    level("Breach", (2, 1), "choke", "knife and bomb", [
        "Weak patrols hold the breach; ghosts close in from behind walls.", "Use the knife only when a patrol blocks the doorway.",
        "Save bombs for the crowded room beyond the breach.",
    ], weak=5, ghosts=7, bombs=3, knife=True, checkpoint_count=4, bomb_cluster=True, health=100),
    level("Silent", (3, 2), "lanes", "stealth route", [
        "Ten patrols can hurt you, but none will chase.", "Learn their loops and cross one lane at a time.",
        "The outer route is longer and leaves more room to recover.",
    ], weak=10, checkpoint_count=6, health=80),
    level("Finale", (3, 2), "final", "campaign finale", [
        "Patrols hold the doors while a ghost pack hunts you.", "Pick up all five bombs before the central arena.",
        "Use the maze to gather the ghosts, clear a path, and extract.",
    ], weak=8, ghosts=14, bombs=5, knife=True, checkpoint_count=7, bomb_cluster=True, health=80),
]


def wall_rect(x, y, w, h):
    return {"top_left": (int(x), int(y)), "bottom_right": (int(x + w), int(y + h))}


def outer_walls(cols, rows):
    width, height = cols * CELL_W, rows * CELL_H
    return [
        wall_rect(0, 0, width, BORDER), wall_rect(0, height - BORDER, width, BORDER),
        wall_rect(0, 0, BORDER, height), wall_rect(width - BORDER, 0, BORDER, height),
    ]


def divider_walls(cols, rows, style):
    """Make connected routes with style-specific patterns across each cell seam."""
    walls = []
    width, height = cols * CELL_W, rows * CELL_H
    if style in ("open", "arena", "pillars", "crossfire", "final"):
        return walls
    gap = 120 if style == "choke" else (290 if style == "rooms" else 230)
    # Each cell seam has one door per adjacent cell pair. Matching horizontal
    # and vertical doors keep the whole maze connected without making it open.
    for cx in range(1, cols):
        x = cx * CELL_W
        for cy in range(rows):
            top, bottom = cy * CELL_H + BORDER, (cy + 1) * CELL_H - BORDER
            frac = (0.28 if (cx + cy) % 2 == 0 else 0.72) if style in ("zigzag", "maze", "choke") else 0.5
            center = int(cy * CELL_H + CELL_H * frac)
            lo, hi = center - gap // 2, center + gap // 2
            walls.extend((wall_rect(x - 20, top, 40, lo - top), wall_rect(x - 20, hi, 40, bottom - hi)))
    for cy in range(1, rows):
        y = cy * CELL_H
        for cx in range(cols):
            left, right = cx * CELL_W + BORDER, (cx + 1) * CELL_W - BORDER
            frac = (0.72 if (cx + cy) % 2 == 0 else 0.28) if style in ("zigzag", "maze", "choke") else 0.5
            center = int(cx * CELL_W + CELL_W * frac)
            lo, hi = center - gap // 2, center + gap // 2
            walls.extend((wall_rect(left, y - 20, lo - left, 40), wall_rect(hi, y - 20, right - hi, 40)))
    return walls


def extra_walls(cols, rows, style):
    width, height = cols * CELL_W, rows * CELL_H
    walls = []
    # Hand-shaped obstacles emphasize different movement decisions.
    if style == "zigzag":
        for i, x in enumerate((int(width * .38), int(width * .68))):
            y = 35 if i == 0 else height - 220
            walls.append(wall_rect(x, y, 240, 170))
    elif style in ("lanes", "crossfire"):
        for row in range(rows):
            y = row * CELL_H + (130 if row % 2 == 0 else 410)
            for x in (int(width * .32), int(width * .62)):
                walls.append(wall_rect(x, y, 210, 45))
    elif style in ("switchback", "maze"):
        for col in range(cols):
            x = col * CELL_W + (350 if col % 2 == 0 else 820)
            walls.append(wall_rect(x, 100, 55, int(height * .38)))
            walls.append(wall_rect(x, int(height * .60), 55, int(height * .34)))
    elif style == "rooms":
        for col in range(cols):
            for row in range(rows):
                x, y = col * CELL_W + 760, row * CELL_H + 390
                walls.append(wall_rect(x, y, 230, 48))
    elif style == "pillars":
        for col in range(cols):
            for row in range(rows):
                base_x, base_y = col * CELL_W, row * CELL_H
                walls.extend((wall_rect(base_x + 360, base_y + 210, 110, 110), wall_rect(base_x + 850, base_y + 420, 110, 110)))
    elif style == "ambush":
        for col in range(cols):
            for row in range(rows):
                base_x, base_y = col * CELL_W, row * CELL_H
                walls.extend((wall_rect(base_x + 390, base_y + 175, 48, 300), wall_rect(base_x + 850, base_y + 280, 48, 300)))
    elif style == "final":
        for col in range(cols):
            for row in range(rows):
                base_x, base_y = col * CELL_W, row * CELL_H
                walls.extend((wall_rect(base_x + 250, base_y + 230, 260, 45), wall_rect(base_x + 720, base_y + 420, 300, 45)))
    elif style == "labyrinth":
        for col in range(cols):
            for row in range(rows):
                x, y = col * CELL_W, row * CELL_H
                walls.extend((
                    wall_rect(x + 420, y + 65, 42, 230), wall_rect(x + 420, y + 405, 42, 245),
                    wall_rect(x + 820, y + 150, 42, 250), wall_rect(x + 820, y + 510, 42, 150),
                    wall_rect(x + 462, y + 290, 250, 42), wall_rect(x + 600, y + 500, 220, 42),
                ))
    elif style == "spiral":
        for col in range(cols):
            for row in range(rows):
                x, y = col * CELL_W, row * CELL_H
                if (col + row) % 2 == 0:
                    walls.extend((wall_rect(x+210,y+125,790,42), wall_rect(x+958,y+167,42,350),
                                  wall_rect(x+350,y+475,608,42), wall_rect(x+350,y+300,42,175)))
                else:
                    walls.extend((wall_rect(x+280,y+555,790,42), wall_rect(x+280,y+205,42,350),
                                  wall_rect(x+322,y+205,608,42), wall_rect(x+888,y+247,42,180)))
    elif style == "deadends":
        for col in range(cols):
            for row in range(rows):
                x, y = col * CELL_W, row * CELL_H
                walls.extend((wall_rect(x+260,y+110,46,340), wall_rect(x+306,y+110,340,46),
                              wall_rect(x+646,y+156,46,245), wall_rect(x+692,y+355,300,46),
                              wall_rect(x+946,y+401,46,220)))
    elif style == "crossing":
        for col in range(cols):
            for row in range(rows):
                x,y=col*CELL_W,row*CELL_H
                walls.extend((wall_rect(x+370,y+110,250,42),wall_rect(x+660,y+300,250,42),
                              wall_rect(x+370,y+500,250,42),wall_rect(x+620,y+155,42,145),
                              wall_rect(x+910,y+340,42,160)))
    return walls


def level_walls(spec):
    cols, rows = spec["size"]
    walls = outer_walls(cols, rows)
    walls += divider_walls(cols, rows, spec["style"])
    walls += extra_walls(cols, rows, spec["style"])
    return walls


def wall_rects(walls):
    return [pygame.Rect(w["top_left"], (w["bottom_right"][0]-w["top_left"][0], w["bottom_right"][1]-w["top_left"][1])) for w in walls]


def point_clear(point, rects, padding=0):
    return not any(r.inflate(padding * 2, padding * 2).collidepoint(point) for r in rects)


def missions(spec, rects):
    cols, rows = spec["size"]
    # A serpentine cell route stretches large levels across the whole map.
    cells = [(cx, cy) for cy in range(rows) for cx in (range(cols) if cy % 2 == 0 else range(cols-1, -1, -1))]
    if spec["purpose"] == "tutorial":
        preferred = [(105, 360), (CELL_W*.55, CELL_H*.72), (CELL_W*.82, CELL_H*.38)]
    elif cols * rows == 1:
        preferred = [(CELL_W*.22,CELL_H*.72),(CELL_W*.55,CELL_H*.25),(CELL_W*.82,CELL_H*.7)]
    else:
        preferred = []
        for i in range(spec["checkpoint_count"]):
            cx, cy = cells[i % len(cells)]
            lap = i // len(cells)
            xoff = .30 if (i + lap) % 2 == 0 else .70
            yoff = .30 if (i + lap // 2) % 2 == 0 else .70
            preferred.append((cx*CELL_W + CELL_W*xoff, cy*CELL_H + CELL_H*yoff))
    candidates = [(x, y) for y in range(80, rows*CELL_H-40, 80) for x in range(80, cols*CELL_W-40, 80)]
    result = []
    for want in preferred[:spec["checkpoint_count"]]:
        options = sorted(set(candidates + [(int(want[0]), int(want[1]))]), key=lambda p: (p[0]-want[0])**2 + (p[1]-want[1])**2)
        point = next((p for p in options if p not in result and point_clear(p, rects, 40)), None)
        if point is None:
            raise ValueError(f"No clear checkpoint for {spec['name']} near {want}")
        result.append(point)
    return result


def width_of(spec): return spec["size"][0] * CELL_W
def height_of(spec): return spec["size"][1] * CELL_H


def actor_positions(spec, rects, targets):
    cols, rows = spec["size"]
    player = (80, CELL_H // 2 - 25)
    enemies, occupied = [], [player, *targets]
    width, height = width_of(spec), height_of(spec)
    if spec["bomb_cluster"]:
        cluster = (width * .72, height * .52)
        for idx in range(spec["ghosts"]):
            angle = idx * 2.39996
            radius = 65 + (idx % 4) * 42
            desired = (int(cluster[0] + __import__('math').cos(angle)*radius), int(cluster[1] + __import__('math').sin(angle)*radius))
            fallback = [(int(x),int(y)) for y in range(int(cluster[1]-250),int(cluster[1]+251),50)
                        for x in range(int(cluster[0]-250),int(cluster[0]+251),50)]
            candidates = [desired] + sorted(fallback,key=lambda p:(p[0]-desired[0])**2+(p[1]-desired[1])**2)
            p = next((p for p in candidates if 40<=p[0]<width-40 and 40<=p[1]<height-40
                      and point_clear((p[0]+25,p[1]+25),rects,35)
                      and all((p[0]-q[0])**2+(p[1]-q[1])**2>=55**2 for q in enemies)
                      and all((p[0]+25-t[0])**2+(p[1]+25-t[1])**2>=110**2 for t in targets)),None)
            if p is None: raise ValueError(f"Cannot fit bomb target cluster for {spec['name']}")
            enemies.append((p[0],p[1],"basic")); occupied.append(p)
    # Patrols and wall-crossing chasers are deliberately placed in different
    # cells and corridors. The chase packs gather around chokepoints.
    for kind, count in (("weak", spec["weak"]), ("basic", spec["ghosts"] if not spec["bomb_cluster"] else 0)):
        for idx in range(count):
            if kind == "basic" and spec["style"] in ("ambush", "choke", "maze", "rooms"):
                col = min(cols-1, max(0, (idx % max(cols,1))))
                row = min(rows-1, idx % rows)
                want = (col*CELL_W + CELL_W*.72, row*CELL_H + CELL_H*.52)
            else:
                col = (idx * 2 + (1 if kind == "basic" else 0)) % cols
                row = (idx + (0 if kind == "weak" else 1)) % rows
                want = (col*CELL_W + (CELL_W*.32 if idx%2==0 else CELL_W*.72), row*CELL_H + (CELL_H*.38 if idx%2==0 else CELL_H*.68))
            choices = [(int(x),int(y)) for y in range(max(60,int(want[1])-220),min(height-100,int(want[1])+221),50)
                       for x in range(max(100,int(want[0])-220),min(width-100,int(want[0])+221),50)]
            p = next((p for p in sorted(choices,key=lambda p:(p[0]-want[0])**2+(p[1]-want[1])**2)
                      if p not in occupied and point_clear((p[0]+25,p[1]+25),rects,40)
                      and (p[0]-player[0])**2+(p[1]-player[1])**2 > 400**2), None)
            if p is None:
                raise ValueError(f"No safe {kind} spawn for {spec['name']} at {want}")
            enemies.append((p[0],p[1],kind)); occupied.append(p)
    return player, enemies


def patrol_graph(enemies, rects, spec):
    nodes=[]
    if not enemies:
        enemies=[(int(width_of(spec)*.65),int(height_of(spec)*.5),"weak")]
    for ex,ey,_kind in enemies:
        center=(ex+25,ey+25)
        candidates=[((ex-170,ey+25),(ex+170,ey+25)),((ex+25,ey-170),(ex+25,ey+170)),((ex-140,ey-140),(ex+140,ey+140))]
        pair=next((pair for pair in candidates if all(20<=p[0]<width_of(spec)-20 and 20<=p[1]<height_of(spec)-20 and point_clear(p,rects,18) for p in pair)
                  and not any(r.clipline(pair[0],pair[1]) for r in rects)),None)
        if pair is None:
            # Keep candidate nodes local and connected even in tight passages.
            pair=((max(40,ex-100),ey+25),(min(width_of(spec)-40,ex+100),ey+25))
        for p in pair:
            if p not in nodes: nodes.append(p)
    lines=[]
    for i,p in enumerate(nodes):
        visible=[j for j,q in enumerate(nodes) if j!=i
                 and pygame.Vector2(p).distance_to(q) >= MIN_PATROL_NODE_DISTANCE
                 and not any(r.clipline(p,q) for r in rects)]
        lines.append(tuple(visible))
    # Guarantee every patrol endpoint has a visible partner; nodes were added in pairs.
    for i,row in enumerate(lines):
        if not row:
            partner=i-1 if i%2 else i+1
            if (0<=partner<len(nodes)
                    and pygame.Vector2(nodes[i]).distance_to(nodes[partner]) >= MIN_PATROL_NODE_DISTANCE):
                lines[i]=(partner,)
                existing=list(lines[partner]); existing.append(i); lines[partner]=tuple(sorted(set(existing)))
    return nodes,lines


def grid_wall_map(walls, cols, rows):
    result={}
    rects=wall_rects(walls)
    for gx in range(cols):
        for gy in range(rows):
            box=pygame.Rect(gx*CELL_W-150,gy*CELL_H-150,CELL_W+300,CELL_H+300)
            result[(gx,gy)]=[wall for wall,rect in zip(walls,rects) if box.colliderect(rect)]
    return result


def map_data(spec):
    cols,rows=spec["size"]
    walls=level_walls(spec); rects=wall_rects(walls)
    targets=missions(spec,rects)
    player,enemies=actor_positions(spec,rects,targets)
    nodes,lines=patrol_graph(enemies,rects,spec)
    # Place bomb caches on the approach to the most dangerous area.
    bombs=[]
    for i in range(spec["bombs"]):
        want=(width_of(spec)*(.3+.08*i),height_of(spec)*(.78 if i%2==0 else .25))
        candidates=[(x,y) for y in range(80,int(height_of(spec))-40,80) for x in range(80,int(width_of(spec))-40,80)]
        p=next((p for p in sorted(candidates,key=lambda p:(p[0]-want[0])**2+(p[1]-want[1])**2) if point_clear(p,rects,30) and p not in bombs),None)
        if p is None: raise ValueError(f"No bomb cache location for {spec['name']}")
        bombs.append(p)
    return {
        "walls":grid_wall_map(walls,cols,rows), "path_nodes":nodes, "path_lines":lines,
        "mission_pointers":targets, "enemy_data":enemies, "player_data":player,
        "bomb_positions":bombs,
    }


def mission_module(spec,index):
    track=("bass.wav","bass1.wav","bassanddrum.wav","drums1.wav","all.wav")[index%5]
    lines=["from Levels import commonfunctions as CFS","",f"## checkpoint events for {spec['name']}",
           f"starting_health = {spec['health']}",f"bgm = CFS.sound_loader('./sounds/music/{track}')",""]
    messages=list(spec["messages"])
    continuation=("Route updated. Take the next opening.","Another sector cleared. Keep your pace.","The final stretch is ahead. Stay alert.")
    while len(messages)<spec["checkpoint_count"]:
        messages.append(continuation[(len(messages)-len(spec["messages"]))%len(continuation)])
    for i,message in enumerate(messages[:spec["checkpoint_count"]]):
        message_lines = (message,) if isinstance(message, str) else tuple(message)
        lines += [f"msg{i} = CFS.create_messages({message_lines!r})",f"def func{i}(gameObj, levelObj=None):"]
        if i==0 and not spec["knife"]: lines.append("    levelObj.player.knife_equiped = False")
        if i==0 and spec["knife"]: lines.append("    levelObj.player.knife_equiped = True")
        if i==1: lines.append("    gameObj.music_channel.play(bgm, -1)")
        if i==spec["checkpoint_count"]-1: lines.append("    gameObj.music_channel.stop()")
        lines += ["    CFS.play_sound(gameObj.mission_pass_channel)",f"    return CFS.render_messages, (gameObj.screen, msg{i}), gameObj.fps * 9",""]
    return "\n".join(lines)


def export_backgrounds(spec,data,index):
    name=spec["name"]
    texture=("dark.png","darkest.png","mid.png","light.png")[index%4]
    wall_color=((48,64,76),(55,53,68),(48,72,64),(78,62,52))[index%4]
    base=pygame.image.load(str(MAPS/texture)).convert()
    cols,rows=spec["size"]
    for (gx,gy),cell_walls in data["walls"].items():
        tile=base.copy()
        for wall in cell_walls:
            x,y=wall["top_left"]; right,bottom=wall["bottom_right"]
            clipped=pygame.Rect(x-gx*CELL_W,y-gy*CELL_H,right-x,bottom-y).clip(pygame.Rect(0,0,CELL_W,CELL_H))
            if clipped.width and clipped.height: pygame.draw.rect(tile,wall_color,clipped)
        out=LEVELS/name/f"{name}-bgpics"/f"{name}-{gx}-{gy}.png"
        out.parent.mkdir(parents=True,exist_ok=True)
        pygame.image.save(tile,str(out))


def write_level(spec, data, index, *, write_source=True):
    name=spec["name"]
    if write_source:
        with (MAPS/f"{name}.map").open("wb") as f: pickle.dump(data,f,pickle.HIGHEST_PROTOCOL)
        with (MAPS/f"{name}.mapsupport").open("wb") as f:
            pickle.dump("none.png",f); pickle.dump(spec["size"][0],f); pickle.dump(spec["size"][1],f)
    dest=LEVELS/name; dest.mkdir(parents=True,exist_ok=True)
    with (dest/f"{name}.map").open("wb") as f: pickle.dump(data,f,pickle.HIGHEST_PROTOCOL)
    export_backgrounds(spec,data,index)
    (LEVELS/f"{name}.py").write_text(mission_module(spec,index),encoding="utf-8")


def main():
    pygame.init(); pygame.display.set_mode((CELL_W,CELL_H))
    names=[]
    for index,spec in enumerate(CAMPAIGN):
        data=map_data(spec); write_level(spec,data,index); names.append(spec["name"])
    (LEVELS/"Level-Names.txt").write_text("# Tutorials first, then the main campaign.\n##\n"+"\n".join(names)+"\n",encoding="utf-8")
    (LEVELS/"__init__.py").write_text("__all__ = "+repr(names)+"\n",encoding="utf-8")
    pygame.quit()
    print(f"Generated {len(names)} levels: 4 tutorials and 20 main challenges.")


if __name__=="__main__": main()
