# INFILTRATION: 50-level campaign

The active roster contains **50 playable levels**: four focused tutorials,
followed by 46 campaign missions. The registry order is the game order.
Historical level files remain in the project as reference material; only the
IDs listed in `Level-Names.txt` are playable from the selector.

## Tutorials

| # | Level | Lesson |
|---:|---|---|
| 1 | Move | Aim and move relative to the cursor or left stick; follow ordered markers. |
| 2 | Patrol | Read a fixed patrol route and cross after it turns. |
| 3 | Knife | Learn the short attack range and time attacks against a patrol. |
| 4 | Bombs | Collect, plant, retreat beyond the blast radius, and detonate. |

## Main campaign

| # | Mission | Main play idea |
|---:|---|---|
| 1 | Saltwind Causeway | Offset crossings around one turning patrol. |
| 2 | Twin Switches | Choose between braided freight lanes. |
| 3 | Sluice Gate | Bend around a channel while a chaser closes. |
| 4 | Ash Court | Use staggered pockets to choose an approach. |
| 5 | Underpass Relay | Change routes while a wall-crossing chaser follows. |
| 6 | Floodplain Loop | Read two loops and take a guarded return. |
| 7 | Blind Turn | Anticipate a crossing hidden by a dogleg. |
| 8 | Paper District | Navigate a figure-eight route and its return leg. |
| 9 | Night Docks | Choose a lane around islands and a patrol. |
| 10 | Narrow Gauge | Compare a close knife route with a wider bypass. |
| 11 | Split Signal | Collect one charge and retreat before detonation. |
| 12 | Parcel Run | Avoid the false doorway and circle the sorting racks. |
| 13 | Fort Bracket | Choose when to fight at a guarded junction. |
| 14 | Freight Return | Turn back at the far gate and reuse earlier doors. |
| 15 | Pier Blackout | Cross loading bays with a chaser and little waiting space. |
| 16 | Cold Store | Read winding aisles and avoid a misleading dead end. |
| 17 | Watchhouse Gauntlet | Time overlapping patrols across a long route. |
| 18 | Narrow Works | Manage two pinches with a recovery court between them. |
| 19 | Glass Yard | Separate two threats around three island lanes. |
| 20 | Long Night | Follow a long hooked route with limited recovery. |
| 21 | Last Train | Recognize the false finish and use a charge safely. |
| 22 | Sawtooth Mile | Change lanes through alternating wall openings. |
| 23 | Pump Station | Reconnect through channels below a guarded room. |
| 24 | Freight Braid | Avoid a junction where patrol routes converge. |
| 25 | Three Courtyards | Weigh a close knife route against a longer outer route. |
| 26 | False Shortcut | Reject a near doorway that loops into a watched pocket. |
| 27 | Dispatch Loop | Re-enter a shared doorway from the other side. |
| 28 | Cargo Maze | Orient through obscured openings across six sectors. |
| 29 | Split Basin | Trade a longer lower loop for room to recover. |
| 30 | Blind Relay | Keep moving through chained blind turns. |
| 31 | Foundry Spiral | Stay on the broad outer turn through a winding aisle. |
| 32 | North Crossing | Time offset patrol windows across connected courts. |
| 33 | Broken Yard | Choose between an exposed cut and a broader loop. |
| 34 | Long Return | Remember the first junction on a folded route. |
| 35 | Two Charges | Place two pickups before separate crowded approaches. |
| 36 | Breach Yard | Combine close knife combat with a charge and incoming chasers. |
| 37 | Redoubt | Separate guards at a three-way fort approach. |
| 38 | Crosswind | Read offset patrols across intersecting lanes. |
| 39 | Silent Pier | Switch sides at a ramp without stopping in the center. |
| 40 | Dead Angle | Draw a chaser away from a dangerous blind junction. |
| 41 | Pressure Valve | Use a charge at a compressed crossing, then retreat. |
| 42 | Ghost Line | Change direction and recover from wall-crossing chasers. |
| 43 | No Safe Center | Circle the exposed central island and commit on a patrol turn. |
| 44 | Final Window | Combine repeated patrol crossings with an optional charge. |
| 45 | Last Platform | Combine route timing, close combat, and an open final crossing. |
| 46 | Extraction Route | Synthesize long return lanes, overlapping threats, and two charges. |

## Progression and production

- The four opening missions teach movement, patrol timing, knife range, and
  bomb safety before those demands appear together.
- Campaign encounters vary from one to three waves, with one to three charges
  and two to seven chasers. Some missions reward a single large catch; others
  spread smaller groups along the route so one well-timed blast cannot empty
  the rest of the level.
- Bomb supplies vary by mission. Scarce-charge maps mix in patrols or longer
  routes, while bomb-rich maps ask the player to manage several separate
  encounters. Selected levels enable the knife for short patrol fights.
- Checkpoint text is limited to one brief radio line at the first marker.
  Later checkpoints stay quiet so players can read the space and discover
  pickups, timing, and routes themselves.
- Campaign starting health now ranges from 70 to 110. Bombs still kill a
  chaser in one hit; a 50-damage blast also kills a 50-health patrol at zero
  health after the runtime death-threshold fix.
- Layouts use varied 1–3 by 1–2 cell spaces, ordered markers, 50-pixel actor
  rectangles, and the existing wall, patrol, knife, and bomb rules. There is no
  stealth vision or wall-based bomb protection.
- `maps/organic_campaign.py` is the source for all 46 main-campaign maps and
  checkpoint scripts. Run `python maps/organic_campaign.py` from the project
  root to regenerate their packages and the 50-entry registry.
- `Max-Level-Unlocked` is currently set to 49 so the full 50-level roster is
  available for the next playthrough.
- Generation checks the player-sized reachable space, checkpoint access,
  enemy placement, and patrol-pair distance/line of sight. Reported checkpoint
  nudges are small adjustments away from nearby wall edges. These checks do
  not replace a full human playthrough; no complete 50-level playthrough was
  performed during this authoring pass.
