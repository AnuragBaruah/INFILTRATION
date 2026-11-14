# INFILTRATION level-authoring handoff

**Snapshot date:** 2026-11-14  
**Purpose:** Technical reference for an agent continuing level work. Covers
runtime contracts, map data, authoring tools, packaging, validation, and the
history of level sets. It is not a design brief.

## Source-of-truth notes

- Current playable registry: Levels/Level-Names.txt, paired with
  Levels/__init__.py. Campaign details: Levels/Campaign-Design.md.
- Current campaign authoring source: maps/organic_campaign.py. Run from the
  repository root with: python maps/organic_campaign.py
- maps/campaign_expansion.py is a compatibility launcher for organic_campaign.
- maps/ultimate_map_maker.py is the interactive/manual editor. It is a separate
  workflow and does not run the organic campaign validator.
- .codex/overview.md and .codex/tasks.md describe older snapshots and
  requirements. The overview's “seven finalized maps” table is stale for the
  current 50-level registry. .codex/level-authoring-runbook.md and
  .codex/level-design-checklist.md remain useful for manual-editor work.
- Do not remove historical map folders simply because they are unlisted.
  Existing assets are retained as references unless cleanup is requested.

## Current playable campaign

There are 50 entries: four tutorials and 46 newly generated campaign missions.
Registry order is gameplay order. The previous roster and historical maps stay
on disk as references and are not in the active selector.

The campaign centers on trapping and blasting enemies, but varies the number
of pickups (one to three), chasers (two to seven), and encounter waves (one to
three). Some missions use patrols or knife fights; others spread chaser groups
along the route so a single perfect blast cannot clear the remaining level.
Starting health ranges from 70 to 110. Bombs deal 50 damage; enemies at zero
health are now removed, so a 50-health patrol correctly dies to one blast.
Campaign scripts show one brief opening line; later checkpoints are silent.
The next-test unlock state is `Max-Level-Unlocked = 49` for 50 active levels.

**Tutorials:** Move, Patrol, Knife, Bombs.

**Campaign:** Saltwind Causeway, Twin Switches, Sluice Gate, Ash Court,
Underpass Relay, Floodplain Loop, Blind Turn, Paper District, Night Docks,
Narrow Gauge, Split Signal, Parcel Run, Fort Bracket, Freight Return, Pier
Blackout, Cold Store, Watchhouse Gauntlet, Narrow Works, Glass Yard, Long
Night, Last Train, Sawtooth Mile, Pump Station, Freight Braid, Three
Courtyards, False Shortcut, Dispatch Loop, Cargo Maze, Split Basin, Blind
Relay, Foundry Spiral, North Crossing, Broken Yard, Long Return, Two Charges,
Breach Yard, Redoubt, Crosswind, Silent Pier, Dead Angle, Pressure Valve,
Ghost Line, No Safe Center, Final Window, Last Platform, Extraction Route.

The roster uses internal_id|display title. Legacy one-field lines are accepted
by Game as a backward-compatible fallback. gameObj.level_ids is for loading
modules/maps; gameObj.level_names is for UI labels. Keep order and lengths
identical. Internal IDs must be valid Python module names because level_new
imports Levels and resolves each level's funcN.

## Runtime and map-package contract

### Important files

| File | Level-work responsibility |
| --- | --- |
| INFILTRATION.py | Uses the registry index to load a level and show its display title on clear. |
| game.py | Reads ID/title registry into level_ids and level_names; owns shared state and inputs. |
| level_new.py | Loads maps/backgrounds, creates actors and bombs, advances triggers, renders the world. |
| player_new.py | Player Rect, movement, wall collision, health, knife, sprites. |
| enemy_new.py | Basic chaser and weak patrol movement; patrol-link filtering. |
| Levels/<ID>.py | Checkpoint event functions func0, func1, … and per-level health/music/weapon state. |
| maps/organic_campaign.py | Current campaign data, map construction, checks, packaging, registry generation. |
| maps/ai_agent_map_maker.py | Shared map/package helpers used by the organic generator. |
| maps/ultimate_map_maker.py | Interactive editor and legacy manual packaging workflow. |

