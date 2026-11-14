# INFILTRATION: full technical handoff

This document is the current implementation reference for developers and agents continuing the project.

## Overview

INFILTRATION is a fullscreen top-down Pygame action game. The player moves through tiled worlds, reaches ordered mission markers, gathers charges, plants bombs, escapes their blasts, and uses knives for close-range pressure. The active campaign focuses on trapping basic chasers with bombs and uses weak patrols for local timing and knife decisions.

The codebase uses direct mutable state. `Game`, menu classes, and level objects modify shared fields directly; there is no event bus, ECS, or scene framework.

## Running and dependencies

Run from the repository root:

```powershell
python INFILTRATION.py
```

Python 3 and Pygame are the required dependencies. Relative asset paths mean the process must start at the repository root. Startup initializes Pygame and mixer audio, opens fullscreen hardware/double-buffered display, and loads assets. Map packages and unlock data are pickles, so they must only come from trusted project files. There is no requirements file, packaging metadata, test suite, or CI configuration.

## Repository ownership

| Path | Responsibility |
|---|---|
| `INFILTRATION.py` | Application entry point, outer menu loop, gameplay loop. |
| `game.py` | Shared state, display/audio setup, registry loading, keyboard/mouse/controller input. |
| `menu.py` | Menu widgets, level selector, focused controller navigation, score display. |
| `level_new.py` | Runtime level loader, updates, rendering, bombs, mission triggers, HUD and camera. |
| `player_new.py` | Player rectangle, motion, collision, facing, knife and slash animation. |
| `enemy_new.py` | Basic chaser and weak patrol behavior. |
| `effects.py` | Knife blood, bomb-kill blood, player hurt overlay. |
| `scoring.py` | Result calculation and JSON best-score persistence. |
| `Levels/` | Active levels, scripts, registry, module export list, shared mission helpers. |
| `Levels/legacy-levels/` | Archived inactive levels, scripts, map metadata and references. |
| `maps/` | Current campaign generator, shared generation helpers, editor tools and textures. |
| `images/` | Entity sprites, UI, blasts, slashes and blood art. |
| `sounds/` | Music and audio effects. |

`maps/` intentionally contains no generated `.map` or `.mapsupport` files. Generated runtime maps belong under `Levels/`.

## Application and state flow

`INFILTRATION.py` creates a single `Game` and initial `Main_Menu`. The old intro function exists but is commented out. The outer loop creates a menu object whenever `Game.menumode` changes. New Game or the selector sets `Game.isplaying`; that creates a fresh `Level` unless resuming a paused level.

```text
startup -> outer menu -> select/start level -> Level constructor
        -> gameplay: user_input -> update_world -> render_world
        -> pause / win / game complete / game over -> outer menu
```

The central mutable state includes `isrunning`, `isplaying`, `menumode`, `playing_level_index`, `level_ids`, `level_names`, `INPUTS`, `screen`, `clock`, color palette and mixer channels. The selected display title is separate from the internal module ID used for loading.

## Registry, unlocks and selector

`Levels/Level-Names.txt` holds `internal_id|display title` lines. Comment lines are ignored. `Levels/__init__.py` must export the same IDs in exactly the same order because `level_new.py` imports level modules through `from Levels import *`.

The active roster has 50 entries: Move, Patrol, Knife, Bombs, then 46 campaign missions. `Max-Level-Unlocked` stores a pickled zero-based index. It is currently `49`, so every active level is available for testing. A completed level writes the highest index reached. The selector has nine levels per page in a 3 by 3 grid. D-pad vertical navigation skips empty final-page rows and reaches the Prev Page, Next Page, and Back footer controls.

## Input system

Keyboard/mouse actions: W moves toward the cursor, S moves away, left mouse plants a bomb, right mouse attacks, Space detonates, Escape pauses or goes back, arrows navigate menus, and Enter confirms menu focus.

