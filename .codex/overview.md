# INFILTRATION — Technical Overview

## Purpose and scope

INFILTRATION is a fullscreen, top-down Pygame game. The player moves through a tiled world, reaches ordered mission checkpoints, fights or avoids patrolling enemies, collects and plants bombs, and progresses through a fixed sequence of levels. This document describes the implemented architecture and the current level-authoring workflow so that a later agent can work effectively without rereading every source file.

This document is descriptive, not a proposed redesign. Behaviors below are based on the checked-in code and deserialized map data.

## Repository layout

| Path | Responsibility |
| --- | --- |
| `INFILTRATION.py` | Application entry point, intro sequence, outer menu loop, inner gameplay loop, and post-level menu selection. |
| `game.py` | Shared mutable `Game` state; Pygame/display/audio initialization; game-wide input snapshot. |
| `menu.py` | Mouse-driven menu widgets and all menu screens. |
| `level_new.py` | Runtime level loader, update/render coordinator, mission-trigger system, bomb system, camera, HUD, and screen shake. |
| `player_new.py` | Player state, input-driven movement, wall collision, sprite rendering, and knife attack. |
| `enemy_new.py` | Basic and weak enemy types, patrol/chase behavior, and enemy melee damage. |
| `Levels/` | Playable level definitions: generated map package, background tiles, and per-level mission Python. |
| `maps/` | Active authoring workflow: map editor, source maps, support metadata, reference images, and older map experiments. |
| `images/` | Runtime sprites, UI assets, explosion frames, slice frames, and blood assets. |
| `sounds/` | Music and sound effects. |
| `Max-Level-Unlocked` | Pickled persistent level-unlock index. |

## Dependencies and runtime assumptions

- Python 3 and `pygame` are the only documented runtime requirements.
- There is no `requirements.txt`, packaging metadata, test suite, or CI configuration.
- The project relies on relative paths and therefore expects the process working directory to be the repository root when the game runs.
- The game opens a fullscreen display and initializes Pygame audio during construction/import paths.
- Current source uses `pickle` for map and progression persistence. Map files are trusted project assets, not an interchange format for untrusted files.

## Runtime architecture

```text
INFILTRATION.py
  ├─ Game (game.py): display, clock, inputs, audio channels, progress, state flags
  ├─ Menu classes (menu.py): menu-state rendering and mouse button actions
  └─ Level (level_new.py): one instance per gameplay session
       ├─ Player (player_new.py)
       ├─ Enemy_Basic / Enemy_Weak (enemy_new.py)
       ├─ Bomb (level_new.py)
       └─ Trigger_event (level_new.py)
            └─ generated/manual level module in Levels/<LevelName>.py
```

`Game` is the central shared state object. Menus and levels mutate its `isrunning`, `isplaying`, `menumode`, `playing_level_index`, `INPUTS`, display surface, clock, colors, and mixer channels directly. There is no event bus or separate model layer.

## Entry point and state flow

`INFILTRATION.py` constructs `Game` and `Main_Menu`, plays the opening sequence immediately, then enters `main()`.

```text
startup
  → intro animation
  → outer menu loop
       → New Game / Level Selector sets Game.isplaying
       → create Level(Game, selected level name)
       → inner gameplay loop
            Game.user_input()
            Level.update_world()
            Level.render_world()
       → pause / win / gamecomplete / gameover menu
       → outer menu loop
```

The selected level name comes from `Levels/Level-Names.txt`; comment-prefixed lines are ignored. `Levels/__init__.py` exports the same level module names through `__all__`, which allows `level_new.py` to use `from Levels import *`.

### Main loop details

- The outer loop renders one menu object per frame.
- On entry to gameplay, a fresh `Level` object is constructed unless resuming from pause. This recreates level state for a replay/retry.
- The inner loop calls `Game.user_input()`, then updates and renders the current level at the configured 60 FPS.
- `menumode` determines which menu object replaces the current menu after gameplay ends.

## `Game` responsibilities (`game.py`)

`Game.__init__`:

- Calls `pygame.init()` and `pygame.mixer.init()`.
- Opens a fullscreen hardware/double-buffered display.
- Creates the 60 FPS clock and shared palette.
- Reserves mixer channels: music (0), UI (1), mission/checkpoint (2), player attack (3; currently not used by the player attack implementation).
- Loads ordered level names.
- Ensures `Max-Level-Unlocked` exists, initially serializing integer `0` if it does not.

