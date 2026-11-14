# INFILTRATION — Planned Improvements

## Scope

Implement the following gameplay and presentation upgrades while preserving the existing playable-level and map-authoring pipeline. The active runtime files are `game.py`, `menu.py`, `level_new.py`, `player_new.py`, and `enemy_new.py`; the map editor remains `maps/ultimate_map_maker.py`.

Do not change generated level-map schema or authoring output unless a task explicitly requires it. Existing levels must continue to load from `Levels/<Name>/<Name>.map`.

## Task 1 — Add Xbox-compatible gamepad input

### Objective

Support a connected Xbox-compatible PC controller in the game application, including Bluetooth-connected devices. Retain keyboard/mouse support when no gamepad is active.

### Requirements

1. Detect and initialize gamepads through Pygame’s joystick/controller facilities.
2. Perform connection discovery while in every menu state, including startup, pause, win, game-over, completion, and level selector.
3. Handle connection and disconnection while the application remains open.
4. Restrict input switching to this game application only. Do not alter system-wide keyboard, mouse, Bluetooth, or controller behavior.
5. When a usable gamepad is connected:
   - game menus accept controller navigation;
   - menu mouse pointing/clicking is disabled for the game window;
   - gameplay keyboard/mouse control is disabled for the game window;
   - mouse cursor is hidden during gameplay;
   - keyboard/mouse functionality returns when no usable gamepad remains connected.
6. Preserve mouse cursor usability in keyboard/mouse menu mode. The user’s intended behavior is: hide/disable it during gameplay, while keeping it available for menus when controller mode is not active.
7. Avoid hard-coding platform-specific device indices. Device selection must survive controller reconnects.

### Default controller layout

Use this as the initial default mapping, with action names independent from device-specific numeric constants:

| Context | Default control | Action |
| --- | --- | --- |
| Gameplay | Left stick | 2D movement and facing direction. |
| Gameplay | Right bumper (RB) | Knife attack. |
| Gameplay | Right trigger (RT) | Detonate planted bombs. |
| Gameplay | One face button (`A` preferred) | Context action / bomb pickup interaction if interaction becomes explicit. |
| Gameplay | Another face button (`X` preferred) | Plant bomb. |
| Gameplay | Menu/Gameplay | Start/Menu | Pause or menu back, subject to final UX design. |
| Menus | D-pad up/down | Change selected menu item. |
| Menus | D-pad left/right | Navigate grids such as Level Selector. |
| Menus | `A` | Activate selected button. |
| Menus | `B` | Back/cancel where a parent menu exists. |

The current runtime automatically collects bombs on collision. Do not claim that a face button performs pickup unless either the pickup mechanic is deliberately changed or the action is explicitly reserved for future interaction.

### Implementation design

1. Centralize raw device polling and connection state in `Game`, not in individual entities or menus.
2. Add a declarative, editable default binding table in `game.py` for all game actions. It must support remapping every action without changing entity/menu code.
3. Translate raw keyboard/mouse and controller events into the same high-level input structure. Suggested action-level state includes:

   ```python
   movement_vector
   facing_vector
   knife_pressed
   plant_bomb_pressed
   detonate_pressed
   pause_pressed
   menu_up_pressed
   menu_down_pressed
   menu_left_pressed
   menu_right_pressed
   menu_confirm_pressed
   menu_back_pressed
   controller_active
   ```

4. Use a controller dead zone and normalize analog-stick magnitude. Determine facing from the left-stick vector while controller mode is active.
5. Handle triggers as axes, not only button events; use a configurable threshold and rising-edge detection so holding RT does not repeatedly detonate every frame.
6. Implement menu focus/selection state rather than attempting to simulate mouse position. Existing menu callbacks may remain reusable.
7. Ensure the outer menu loop processes controller connection events and menu inputs before rendering.
8. Update pause handling to work without an Escape key in controller mode.

### Acceptance criteria

- A connected Xbox-compatible controller can start a game, select a level, pause/resume, retry, advance, and exit entirely through controller input.
- D-pad navigation visibly identifies the current menu item and activation invokes exactly one callback.
- Gameplay responds to left-stick direction without mouse input.
- Controller mode suppresses keyboard/mouse gameplay actions; unplugging the controller restores them in the game application.
- Keyboard/mouse gameplay still works when no controller is connected.
- All bindings are configurable in one clearly named area of `game.py`.

## Task 2 — Decouple movement, facing, and rendering orientation

### Objective

Introduce an explicit entity-facing model that works for both controller and keyboard/mouse play, and rotate the replacement circular player/enemy graphics accordingly.

### Requirements