Controller support is implemented in `game.py`. Pygame joystick discovery runs continuously, so hot-plugging works. The first connected Xbox-compatible controller is used. Left stick moves and faces, A plants, RB attacks, RT detonates, Start pauses, B goes back, and D-pad navigates menus. Inputs are edge-triggered for buttons and D-pad directions. Trigger axes are normalized for common `-1..1` and `0..1` SDL mappings. Controller mode hides the mouse during gameplay.

`trigger_action` and `make_new_node` are still created by input but do not have current gameplay consumers.

## Runtime map package

Every active level package requires:

```text
Levels/<ID>.py
Levels/<ID>/<ID>.map
Levels/<ID>/<ID>-bgpics/<ID>-<grid_x>-<grid_y>.png
```

The map pickle has this schema:

```python
{
    "walls": {(grid_x, grid_y): [{"top_left": (x1, y1), "bottom_right": (x2, y2)}]},
    "path_nodes": [(x, y), ...],
    "path_lines": [(neighbor_index, ...), ...],
    "mission_pointers": [(x, y), ...],
    "enemy_data": [(x, y, "basic" | "weak"), ...],
    "player_data": (x, y),
    "bomb_positions": [(x, y), ...],
}
```

Coordinates are world-space pixels. A cell is 1280 by 720. Actors are 50 by 50 axis-aligned rectangles. The level loader converts wall dictionaries to `pygame.Rect`, then renders the player's surrounding 3 by 3 background-cell window.

## Level creation, update and rendering

`Level(Game, ID)` loads its map, tiled backgrounds, player, enemies, `Bomb`, effects, level module, and per-level starting health. It also reads and updates progression. The camera starts on the player and follows with smoothing.

Every gameplay frame: update time/effects; detect player death; move player; detonate; pick up one overlapping charge; plant; update living enemies; resolve knife attack; remove dead enemies; add player hurt feedback; then test the next mission marker. Enemy health at zero is removed, which fixes bombs failing to kill 50-health patrols.

Rendering draws backgrounds, ground effects, active mission callback, enemies, player, slash, foreground effects, bombs, green marker or mission arrow, health bar, and bomb count. Detonation creates 40 frames of camera shake.

## Player system

`Player` subclasses `pygame.Rect` and also stores floating point position. Movement speed is 500 using the 60 FPS update assumption. Default health is 130 but each level script can override it. Wall collisions are axis-aligned with a 10-pixel tolerance.

For keyboard/mouse, facing and velocity derive from cursor direction relative to rendered player position. Controller movement supplies both facing and velocity. Player sprites rotate from an immutable base surface; the last valid facing direction is retained while still.

Knife range is the player rectangle inflated by 20 percent per dimension. A slash damages each overlapping target by 10. The slash animation lasts 240 ms across nine frames, and early slash frames block another attack to avoid accidental per-frame damage.

## Enemy system

| Type | Health | Movement | Attack |
|---|---:|---|---|
| `basic` | 30 | Graph patrol at 300; direct chase at 450 | Starts 20 chase frames inside 400 distance; attacks within 100 |
| `weak` | 50 | Two-node, wall-colliding patrol | No chase; attacks within 100 |

Both classes inherit Player. A basic enemy starts from its nearest patrol node and randomly chooses valid graph links. Runtime filters malformed, self, duplicate, and links shorter than 72 pixels. Node pairs closer than 72 can make an enemy repeatedly flip direction. Basic chase movement does not perform wall blocking, so chasers can cross walls. A successful melee rectangle overlap deals one player health and starts an enemy cooldown.

## Bombs and effects

Pickups are map points. Player contact removes one pickup and increments inventory. Planting consumes one charge and creates a 300 by 300 world rectangle centered on the player; its red outline lasts 60 frames. Detonation triggers every planted bomb at once.

Every overlapping target loses 50 health per bomb. The affected targets include the player. Walls do not block blasts and there is no falloff. Basic chasers and weak patrols both die from one direct blast. The explosion uses 24 frames. A bomb kill adds blood oriented radially from the closest detonating bomb and fades over ten seconds. Knife hits use 12 short blood frames. Player damage draws a short red overlay.