`Game.user_input()` collects input each gameplay frame. It resets one-frame actions and then populates `INPUTS`:

| Input | Current resulting state |
| --- | --- |
| `W` / `S` held | `movement` is `+1` / `-1`; direction itself comes from the mouse. |
| Mouse position | `mouse_pos`. |
| `E` | `trigger_action=True`; no gameplay consumer was identified. |
| Left mouse down | `plant_bomb=True`. |
| Right mouse down | `knife=True`. |
| Space | `detonate=True`. |
| Tab | `make_new_node=True`; no gameplay consumer was identified. |
| Escape | exits gameplay into pause mode. |
| Quit event | stops both gameplay and the application. |

The current input model is therefore mouse-directed forward/back movement, not conventional WASD movement.

## Menus (`menu.py`)

Menu behavior is mouse-only today.

- `Menu_Button` stores rendered normal/hover text, bounds, callback, and callback parameters.
- `Locked_Button` is non-actionable and changes sound/appearance while hovered.
- `Main_Menu` provides New Game, Level Selector, and Exit.
- `Pause_Menu`, `Win_Menu`, `Game_Complete_Menu`, `Game_Over_Menu`, and `Level_Selector_Menu` specialize the background and buttons.
- The level selector reads `Max-Level-Unlocked`; levels at or below the stored index are actionable.
- Button callbacks directly mutate `Game` fields.

## Level runtime (`level_new.py`)

### Loading

`Level(Game, level_name)` reads:

```text
Levels/<level_name>/<level_name>.map
```

It loads map data, creates background-tile surfaces, converts serialized wall dictionaries to `pygame.Rect` objects, instantiates the player, creates enemies from spawn data, constructs the bomb manager, and advances persistent unlock progress.

The camera starts centered on the player and then follows with linear smoothing. Rendering draws a 3×3 neighborhood of background grid tiles around the player’s current world grid.

### Update order

Each gameplay frame currently proceeds in this order:

1. End game if player health is below zero.
2. Determine the player’s grid from its top-left position.
3. Update player direction from mouse input, calculate velocity, check current-grid walls, and advance player position.
4. Detonate bombs when requested.
5. Pick up bombs that overlap the player.
6. Plant a bomb when requested and inventory is positive.
7. For each living enemy: update alert state, velocity, and position; remove enemies whose health is below zero.
8. Resolve player knife action when requested.
9. Check whether the player reached the next mission pointer.

### Rendering order

1. Smooth camera position and optionally apply random screen shake.
2. Draw nearby static background tiles.
3. Run any active mission message callback for its remaining frame count.
4. Draw enemies, player, bombs, mission direction arrow/checkpoint, health, and bomb inventory.

## Player (`player_new.py`)

`Player` subclasses `pygame.Rect` and keeps a parallel floating-point `position` vector.

| Property | Current value/behavior |
| --- | --- |
| Shape | 50×50 axis-aligned rectangle. |
| Speed | 500 units/second. |
| Health | 130 maximum and initial health. |
| Facing/movement | Mouse direction from the player’s screen-space render position; `W` moves toward it and `S` away from it. |
| Collision | Axis-aligned rectangle checks against walls in the active grid cell, with 10-pixel tolerance. |
| Knife | Inflates player rect by 100 pixels each direction, damages only the first colliding enemy by 10, and plays swing/hit SFX. |

The player is rendered as a static image without rotation. The current render position is important: `direction_update()` derives its mouse vector from this position.

## Enemies (`enemy_new.py`)

Both enemy types inherit `Player`, so they also inherit rectangle collision fields, `position_update`, draw logic (with replaced sprite), and health.

### `Enemy_Basic`

- Initial health: 30.
- Patrol speed: 300; chase speed: 450.
- Loads the level map again to access `path_nodes` and `path_lines`.
- Selects its nearest path node, then randomly chooses a linked node.
- Patrols graph edges.
- Starts/refreshes a 20-frame chase period when the player is within 400 world pixels.
- During chase, moves directly toward the player and attacks when within 100 pixels.
- A successful rectangle-overlap melee attack deals 1 health and enters a temporary satisfied period.

### `Enemy_Weak`

