"""Generate the authored 4-tutorial + 20-level INFILTRATION campaign.

Run from the repository root with ``python maps/ai_agent_map_maker.py``.
Maps use the same pickle schema and package layout as ultimate_map_maker.py.
The source maps and .mapsupport files remain in maps/ for later editing.
"""
from __future__ import annotations

import os
import pickle
from pathlib import Path

import pygame


ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "maps"
LEVELS_DIR = ROOT / "Levels"
CELL_W, CELL_H, BORDER = 1280, 720, 15

# name, teaching/challenge focus, mission messages, enemy count, bombs, knife unlock checkpoint
CAMPAIGN = [
    ("T01_FirstSteps", "tutorial", ["Welcome, operative.", "Reach the green checkpoints in order.", "Keep moving through the open training yard."], 0, [], None),
    ("T02_ReadThePatrol", "tutorial", ["Patrols move between connected route nodes.", "Watch the guard, then cross behind it.", "Checkpoint reached. Keep your distance."], 1, [], None),
    ("T03_CloseQuarters", "tutorial", ["Your knife is ready for close combat.", "Approach the weak guard and use a knife slash.", "Cross the yard after the patrol turns away."], 1, [], 0),
    ("T04_BombSafety", "tutorial", ["Bombs are collected by walking over them.", "Plant one near the hostile, then retreat.", "Detonate only after you have left the blast."], 1, [(180, 560)], None),
    ("L01_QuietApproach", "stealth", ["Stay wide of the patrol's sightline.", "Use the south opening to cross the yard.", "Reach the extraction marker."], 1, [], None),
    ("L02_CoverToCover", "cover", ["Use the staggered barriers as cover.", "Cross between patrol passes.", "Secure the far checkpoint."], 2, [], None),
    ("L03_TheLongHall", "corridor", ["The hall narrows ahead.", "Take the side opening before the guard turns.", "Clear the final checkpoint."], 2, [], None),
    ("L04_Crossfire", "crossfire", ["Two patrol routes overlap in the center.", "Choose a lane and keep moving.", "Reach the exit beyond the crossfire."], 2, [], None),
    ("L05_TheSupplyCache", "bomb", ["A bomb cache is marked near your start.", "Collect it before entering the guard's lane.", "Retreat from the blast before detonating."], 2, [(180, 565)], None),
    ("L06_Switchback", "switchback", ["The walls form a switchback route.", "Follow the open turns around the barriers.", "The last marker is beyond the second bend."], 2, [], None),
    ("L07_PatrolClock", "timing", ["This patrol crosses the central lane.", "Wait for it to move away, then pass.", "Reach the west side without getting pinned."], 2, [], None),
    ("L08_ThePillars", "pillars", ["Pillars break up the open sightlines.", "Use the gaps to approach the next marker.", "Exit through the northeast lane."], 2, [], None),
    ("L09_CloseQuarters", "knife", ["A weak guard blocks the short route.", "Close the distance and use your knife.", "Continue to the extraction point."], 2, [], 0),
    ("L10_BlastRadius", "bomb", ["Collect the bomb before the central room.", "Plant it near the patrol, then back away.", "Detonate from a safe position and extract."], 2, [(180, 565)], None),
    ("L11_ThreeLanes", "route choice", ["Three lanes lead across the yard.", "The center is fastest; the sides are safer.", "Choose a route and reach the far marker."], 3, [], None),
    ("L12_TheGauntlet", "escape", ["The guards are close together here.", "Break contact and keep to the outer route.", "Do not stop in the center lane."], 3, [], None),
    ("L13_DeadDrop", "bomb", ["A supply drop is waiting near the start.", "Take the bomb and enter the marked yard.", "Create space before you detonate."], 2, [(180, 565)], None),
    ("L14_RedCorridor", "corridor", ["A narrow corridor splits the room.", "Use the two openings to avoid the patrols.", "The extraction marker is on the far side."], 3, [], None),
    ("L15_RelayRun", "route", ["Move through the relay markers in order.", "The middle checkpoint is exposed.", "Keep moving to reach the final relay."], 3, [], None),
    ("L16_TheBlindCorner", "ambush", ["A guard patrols behind the central wall.", "Approach through the lower opening.", "Turn the corner only when the route is clear."], 2, [], None),
    ("L17_SilentExit", "stealth", ["Avoid contact and keep your health intact.", "Use the gaps between the patrol lanes.", "Reach the exit on the far edge."], 3, [], None),
    ("L18_BreachPoint", "knife and bomb", ["A guard holds the breach point.", "Use the cache if you need to clear the route.", "The final checkpoint is behind the breach."], 3, [(180, 565)], 0),
    ("L19_LastPatrol", "timing", ["This final patrol crosses your route twice.", "Use the side cover and watch its turn.", "Reach the extraction marker to finish."], 3, [], None),
    ("L20_Extraction", "final challenge", ["Final operation: reach all three markers.", "Two patrol lanes cover the direct approach.", "Secure the last marker to complete the campaign."], 4, [(180, 565)], 0),
]