## Mission triggers and scripts

`Trigger_event` consumes `mission_pointers` in order. When the player rectangle contains the current pointer, it invokes `func0`, `func1`, and so on in the level's module. Each function returns a callback, callback parameters, and duration in frames. It may also enable or disable the knife and control music. Reaching the final pointer records a score and switches to win or game-complete state.

`Levels/commonfunctions.py` creates and renders text surfaces, loads sounds, and plays the checkpoint sound. Current campaign scripts show one short opener at their first marker; later checkpoint text is deliberately blank. Tutorials retain essential control prompts. Do not add text that explains visible routes, pickups, blast range, or tactical solutions.

## Scores and persistence

`scoring.py` writes `Level-High-Scores.json`. It records elapsed time, basic kills (`ghosts_killed`), patrol kills, starting health, health remaining and score. Score equals `1000 + max(0, 3600 - seconds * 8) + basic_kills * 450 + patrol_kills * 200 + health_remaining * 25`. A record is replaced only when a score is strictly higher. JSON saves through a temporary file followed by replace.

## Active campaign pipeline

The current source of truth is `maps/organic_campaign.py`.

- `DESIGNS` contains `(ID, title, motif, (columns, rows), checkpoint_count)`.
- `MISSION_TUNING` contains `(bombs, basic_chasers, weak_patrols, health, knife, waves)`.
- `layout()` builds seams and motif-specific wall geometry.
- `markers_for()` builds ordered routes and supports return-leg missions.
- `build()` places patrols, separate basic-chaser waves, patrol graph pairs and charge pickups.
- `validate()` uses a sampled player-sized flood fill and rejects broken spawns, markers, pickups, patrol links and enemy placements.

The campaign varies one to three charges, two to seven chasers, zero to three weak patrols, 70 to 110 health, optional knife use, and one to three waves. Wave placement is spread over route sectors so a single perfect blast is not intended to clear a whole mission.

Regenerate from the repository root:

```powershell
python maps/organic_campaign.py
```

This regenerates the 46 campaign packages, scripts, background tiles, registry, and module export list. It retains the four tutorial packages. It calls `write_level(..., write_source=False)`, so it does not repopulate `maps/` with `.map` or `.mapsupport` files.

`maps/ai_agent_map_maker.py` provides shared walls, grid bucketing, package writing, tile rendering, and script generation. Its standalone legacy main still writes source maps by default. `maps/ultimate_map_maker.py` is an older interactive editor and can rewrite the registry in an old format, so do not use it for the active campaign without reviewing the output.

## Content rules and cleanup policy

Keep spawn, markers, enemies, path nodes and pickups outside walls. Keep a player-sized path from spawn to every ordered pointer. Every patrol needs valid graph links. Put charges before intended trap opportunities. Vary supply, health, route topology, timing, patrol pressure and enemy mixes rather than scaling only by enemy count. Play changed levels through the normal selector because static validation does not prove fairness or fun.

The root of `Levels/` contains only active packages and scripts plus `__init__.py`, `commonfunctions.py`, registry, score data and campaign documents. Retired material belongs in `Levels/legacy-levels/`. Keep generated map sources out of `maps/` unless a level is actively being edited manually; archives are under `Levels/legacy-levels/maps/`.

## Known limitations

- Relative paths make alternate working directories unreliable.
- Map and progress pickles are trusted local data only.
- Bomb blasts ignore walls and have no distance falloff.
- Collision is rectangle-based; no circle-collision implementation exists.
- Most movement and timing assume the 60 FPS loop instead of complete delta-time simulation.
- Generator flood-fill validation is a safety net, not a playtest.
- There is no automated test suite; use generation validation and real playthroughs.

## Audio, visual assets and UI