The application expects to run with the repository root as the working
directory. It uses relative paths and pickled map data. Only load trusted
project .map files.

### World coordinates

- Each world/background cell is 1280 × 720 pixels.
- Coordinates are global pixels. Cell index is (x // 1280, y // 720).
- Player and enemy Rects are 50 × 50 pixels. Player speed is 500 px/second at
  60 FPS. Collision uses Rect overlap; wall blocking has a 10 px tolerance.
- Outer boundary walls are 15 px thick in the current map helpers.
- Runtime renders nearby background cells around the player. Generate a
  background image for every grid cell, even where adjacent cells look alike.

### Pickled map dictionary

Runtime map path: Levels/<ID>/<ID>.map. It is a pickle of:

~~~python
{
    "walls": {(grid_x, grid_y): [
        {"top_left": (x1, y1), "bottom_right": (x2, y2)},
        ...
    ]},
    "path_nodes": [(x, y), ...],
    "path_lines": [(neighbor_index, ...), ...],
    "mission_pointers": [(x, y), ...],  # ordered trigger points
    "enemy_data": [(x, y, "basic" | "weak"), ...],
    "player_data": (x, y),             # player Rect top-left
    "bomb_positions": [(x, y), ...],   # pickup points
}
~~~

walls[(gx, gy)] is a local collision bucket of world-space wall dictionaries.
Generators duplicate references into padded neighboring cell buckets; keep
coordinates global. Runtime converts each dictionary to
pygame.Rect(x1, y1, x2-x1, y2-y1). Right/bottom bounds are exclusive Pygame
Rect edges.

Normal generated package:

~~~text
maps/<ID>.map
maps/<ID>.mapsupport
Levels/<ID>.py
Levels/<ID>/<ID>.map
Levels/<ID>/<ID>-bgpics/<ID>-<grid_x>-<grid_y>.png
Levels/Level-Names.txt
Levels/__init__.py
~~~

The source map and runtime map are separate copies. Runtime loads only the
Levels/ copy. Regenerate after source geometry changes.

### Checkpoint script contract

level_new.Trigger_event pairs marker i with <ID>.func<i>. When the player Rect
contains the marker point, it calls the function with (gameObj, levelObj).
Return a callback, parameters, and frame duration:

~~~python
return CFS.render_messages, (gameObj.screen, msg_i), gameObj.fps * duration_seconds
~~~

The callback runs during subsequent render frames. The next marker activates
immediately; after the last marker, runtime records a result and opens the
win/completion menu. Functions can update music or
levelObj.player.knife_equiped. Author one specific event message per marker and
keep exactly one funcN per marker.

### Player, threats, and tools

- Keyboard/mouse movement: aim with mouse; hold W toward cursor and S away.
  Controller movement uses movement_vector.
- Player starts with 130 health and knife_equiped=True, but a level script
  often disables the knife at its first trigger. Check func0; the map schema
  does not control weapon availability.
- Knife attacks use a player Rect inflated by 20% of each dimension (10 px
  total added to width and height), hit the first overlapping target, and deal
  10 damage. Weak enemies have 50 HP; basic enemies have 30 HP.
- Enemy_Weak patrols a two-node segment, collides with walls, and attacks
  within 100 px. Enemy_Basic patrols the graph, can chase for 20 frames when
  within 400 px, and is not wall-blocked while chasing. Some level text calls
  basic enemies “ghosts”; “basic” is the runtime type.
- Bomb pickups are collected when the player Rect contains their coordinate.
  Planting creates a 300 × 300 blast Rect centered on the player; detonation
  deals 50 damage per overlapping bomb to enemies and the player. Blast damage
  ignores walls. Leave a retreat lane; don't require self-harm.

## Patrol graph rules and stuck-node defect

Enemy_Basic.reset_nodes() loads path_nodes/path_lines, finds the nearest node,
then chooses a linked node. It changes destination when its Rect contains that
point. Very close nodes can both fall inside the enemy Rect, causing rapid
direction flipping or an apparent stuck patrol.

The shared minimum distance is 72 px:

- enemy_new.MIN_PATROL_NODE_DISTANCE filters malformed/near-duplicate runtime
  links and falls back to another sufficiently distant node.
- maps/ultimate_map_maker.py ignores nodes within min_path_node_distance=72.
- maps/ai_agent_map_maker.py filters graph links shorter than 72 px.
- maps/organic_campaign.py rejects authored patrol pairs under the shared
  helper constant, crossing a wall, or with a spawn Rect intersecting a wall.

For manual graphs, preserve node indices and give each used node at least one
valid neighbor. Use more than 72 px separation (the current organic campaign
uses 270 px endpoints). Put route points inside the same traversable corridor
as their patrol. A line crossing a wall is invalid even if both endpoints are
clear. Weak patrols use the two nodes chosen at construction as their own pair.

## Current organic generator

From the repository root, run:

~~~powershell
python maps/organic_campaign.py
~~~

This regenerates 46 authored map packages and per-level Python event scripts,
then writes the 50-entry Levels/Level-Names.txt and Levels/__init__.py. The
four tutorial packages remain in place. It also writes source .map/.mapsupport
files in maps/. DESIGNS entries contain:

~~~text
(internal ID, display title, layout motif, (columns, rows), checkpoint count)
~~~

MISSION_TUNING holds each mission's bomb supply, chaser count, patrol count,
starting health, knife access, and wave count. Add a motif key in layout() for
a new layout kind. build() spreads chaser packs across ordered checkpoint
sectors, adds patrol path pairs, places pickups along the route, and validates
player-sized reachability. Campaign scripts display one short opener; later
checkpoint messages are intentionally blank. The registry is generated in
tutorial then campaign order with display titles from DESIGNS.

world.write_level() writes map data, support data, tile images, and the level
module. The organic generator uses shared ai_agent_map_maker package helpers.

### Generation-time checks and limits

Before writing each map, validate():

1. Builds a 20 px sampled occupancy grid using 50 × 50 player Rects.
2. Flood-fills clear positions from player spawn using four-way adjacency.
3. Checks every checkpoint is overlappable from reachable player space. If
   not, it moves the marker to the closest reachable sampled standing point
   within 220 px and prints the relocation; farther errors stop generation.
4. Checks bomb caches similarly.
5. Rejects patrol endpoint pairs closer than 72 px or crossing walls.
6. Rejects enemy spawn Rects outside the world or intersecting walls.

This is an authoring safety net, not proof of gameplay quality. It samples
coarsely, checks markers independently rather than simulating the ordered path,
and does not replace a playthrough. Review each relocation: a snap may clear a
broken point while moving it from the intended room.

## Manual editor workflow

For hand editing, open PowerShell in maps/ and run:

~~~powershell
python ultimate_map_maker.py
~~~

Reference and floor image paths are relative to maps/. New-map flow asks for
name, columns, rows, and reference image.

| Key | Action |
| --- | --- |
| W/A/S/D | Pan editor camera |
| Tab, then Space | Start and commit constrained wall |
| Hold Left Ctrl | Free rectangle wall |
| Hold Left Shift | Snap cursor to 80 px |
| Left Alt | Add path node |
| M | Add ordered mission pointer |
| B | Add basic enemy |
| E | Add weak enemy |
| Enter | Add player spawn once |
| 0 | Add bomb pickup |
| 1 | Delete hovered object |
| Escape | Finish editing and generate |

.mapsupport is a stream of three pickle values: reference image filename,
columns, rows. ultimate_map_maker.createfile() buckets walls by grid and links
node pairs whose straight segment does not cross walls. make_level() renders
1280 × 720 tiles, copies the map to Levels/, generates the event script, and
rewrites the registry. The old editor writes one-field names; running it can
rewrite or append to the current ID/title registry. Review registry order and
restore the ID/title format before shipping.

## History of level sets

Classify by the user's definitions, not by whether assets remain on disk.

### Hand-made legacy missions

The original manually created set is exactly:

- TheOpening
- ZIGZAG
- TheCorners
- PRIORITIES
- GetKnife
- DirectionSense
- DETONATE

The current campaign retains the four large challenge maps ZIGZAG, TheCorners,
GetKnife, DirectionSense, and DETONATE. TheOpening is omitted because Move
covers the movement tutorial. PRIORITIES stays in the project but is not
active: its recorded map has 21 pointers, 29 enemies, and 21 bomb pickups.
Historic map counts in the older overview (before current edits):

| Level | Cells | Enemies | Pointers | Bombs |
| --- | ---: | ---: | ---: | ---: |
| ZIGZAG | 6 | 32 | 2 | 0 |
| GetKnife | 8 | 15 | 4 | 0 |
| DETONATE | 6 | 60 | 3 | 3 |
| TheCorners | 9 | 23 | 7 | 23 |
| DirectionSense | 9 | 18 | 7 | 17 |
| PRIORITIES | 9 | 29 | 21 | 21 |

These counts are historic, not a guarantee of present map data. Selected legacy
mission scripts were edited for checkpoint text/actions in an earlier pass;
their hand-authored map geometry was retained.

### First AI-generated set

The user classifies all T01_... and L01_... levels as the first AI batch.

Tutorial IDs: T01_FirstSteps, T02_ReadThePatrol, T03_CloseQuarters,
T04_BombSafety.

Challenge IDs: L01_QuietApproach, L02_CoverToCover, L03_TheLongHall,
L04_Crossfire, L05_TheSupplyCache, L06_Switchback, L07_PatrolClock,
L08_ThePillars, L09_CloseQuarters, L10_BlastRadius, L11_ThreeLanes,
L12_TheGauntlet, L13_DeadDrop, L14_RedCorridor, L15_RelayRun,
L16_TheBlindCorner, L17_SilentExit, L18_BreachPoint, L19_LastPatrol,
L20_Extraction.

These remain reference assets and are not in the current playable roster.

### Second AI-generated set

Four tutorial levels from this generation are active: Move, Patrol, Knife,
Bombs. Other named second-generation maps present in the project include:
Ambush, Blackout, Bloodbath, Breach, Courtyard, Crosswind, DeadReckon, Detour,
Finale, Floodgate, Gauntlet, Ghosts, LastPatrol, Lockdown, LongHall, Lost,
Maze, NoWayOut, Pressure, Silent, Slalom, TwinFuses. They are not all active;
the intent is to retain the good tutorials and selectively use prior work,
not preserve the entire challenge roster.

Some IDs were reused by later authoring: current Blackout, Floodgate, and
Glasshouse packages were regenerated by organic_campaign.py. Do not assume
same-name files still contain their original second-gen maps. Older map
directories remain references where they were not overwritten.

### Intermediate campaign attempts

- An early attempt kept too much of the second-generation challenge set. The
  user clarified that the purpose was to create better levels, not to preserve
  and reorder the old batch.
- A later C/R-prefixed attempt contained 17 C## bespoke missions and four R##
  concept remakes, plus tutorials and five legacy maps. Code-like player-facing
  prefixes were unwanted. The user played through C09_BlindRelay and found a
  checkpoint inside a wall. C/R missions are superseded and excluded from the
  active registry; old files may remain on disk.
- The 50-level redesign retained the four tutorials and replaced the main
  campaign with 46 naturally titled authored missions. Generation completed
  authoring-time reachability, enemy-placement, and patrol-link checks. It
  reported small checkpoint nudges away from nearby wall edges. No complete
  human playthrough of the 50 levels was performed in this pass.

## Continuation checklist

1. Read this file, Levels/Campaign-Design.md, and maps/organic_campaign.py.
2. Keep IDs, titles, module exports, folders, module filenames, and registry
   order synchronized.
3. Preserve the seven-key map schema unless deliberately migrating runtime
   loading, enemy logic, and every map generator together.
4. Patrol links must be at least 72 px apart and clear of walls; check both
   nodes and the line. Ensure enemy Rects fit their route.
5. Spawn, every marker, and every cache must fit in player-sized walkable
   space. Every marker must be reachable from spawn.
6. Regenerate from the repository root and review all “moved checkpoint”
   messages and generated assets.
7. Play the level in-game afterward. Static generation does not check timing,
   damage fairness, ordered route completion, or final-segment survivability.
8. Do not run the legacy editor without checking registry output; it may
   rewrite the current ID/title format to one-field entries.