1. New player and enemy artwork is already in `images/player.png`, `images/enemyb.png`, and `images/enemyw.png`.
2. Artwork convention: a source rotation of 0° faces upward.
3. Rotate each entity sprite toward its current movement/facing direction at render time.
4. Do not mutate or repeatedly rotate an already-rotated image; retain immutable base surfaces and derive rotated render surfaces from them.
5. Maintain a last-valid facing direction while stationary so sprites do not snap or fail when their movement vector is zero.
6. For player controller mode, left-stick direction is both movement and facing.
7. For keyboard/mouse mode, preserve an intentional, documented behavior for movement and facing. The existing forward/back-with-mouse model may be retained initially, but it must produce an explicit facing vector.

### Player facing arrow

Add a small, wide, player-specific directional arrow along the circumference of the player sprite/hitbox.

- It is separate from `images/arrow_blue.png`, which is currently the mission/checkpoint direction indicator.
- Position it on the outer edge of the player circle in the facing direction.
- Rotate it according to facing.
- Render it above the player without affecting collision.
- Either reuse an appropriate existing visual asset intentionally or add a documented runtime-drawn arrow; do not repurpose the mission arrow accidentally.

### Acceptance criteria

- Player and enemy graphics face up at source 0° and rotate correctly for all movement directions.
- Standing still preserves the last facing direction.
- The player-facing arrow remains visibly attached to the player circumference and points in the same direction as the player sprite.
- Mission guidance arrow behavior remains unchanged.

## Task 3 — Replace rectangular entity hitboxes with circular collision

### Objective

Use circular collision for the player and enemies to match the replacement round sprites.

### Requirements

1. Define explicit entity center/radius data for player and enemies.
2. Replace entity-vs-entity rectangle overlap checks with circle-vs-circle tests where appropriate:
   - player knife range/hit selection;
   - enemy attack range;
   - bomb explosion damage;
   - bomb pickup;
   - mission-pointer reach checks where appropriate.
3. Keep wall collision behavior compatible with the rectangular wall data. Implement circle-vs-rectangle wall collision/resolution, rather than reverting entity collision to rectangles.
4. Preserve the existing map coordinate convention: entity positions are world-space and background cells are 1280×720.
5. Avoid breaking sprite drawing, camera following, grid calculation, map loading, or enemy patrol.

### Collision design constraints

- Do not rely on inherited `pygame.Rect.colliderect` for gameplay hit detection once circular hitboxes are introduced.
- A compatibility rectangle may remain for broad-phase/grid selection or legacy positioning, but circle geometry must be authoritative for gameplay collision.
- Establish one shared collision utility module or one clearly owned collision API; do not duplicate distance formulas in player, enemy, bomb, and mission classes.
- Define and test the intended radius values from final sprite dimensions or explicit gameplay constants.

### Acceptance criteria

- Visual overlap and hit detection feel circular for player and enemies.
- Player/enemies cannot pass through walls due to corner artifacts.
- Knife, enemy melee, pickup, bomb damage, and checkpoint triggers use the new geometry consistently.
- Existing levels load with no map-data migration.

## Task 4 — Knife slash animation

### Objective

Play the supplied slash animation when the player performs a knife attack.

### Assets

- Frames: `images/slices/slice0.png` through `images/slices/slice8.png`.
- Existing knife sound effects remain in `sounds/SFX/`.

### Requirements

1. Load slice frames once per level/session, not during every attack frame.
2. Trigger exactly one animation sequence per accepted knife action.
3. Position the animation relative to the player’s circular hitbox and facing direction.
4. Rotate the animation to match player facing, using the source-art orientation that is verified from the supplied frames.
5. Advance animation using elapsed time or clearly defined frame timing, independent of display refresh instability.
6. Allow animation rendering to continue after the one-frame attack input flag resets.
7. Keep damage timing explicitly defined: either apply at attack start or at a documented hit frame; avoid accidental multi-hit damage over the animation’s lifetime.

### Acceptance criteria

- A knife input shows one complete, directionally aligned slash.
- The slash does not persist indefinitely or multiply while a control is held.
- A single slash cannot damage the same target once per rendered frame.

## Task 5 — Blood and combat-feedback effects

### Objective

Add temporary hit feedback for knife attacks, bomb kills, and player damage.

### Knife-hit blood

1. On a successful player knife hit, create small temporary blood drops/effects near the enemy.
2. Prefer the available `images/blood_slash/` frames if their appearance fits the intended small-hit effect; inspect the frames before finalizing the effect rather than assuming their purpose from the folder name.
3. Effects should be short-lived and managed by a dedicated runtime effect system, not embedded permanently into sprites or map tiles.
4. Do not show knife-hit blood when the knife hits no enemy.

### Bomb-kill bloodbath