- Initial health: 50.
- Converts its patrol graph to the two initially chosen nodes, effectively patrolling one segment.
- Continuously points toward the player but follows its simple patrol path.
- Checks walls during its own velocity update and attacks within 100 pixels.

The level-script tutorial text calls these wall-passing enemies “ghosts,” but implementation behavior differs by class and should be verified if this distinction matters to a future task.

## Bombs and explosions (`level_new.py`)

`Bomb` holds:

- `positions`: map-provided collectible pickups.
- `planted`: 300×300 explosion rectangles centered on player position when planted.
- `planted_temp`: temporary outline display for 60 rendered frames.
- `exploded`: active 24-frame explosion animations.

Pickup increments `Player.bomb_equiped`. Planting decrements it. Detonation applies 50 damage to every object whose rectangle overlaps each blast rectangle; that target list includes all enemies and the player. It also plays audio and applies 40 frames of random camera shake. Blast damage does not currently consider walls, distance falloff, or a source bomb vector.

## Missions and level scripts

`Trigger_event` receives an ordered map `mission_pointers` list. It pairs pointer index `i` with dynamically resolved `<LevelName>.func<i>`. When the player rectangle contains the next pointer:

1. The function is called with `(gameObj, levelObj)`.
2. It returns `(callback, parameters, frame_count)`.
3. The callback runs during subsequent render frames.
4. The next pointer/function becomes active.
5. After the final pointer, gameplay enters win mode, or game-complete mode for the final listed level.

Most level functions display messages and play a checkpoint sound. Some also start/stop music or mutate `levelObj.player.knife_equiped`. The generated scripts are templates; existing scripts have been manually customized.

`Levels/commonfunctions.py` provides message-surface construction, message rendering, and checkpoint sound playback.

## Playable map schema

All seven finalized maps currently contain this dictionary:

```python
{
    'walls': dict[tuple[int, int], list[dict]],
    'path_nodes': list[tuple[int, int]],
    'path_lines': list[tuple[int, ...]],
    'mission_pointers': list[tuple[int, int]],
    'enemy_data': list[tuple[int, int, str]],
    'player_data': tuple[int, int],
    'bomb_positions': list[tuple[int, int]],
}
```

`walls` has the shape:

```python
{
    (grid_x, grid_y): [
        {'top_left': (x1, y1), 'bottom_right': (x2, y2)},
        ...
    ]
}
```

The finalized maps and their notable counts are:

| Level | Grid cells | Nodes | Mission pointers | Enemies | Bomb pickups |
| --- | ---: | ---: | ---: | ---: | ---: |
| TheOpening | 4 | 2 | 4 | 1 | 0 |
| ZIGZAG | 6 | 17 | 2 | 32 | 0 |
| GetKnife | 8 | 3 | 4 | 15 | 0 |
| DETONATE | 6 | 4 | 3 | 60 | 3 |
| PRIORITIES | 9 | 30 | 21 | 29 | 21 |
| TheCorners | 9 | 35 | 7 | 23 | 23 |
| DirectionSense | 9 | 34 | 7 | 18 | 17 |

## Active authoring workflow (`maps/`)

`maps/ultimate_map_maker.py` is the active interactive editor and level generator. It is intentionally an executable authoring utility, not runtime code.

### Creating or editing a source map

On startup the tool asks whether to create a new source map or load an existing one.

For a new map it asks for:

- map filename;
- number of grid rows and columns;
- a supporting/reference image for tracing.

It creates initial world-boundary walls and writes a companion `.mapsupport` file. The editor displays the reference image below the editable walls and entities.

Editor controls implemented by the tool:

| Control | Editor action |
| --- | --- |
| `W/A/S/D` | Pan editor camera. |
| `Tab` then `Space` | Start and commit a wall. |
| Hold `Left Ctrl` | Draw unrestricted rectangle instead of constrained horizontal/vertical wall. |
| Hold `Left Shift` | Snap marker to 80-pixel increments. |
| `Left Alt` | Add patrol path node. |
| `M` | Add ordered mission pointer. |
| `B` | Add basic enemy. |
| `E` | Add weak enemy. |
| `Enter` | Place player if none exists. |
| `0` | Add bomb pickup. |
| `1` | Delete hovered wall/node/pointer/enemy/bomb/player. |
| `Escape` | End editing and finalize the source map. |