def boundary_walls():
    return [
        {"top_left": (0, 0), "bottom_right": (CELL_W, BORDER)},
        {"top_left": (0, CELL_H - BORDER), "bottom_right": (CELL_W, CELL_H)},
        {"top_left": (0, 0), "bottom_right": (BORDER, CELL_H)},
        {"top_left": (CELL_W - BORDER, 0), "bottom_right": (CELL_W, CELL_H)},
    ]


def interior_walls(index: int):
    # Every layout leaves broad openings and keeps the ordered objective route clear.
    layouts = [
        [],
        [(390, 170, 105, 190), (700, 375, 110, 180)],
        [(360, 15, 35, 390), (650, 315, 35, 390), (950, 15, 35, 390)],
        [(410, 185, 95, 95), (760, 435, 95, 95), (930, 185, 95, 95)],
        [(350, 200, 150, 45), (590, 360, 150, 45), (850, 200, 150, 45)],
        [(440, 15, 55, 245), (440, 455, 55, 250), (780, 15, 55, 250), (780, 455, 55, 250)],
        [(350, 185, 45, 350), (600, 15, 45, 300), (600, 420, 45, 285), (895, 185, 45, 350)],
        [(370, 125, 80, 80), (540, 275, 80, 80), (710, 425, 80, 80), (900, 170, 80, 80)],
    ]
    boxes = layouts[index % len(layouts)]
    walls = boundary_walls()
    walls.extend({"top_left": (x, y), "bottom_right": (x + w, y + h)} for x, y, w, h in boxes)
    return walls


def missions(index: int):
    # Intro objective is always within a short, safe walk of the spawn.
    routes = [
        [(260, 230), (640, 540), (1080, 470)],
        [(280, 525), (690, 210), (1085, 525)],
        [(280, 220), (650, 520), (1080, 225)],
        [(270, 520), (640, 205), (1080, 500)],
    ]
    walls = [pygame.Rect(w["top_left"], (w["bottom_right"][0] - w["top_left"][0], w["bottom_right"][1] - w["top_left"][1])) for w in interior_walls(index)]
    candidates = [(x, y) for y in (180, 230, 300, 390, 470, 540) for x in (240, 300, 400, 520, 650, 740, 860, 980, 1080)]
    result = []
    for preferred in routes[index % len(routes)]:
        point = next((p for p in sorted(candidates, key=lambda p: (p[0]-preferred[0])**2+(p[1]-preferred[1])**2)
                      if p not in result and not any(r.inflate(60, 60).collidepoint(p) for r in walls)), None)
        if point is None:
            raise ValueError(f"No clear mission point for campaign map {index}")
        result.append(point)
    return result


def nodes_and_enemies(index: int, count: int):
    # All four nodes are mutually reachable in open space; placements are spaced
    # away from the spawn and arranged into visible patrol pairs.
    nodes = [(540, 150), (1050, 150), (540, 570), (1050, 570)]
    enemies = []
    walls = [pygame.Rect(w["top_left"], (w["bottom_right"][0] - w["top_left"][0], w["bottom_right"][1] - w["top_left"][1])) for w in interior_walls(index)]
    candidates = [(x, y) for y in (110, 270, 365, 455, 585) for x in (220, 310, 500, 700, 840, 1010, 1130)]
    occupied = [(105, 330)] + missions(index)
    for e in range(count):
        viable = [p for p in candidates if p not in occupied and not any(r.inflate(50, 50).colliderect(pygame.Rect(p, (50, 50))) for r in walls)]
        if not viable:
            raise ValueError(f"No clear enemy placement for campaign map {index}")
        x, y = min(viable, key=lambda p: ((p[0] + 25 - (800 + e*40))**2 + (p[1] + 25 - (350 + (e%2)*120))**2, (p[0] + index*37) % 997))
        occupied.append((x, y))
        kind = "weak" if (e + index) % 3 == 0 else "basic"
        enemies.append((x, y, kind))
    # Tutorial 1 has no enemies but still contains a safe, connected patrol graph.
    return nodes, enemies


