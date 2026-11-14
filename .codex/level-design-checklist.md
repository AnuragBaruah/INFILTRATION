# Level Design Checklist

## Before authoring

- [ ] The level has one clear gameplay purpose.
- [ ] The grid size is proportional to the route; it does not add empty travel.
- [ ] The planned player path has a safe first few seconds.

## Geometry and spawns

- [ ] Boundary walls enclose the full playable area.
- [ ] Interior walls leave a route from the player spawn to every mission pointer.
- [ ] Player spawn is outside walls and away from enemy overlap.
- [ ] Every enemy has at least two visible patrol nodes available in its area.
- [ ] Enemies are positioned to create choices, sightlines, or timing problems.
- [ ] No enemy is trapped by walls or immediately forced into the player.

## Objectives and bombs

- [ ] Mission pointers are ordered to form a readable route.
- [ ] Every pointer can be entered by the player rectangle.
- [ ] Checkpoints do not require unavoidable damage.
- [ ] Bomb pickups appear before any intended bomb use.
- [ ] Detonating a required bomb has a safe player escape route.
- [ ] Mission text explains unfamiliar mechanics before the player needs them.

## Difficulty and pacing

- [ ] The opening teaches the level's main idea with low pressure.
- [ ] Challenge rises through new spatial conditions or combinations, not only more enemies.
- [ ] The route has room for the player to move, retreat, and aim.
- [ ] The final section tests the level's main idea.

## Final playthrough

- [ ] The level appears in the selector and loads without errors.
- [ ] The full route works after launching from the repository root.
- [ ] Every enemy patrols or chases without errors.
- [ ] Knife, bomb pickup, planting, detonation, mission triggers, win, retry, and pause work where used.
- [ ] No normal gameplay modifies source maps, support files, generated level scripts, or background tiles.
