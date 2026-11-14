# INFILTRATION Level Design: Project Context

This note records the project's current constraints from `.codex/overview.md`, `.codex/level-authoring-runbook.md`, `.codex/level-design-checklist.md`, and `.codex/tasks.md`. Re-check source after gameplay code changes.

## Current game loop and mechanics

- Fullscreen top-down Pygame action game. The player traverses tiled maps, activates ordered mission pointers, fights or avoids patrol/chase enemies, collects and plants bombs, then reaches the final pointer to win.
- Bomb pickups are automatic on overlap. Bombs damage entities in their blast rectangles, including the player; current behavior does not account for walls or distance falloff.
- Basic/weak enemies patrol and chase. Patrol routes are formed from visible path-node connections; each enemy needs accessible connected nodes. The current notes do not document a stealth vision cone or cover/hiding system.
- Pointers activate in order and bind by index to `func0`, `func1`, etc. in the generated level module.
- Runtime coordinates are world-space; background cells are 1280×720. Editor grid snapping is 80 px. The editor generates a 1280×720 background image per world grid cell.
- Runtime wall/entity handling currently uses rectangular geometry. Circular collision, controller support, directional art, slash animation, and richer VFX appear as planned tasks in `.codex/tasks.md`; verify what has landed before relying on them.

## Authoring workflow and files

Run the editor from `maps/` with `python ultimate_map_maker.py` because paths are relative. Keep the editable source map and companion support metadata in `maps/`. Generate runtime maps/packages with the editor; do not hand-substitute source data into runtime paths.

Expected generated output:

```text
Levels/<LevelName>/<LevelName>.map
Levels/<LevelName>/<LevelName>-bgpics/<LevelName>-<gridX>-<gridY>.png
Levels/<LevelName>.py
Levels/Level-Names.txt
Levels/__init__.py
```

Editor controls documented in the runbook: W/A/S/D pan; Tab then Space commits constrained wall; Ctrl-drag draws rectangle wall; Shift snaps to 80 px; Alt adds patrol node; M adds mission pointer; B/E adds basic/weak enemy; Enter adds the one player spawn; 0 adds bomb pickup; 1 deletes hovered object; Escape finishes and generates.

## Level-specific hazards

- Every enemy needs at least a pair of connected, visible nodes in its patrol area; isolated nodes can trigger runtime errors.
- Keep the player, enemies, nodes, pickups, and pointers outside wall rectangles.
- Pointers must be reachable and should not require unavoidable damage. Put bomb pickups before intended bomb use and leave room to escape the blast.
- Bomb damage ignores walls in the current implementation; walls shape movement but do not provide blast safety.
- Maps use wall rectangles and grid indices; a sketch is not proof of reachable traversal. Validate boundaries and test generated levels.
- Run the game from repository root because paths are relative.
- Levels are sequenced in `Levels/Level-Names.txt`; generated level scripts and `Levels/__init__.py` must stay in sync through editor generation.

## Verify implementation status

The project overview is descriptive, while `.codex/tasks.md` includes planned work. Before designing around a feature, inspect `level_new.py`, `player_new.py`, `enemy_new.py`, and `game.py` to confirm it exists and understand behavior. Do not turn planned acceptance criteria into current design promises.