def create_map_data(index: int, enemy_count: int, bomb_positions):
    walls = interior_walls(index)
    nodes, enemies = nodes_and_enemies(index, enemy_count)
    # Reproduce ultimate_map_maker.createfile's wall grid and line-of-sight links.
    grid_walls = {(0, 0): walls}
    path_lines = []
    for source in nodes:
        linked = []
        for target_i, target in enumerate(nodes):
            if target == source:
                continue
            if not any(pygame.Rect(w["top_left"], (w["bottom_right"][0] - w["top_left"][0], w["bottom_right"][1] - w["top_left"][1])).clipline(source, target) for w in walls):
                linked.append(target_i)
        path_lines.append(tuple(linked))
    return {
        "walls": grid_walls,
        "path_nodes": nodes,
        "path_lines": path_lines,
        "mission_pointers": missions(index),
        "enemy_data": enemies,
        "player_data": (105, 330),
        "bomb_positions": list(bomb_positions),
    }


def generate_mission_module(name, messages, unlock_checkpoint, music_file):
    lines = ["import pygame", "from Levels import commonfunctions as CFS", "", f"## authored mission script for {name}", ""]
    lines.append(f"bgm = CFS.sound_loader('./sounds/music/{music_file}')")
    for i, message in enumerate(messages):
        lines.extend(["", f"msg{i} = CFS.create_messages(", "    (" + repr(message) + ",)\n)"])
        lines.extend([f"def func{i}(gameObj, levelObj=None):"])
        if i == 0 and unlock_checkpoint == 0:
            lines.append("    levelObj.player.knife_equiped = True")
        if i == 0 and name in ("T01_FirstSteps", "T02_ReadThePatrol"):
            lines.append("    levelObj.player.knife_equiped = False")
        if i == 1:
            lines.append("    gameObj.music_channel.play(bgm, -1)")
        if i == len(messages) - 1:
            lines.append("    gameObj.music_channel.stop()")
        lines.extend(["    CFS.play_sound(gameObj.mission_pass_channel)", f"    return CFS.render_messages, (gameObj.screen, msg{i}), gameObj.fps * 6", ""])
    return "\n".join(lines) + "\n"


def make_bg_tile(name, walls, index):
    texture_name = ("dark.png", "darkest.png", "mid.png", "light.png")[index % 4]
    bg = pygame.image.load(str(MAPS / texture_name)).convert()
    palette = [(58, 69, 78), (63, 58, 72), (54, 75, 70), (78, 66, 57)]
    color = palette[index % len(palette)]
    for wall in walls[(0, 0)]:
        x, y = wall["top_left"]
        w = wall["bottom_right"][0] - x
        h = wall["bottom_right"][1] - y
        pygame.draw.rect(bg, color, (x, y, w, h))
    out = LEVELS_DIR / name / f"{name}-bgpics" / f"{name}-0-0.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(bg, str(out))


def write_level(name, data, messages, unlock_checkpoint, index):
    # Source package mirrors the editor's generated runtime map data exactly.
    source_map = MAPS / f"{name}.map"
    with source_map.open("wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    with (MAPS / f"{name}.mapsupport").open("wb") as f:
        pickle.dump("none.png", f)
        pickle.dump(1, f)
        pickle.dump(1, f)
    dest = LEVELS_DIR / name
    dest.mkdir(parents=True, exist_ok=True)
    with (dest / f"{name}.map").open("wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    make_bg_tile(name, data["walls"], index)
    music = ("bass.wav", "bass1.wav", "bassanddrum.wav", "drums1.wav")[index % 4]
    (LEVELS_DIR / f"{name}.py").write_text(generate_mission_module(name, messages, unlock_checkpoint, music), encoding="utf-8")


def main():
    pygame.init()
    pygame.display.set_mode((CELL_W, CELL_H))
    names = []
    for index, (name, _focus, messages, enemy_count, bombs, unlock) in enumerate(CAMPAIGN):
        data = create_map_data(index, enemy_count, bombs)
        write_level(name, data, messages, unlock, index)
        names.append(name)
    registry = "# Tutorial levels first, followed by 20 main campaign challenges.\n##\n" + "\n".join(names) + "\n"
    (LEVELS_DIR / "Level-Names.txt").write_text(registry, encoding="utf-8")
    (LEVELS_DIR / "__init__.py").write_text("__all__ = " + repr(names) + "\n", encoding="utf-8")
    pygame.quit()
    print(f"Generated {len(names)} levels: 4 tutorials and 20 main levels.")


if __name__ == "__main__":
    main()