1. On an enemy death caused by a bomb, display `images/blood.png` as a blood-splash effect.
2. Source-art convention for `blood.png`: 0° is 45° counter-clockwise from the positive X axis.
3. Rotate the splash radially from the nearest detonating bomb to the killed enemy.
4. If multiple bombs affect a killed enemy in one detonation pass, choose the nearest source bomb deterministically.
5. Keep the blood splash active temporarily and fade alpha smoothly to zero in approximately 10 seconds of real elapsed time.
6. Render the effect in world space so camera movement keeps it anchored at the death location.
7. Ensure the effect’s lifetime remains valid after the enemy entity is removed from the active enemy list.

### Player hurt overlay

1. Detect player health reduction, including enemy melee and self-damage from bomb blast.
2. Overlay a translucent red screen flash for approximately one or two rendered frames, or an equivalent very short time-based duration.
3. Do not trigger the flash repeatedly when health is unchanged.
4. Render it after the world and HUD so it affects the whole visible screen.

### Effect-system design

1. Introduce a level-owned transient visual-effect collection with explicit creation, update, render, and expiry behavior.
2. Effects must be safe to add/remove while iterating.
3. Use elapsed time or a consistent game-time abstraction for the 10-second fade requirement.
4. Track combat damage provenance. Existing code only subtracts health directly, so bomb-caused deaths need a source-bomb reference or a structured damage event to determine splash orientation reliably.

### Acceptance criteria

- Knife hits show short-lived blood only on successful hits.
- Bomb-killed enemies create one correctly oriented blood splash, located at the death position, fading out over roughly 10 seconds.
- Non-bomb deaths do not incorrectly create bomb splashes.
- The player receives a brief red damage flash whenever health decreases.
- Effects do not leak memory, remain attached to dead entities, or alter persistent map data.

## Task 6 — Regression and verification

### Required manual checks

1. Start the game without a controller: keyboard/mouse menu and gameplay work.
2. Start the game with a controller: controller menu and gameplay work without mouse navigation.
3. Connect/disconnect a controller from a menu and verify mode changes cleanly.
4. Pause, resume, retry, level-select, win, game-over, and final-game-complete flows work in both input modes.
5. Load all seven shipped levels.
6. Verify player/enemy movement, collision, patrol, chase, knife attacks, bombs, mission triggers, and level completion.
7. Verify graphics at multiple facing angles and while standing still.
8. Verify each effect: miss, knife hit, knife kill, bomb kill, bomb self-damage, and enemy melee damage.
9. Verify that no map file, `.mapsupport` file, generated level script, or generated background tile is modified by normal gameplay.

### Implementation sequencing

1. Central input abstraction and controller lifecycle.
2. Controller menu focus/navigation and input-mode cursor behavior.
3. Explicit movement/facing state and sprite rotation.
4. Shared circular collision primitives and wall resolution.
5. Knife animation and structured combat/damage events.
6. Blood effects and hurt overlay.
7. Regression testing across all shipped levels and input modes.

## Task 7 — Produce playable levels through the existing authoring workflow

### Objective

Create one or more new, polished playable levels using either the existing `maps/ultimate_map_maker.py` workflow, or create your own workflow suitable for ai agent `maps/ai_agent_map_maker.py`. Preserve the current map schema and generated package structure so the runtime can load each level through the normal level selector.

Create a complete set of new levels starting from tutorials to main challenges. The total number of non tutorial levels must be 20 - 30. Do not delete my old levels, just edit the `Levels/Level-Names.txt`, to exclude / include any particular existing level. The order of levels in the file denotes the order of actual levels in the game. Change the level specific python file `Levels/<level-name>.py` in order to have different behaviours / text / music etc. when checkpoints are hit.

### Required artifacts

Use these project guides while authoring:

- `.codex/level-authoring-runbook.md`
- `.codex/level-design-checklist.md`

### Requirements

1. Create and retain the source `.map` and companion `.mapsupport` files in `maps/`.
2. Generate every runtime package through `maps/ultimate_map_maker.py`, producing the copied map, background tiles, mission module, and level registry updates.
3. Give every level one player spawn, at least one ordered mission pointer, bounded walkable space, and patrol nodes that can connect to another node.
4. Use enemy placement, walls, bomb pickups, and mission sequence to teach or test a clear gameplay idea. Do not rely on random enemy placement as the sole source of difficulty.
5. Replace generated mission text with level-specific messages and any intended mission actions.
6. Play through the generated level from a clean launch and correct blockers before considering it complete.

### Acceptance criteria

- The level appears in the level selector and starts without missing files or module errors.
- The player can complete all mission pointers and reach the win flow.
- Enemies patrol without path-node errors, and the player cannot leave the authored play area.
- Bombs, if used, can be obtained and used without making completion impossible.
- The level offers a readable route, a deliberate challenge curve, and no unavoidable damage caused by a spawn or checkpoint placement.