`Game` reserves mixer channels: channel 0 for music, 1 for UI, 2 for mission/checkpoint sounds, and 3 for player attack effects. Level modules load one music track through `Levels/commonfunctions.py`; generated event functions start it at the second pointer and stop it at the final pointer. Menu hover and click sounds are owned by `menu.py`. Bomb, pickup, planting, player knife, and enemy knife sounds are created by their owning runtime objects.

Important image conventions:

| Asset area | Runtime owner | Notes |
|---|---|---|
| `images/player.png` | `Player` | Base player sprite, rotated while drawing. |
| `images/enemyb.png`, `images/enemyw.png` | Enemy classes | Basic and weak base sprites, rotated by inherited draw logic. |
| `images/arrow_blue.png` | `Level` | Off-screen objective direction arrow, separate from player facing. |
| `images/bomb1.png`, `images/bomb2.png` | `Bomb` | Planted and pickup/inventory art. |
| `images/blasts/blast0.png` … `blast23.png` | `Bomb` | Ordered explosion animation. |
| `images/slices/slice0.png` … `slice8.png` | `Player` / `Level` | Loaded once per level for the directional slash. |
| `images/blood_slash/` | `Effects` | 12-frame knife-hit blood. |
| `images/blood.png` | `Effects` | Bomb-kill blood, rotated outward from source bomb. |
| `maps/dark*.png`, `mid.png`, `light*.png` | Campaign generator | Tile texture sources. |

The in-game HUD has a green health bar, a bomb count, a green current marker, and the off-screen objective arrow. The arrow only appears when the current marker is off-screen. Camera movement changes all world-space rendering positions; the HUD remains screen-space.

## Menu implementation details

Menu buttons have rendered normal and highlighted images, a hit rectangle, a callback, and callback parameters. Mouse hover updates button state and cursor. Controller or keyboard navigation switches to focused state and uses `navigation_grid` rather than mouse position.

`Level_Selector_Menu.PAGE_SIZE` is nine. It builds the button list from the registry at construction and recreates that list after page navigation. The final navigation row has three footer controls. `Main_Menu._move_selection()` searches vertically through blank cells until it finds an actionable grid position; this is required for the partial last page.

Win and game-over menus present actions through the same button callbacks. The completion UI reads the score result left by `Level.finish_level()` and displays current run plus saved best run.

## Mission event module format

An active level script should follow this pattern:

```python
from Levels import commonfunctions as CFS

starting_health = 90
bgm = CFS.sound_loader('./sounds/music/all.wav')

msg0 = CFS.create_messages(('Short opening line.',))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = False
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 9
```

Use `levelObj.player.knife_equiped` only for level-level weapon availability. Do not rename `funcN`, change the module filename independently of the ID, or change pointer count without matching functions. The current generated functions for blank checkpoints still play the checkpoint sound and run a harmless empty-text callback.

## Map generation internals

`ai_agent_map_maker.py` supplies constants `CELL_W = 1280`, `CELL_H = 720`, `BORDER = 15`, and `MIN_PATROL_NODE_DISTANCE = 72`. `outer_walls()` surrounds a world. `grid_wall_map()` duplicates walls into padded local cell buckets so collision has access near seams. `export_backgrounds()` paints wall rectangles onto the chosen floor texture and writes tiles to the level package.

`write_level(spec, data, index, write_source=True)` writes the runtime pickle, tiles, and Python event module. Its `write_source` parameter controls whether it also writes editable source map files under `maps/`. The organic campaign always passes `write_source=False`. A legacy standalone generator may still use the default and repopulate `maps/`; clean those source files only after confirming they are not an active manual edit.

The organic validator samples the map every 20 pixels using a 50 by 50 player rectangle, flood-fills from player spawn, and checks every pointer and pickup. A nearby inaccessible marker or pickup may be moved to a reachable point within 220 pixels; that adjustment is printed during generation. Review each printed adjustment because it can change the intended encounter location.

For each chaser wave, the generator creates a nearby two-node graph segment even though chasers are designed to pursue the player. This is necessary because `Enemy_Basic` initializes its patrol state from the graph before chase logic runs.

## Active campaign structure