### `.mapsupport` schema

The companion file is a stream of three sequential pickle values, not a dictionary:

```python
image_filename: str
column_count: int
row_count: int
```

Example: `['detonate.jpg', 2, 1]` indicates a two-column, one-row editing world traced from `detonate.jpg`.

This data is only used by the authoring tool to restore the reference image and canvas dimensions. The runtime game does not read `.mapsupport` files.

### Finalizing source maps

`createfile()` performs the content-processing step:

1. Finds grid extents from wall geometry.
2. Creates grid-cell wall buckets.
3. Inserts each wall into each padded cell it overlaps, so edge collisions are available in either neighboring cell.
4. Generates path graph adjacency by connecting each node pair whose straight line does not intersect any wall.
5. Pickles the complete gameplay map dictionary.

### Generating a playable level package

After editing ends, `make_level()`:

1. Loads the source map.
2. Prompts for a floor texture and wall RGB color.
3. Creates `Levels/<Name>/<Name>-bgpics/`.
4. Renders one 1280×720 tile per map grid cell with floor texture and visible wall geometry.
5. Saves the tiles as `<Name>-<grid_x>-<grid_y>.png`.
6. Copies the source map to `Levels/<Name>/<Name>.map`.
7. Generates `Levels/<Name>.py`, containing one default `funcN` message function per mission pointer.
8. Appends the level name to `Levels/Level-Names.txt` if absent.
9. Rewrites `Levels/__init__.py` with the complete exported level list.

```text
maps/<Name>.map + maps/<Name>.mapsupport + reference image
    → editor/finalizer
    → Levels/<Name>/<Name>.map
    → Levels/<Name>/<Name>-bgpics/<Name>-X-Y.png
    → Levels/<Name>.py
    → level registry updates
```

The `maps/` source map and the copied `Levels/` map can diverge after generation; the runtime uses the `Levels/` copy.

## Other map utilities

- `maps/create_map_based_bg.py` is an earlier/background-only generator. It reads a map, asks for a floor image, and writes per-grid images, but does not produce the full level package or script.
- `maps/make_the_map.py` creates walls from `Default Dataset.csv` coordinate pairs.
- `maps/map_maker_ab.py` and `maps/map_maker_ag.py` are older/manual map-generation approaches.
- Numerous other maps, support files, images, spreadsheets, and text files in `maps/` are prototypes or source assets. Their schemas are not uniformly current: several lack player, enemy, mission, or bomb fields expected by current runtime levels.

## Visual/audio asset inventory relevant to runtime work

- `images/player.png`, `images/enemyb.png`, `images/enemyw.png`: current entity sprites.
- `images/arrow_blue.png`: existing mission direction arrow, not a player-facing arrow.
- `images/slices/slice0.png` through `slice8.png`: nine provided knife-slice frames.
- `images/blood.png`: provided bomb-kill blood-splash asset.
- `images/blood_slash/blood_slash0.png` through `blood_slash11.png`: twelve additional blood-slash frames present in the repository; no current runtime code uses them.
- `images/blasts/blast0.png` through `blast23.png`: 24 explosion frames already used by `Bomb`.
- `sounds/SFX/`: knife, enemy-knife, bomb, pickup, checkpoint, hover, click, and planting audio.
- `sounds/music/`: intro and level music tracks.

## Constraints and risks for future work

- Input is spread between menu polling and `Game.user_input()`. Controller support must address both paths, including mouse cursor visibility/capture and menu navigation.
- Movement and facing are coupled to mouse-derived direction; controller movement requires an explicit facing/movement-vector model rather than merely translating key events.
- Player/enemies inherit `pygame.Rect`, and attacks/bombs use rectangle APIs (`colliderect`, `collidepoint`, `collidelistall`). Circular hitboxes require a compatible collision abstraction or targeted replacement at every interaction point.
- Runtime map data currently has no entity radius, animation, controller mapping, visual-effects, or blood-effect fields. Those should remain runtime defaults/configuration unless authoring requirements change.
- Level script binding uses `eval`, and level registration is generated through `__all__`; refactors should preserve or deliberately replace this contract.
- The map maker writes files and invokes shell directory creation. It must not be imported casually by runtime code.
- Relative paths are pervasive. Any restructuring must account for runtime and editor working-directory assumptions.
