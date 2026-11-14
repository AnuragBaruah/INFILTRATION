# Level Authoring Runbook

Use this runbook to create a playable level with the checked-in map editor. Run the editor from the `maps` directory because its paths are relative to that directory:

```powershell
cd maps
python ultimate_map_maker.py
```

## 1. Plan the level

Pick one gameplay idea before opening the editor: route choice, patrol avoidance, knife combat, bomb use, or an escape through a hostile space. Write down the player spawn, the intended route, where difficulty rises, and the final checkpoint.

Each world grid cell is 1280×720. Start with one to three cells. Use more cells only when the route needs meaningful travel or a larger combat space.

## 2. Prepare source assets

Place the tracing/reference image and floor texture in `maps/`. Use a reference image that matches the chosen column and row count when scaled to `columns × 1280` by `rows × 720`.

The editor creates these source assets:

```text
maps/<LevelName>.map
maps/<LevelName>.mapsupport
```

Keep them after generation. They are the editable source of the level.

## 3. Create or edit the source map

At startup, press Enter to create a new map, then provide the level name, rows, columns, and reference image filename. Enter an existing map name to edit it.

Editor controls:

| Control | Action |
| --- | --- |
| W/A/S/D | Pan the editor camera |
| Tab, then Space | Start and commit a constrained wall |
| Hold Left Ctrl | Draw a free rectangle wall |
| Hold Left Shift | Snap the editor marker to 80 pixels |
| Left Alt | Add patrol node |
| M | Add ordered mission pointer |
| B | Add basic enemy |
| E | Add weak enemy |
| Enter | Add the player spawn, once |
| 0 | Add bomb pickup |
| 1 | Delete the hovered object |
| Escape | Finish editing and generate the level |

The editor automatically creates outer boundary walls. Add interior walls to shape paths, cover, and chokepoints. Avoid placing the player, enemies, nodes, pickups, or pointers inside wall rectangles.

## 4. Make enemy patrols valid

The editor creates path links automatically between nodes that have line of sight. Every node used by an enemy needs at least one clear connection to another node; an isolated nearest node can cause runtime errors when the enemy selects a patrol destination.

Place nodes along enemy routes, keeping them clear of walls. After adding walls or nodes, check that each enemy has a reachable pair of nodes in its intended patrol area.

## 5. Build the mission route

Mission pointers are activated in placement order. Put the first pointer close enough to the player to communicate the initial goal, then use each later pointer to mark progression through the level.

Do not place a pointer inside a wall, directly underneath a hostile spawn, or where the player must take unavoidable damage to reach it. The final pointer triggers the win flow.

Bomb pickups are collected automatically when the player overlaps them. If bombs are required, place the pickup before the required detonation space and give the player room to leave the blast area.

## 6. Generate the runtime package

After pressing Escape, answer the prompts for the floor texture and wall RGB colour. The editor generates:

```text
Levels/<LevelName>/<LevelName>.map
Levels/<LevelName>/<LevelName>-bgpics/<LevelName>-<gridX>-<gridY>.png
Levels/<LevelName>.py
Levels/Level-Names.txt
Levels/__init__.py
```

Do not manually substitute a source map for the copied runtime map. Regenerate after source-map edits so both match.

## 7. Customize missions

Open `Levels/<LevelName>.py` after generation. Replace each generated message with text that explains the current objective, threat, or mechanic. Preserve the exported function names (`func0`, `func1`, and so on), because the runtime binds pointers to those names in order.

## 8. Playtest and iterate

Launch the game from the repository root. Verify that the new level appears in the level selector, starts, and reaches its final mission pointer.

After every map geometry change, regenerate the runtime package and replay the level. Use the checklist in `.codex/level-design-checklist.md` before marking the level complete.