The active campaign registry starts with these tutorials:

| Order | ID | Purpose |
|---:|---|---|
| 1 | `Move` | Mouse/stick movement and ordered markers. |
| 2 | `Patrol` | Read a looping patrol. |
| 3 | `Knife` | Basic close-range attack use. |
| 4 | `Bombs` | Pickup, planting, and detonation controls. |

The remaining 46 levels are defined in `DESIGNS`, in exact gameplay order. Avoid changing only `MISSION_TUNING` if the intended novelty requires a different map topology; use a distinct layout motif or route shape as well. Return-leg IDs are listed in `RETURN_LEG_IDS`; their final marker intentionally revisits a prior sector.

The campaign’s health range is deliberate. Lower health in later missions changes the cost of absorbing mistakes, while scarce-charge missions require route and knife choices. Bomb-rich missions should use multiple separated waves, so the player has more than one tactical decision.

## Manual-editor boundary

`maps/ultimate_map_maker.py` supports manual creation with W/A/S/D pan, Tab then Space constrained walls, Ctrl-drag free walls, Shift snapping, Alt nodes, M markers, B basic enemy, E weak enemy, Enter player spawn, 0 bomb pickup, 1 delete, and Escape package generation.

It is a legacy/manual workflow. It may create source maps under `maps/` and can rewrite `Levels/Level-Names.txt` using an older one-field format. Before using it on active content, back up or inspect the registry, then restore `internal_id|title` format and regenerate `Levels/__init__.py` if needed. The interactive editor does not run the organic generator's flood-fill validator.

## Change recipes

### Add a campaign mission

1. Add a unique ID/title/motif/size/checkpoint entry to `DESIGNS`.
2. Add matching tuning to `MISSION_TUNING`.
3. Add a motif in `layout()` if the existing motifs cannot express the intended decision.
4. Run `python maps/organic_campaign.py` from the root.
5. Confirm generator output has no rejected placement and that the registry has the new ID and title.
6. Play the mission from the normal selector and inspect wave order, bomb supply, and recovery space.

### Change a level's difficulty

Change only the relevant `MISSION_TUNING` fields first. `bombs` changes resource count; `basic_chasers` changes total threat; `weak_patrols` adds path-bound pressure; `health` changes error tolerance; `knife` enables close combat; `waves` determines how many sectors receive chaser groups. Regenerate, then play the result. Change geometry only when the player decision itself needs to change.

### Change gameplay rules

Update the owning runtime file and all affected systems. For example, changing bomb size or damage affects `Bomb`, map encounter tuning, generator comments, campaign design documentation, and playtesting. Changing collision affects Player, Enemy, Bomb, Trigger_event, and validation assumptions. Keep map schema stable unless loader and generators are migrated together.

## Troubleshooting

| Symptom | First checks |
|---|---|
| Level does not appear | Verify `Level-Names.txt`, `__init__.py`, `<ID>.py`, and package folder all use the same ID. |
| Level crashes on load | Verify runtime map path, every background tile, and map dictionary keys. |
| Enemy stops or flickers | Check node links, node spacing of at least 72, and wall-free segment between nodes. |
| Enemy spawns in wall | Regenerate; inspect wall geometry and `open_actor()` placement. |
| Checkpoint cannot complete | Inspect marker reachability, map pointer order, and matching `funcN`. |
| Selector unlocks wrong content | Inspect the pickled integer in `Max-Level-Unlocked` and registry ordering. |
| Controller input does not respond | Check Pygame joystick count, controller mode, and `DEFAULT_BINDINGS`. |
| `maps/` fills with sources | Identify whether a legacy tool called `write_level()` without `write_source=False`. |

## Verification after changes

Run campaign generation after campaign edits. Confirm it reports 50 active levels and no validation errors. Confirm `maps/` has no generated map source files after organic generation. Then launch the game from the repository root, open the selector, load affected levels, verify completion, pause, retry, bombs, knife, patrol/chaser behavior, and selector page navigation.
