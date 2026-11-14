# Applied Design Method for INFILTRATION

This is a working synthesis of the sources annotated in [references.md](references.md). Every principle is a design hypothesis to test against the implemented game. The strongest direct evidence base here is still modest: several empirical papers study platformers or 3D navigation, while professional talks document experience rather than controlled experiments.

## A. The design problem is a player experience, not a map shape

Use the short design contract below before opening the editor:

| Prompt | What to decide |
| --- | --- |
| Player promise | What should this level let the player do or feel that is memorable? |
| Player verb | What concrete action/decision carries the experience? |
| Existing mechanic | Which implemented rule makes that verb possible? |
| Learning/mastery | What should a newcomer learn or a returning player demonstrate? |
| Stakes | What is gained/lost, and what makes the choice legible? |
| Evidence | What could be seen in a first-time playtest that would confirm the intent? |
| Boundaries | Required pointers, spawn, length, assets, gameplay scope, schema/pipeline constraints? |

Differentiate **mechanics**, **dynamics**, and **experience**: the mechanic is a rule/action; dynamics are the play patterns that emerge when rules interact; experience is the player's interpretation and feeling. A bomb is only a mechanic. A bomb pickup before a patrol crossing, where planting exposes the player to a blast that harms the player and ignores walls, creates a specific decision/risk. Decide if that risk is actually intended and communicated before using it as design material.

Keep the core loop visible in the brief: orient → choose a route/action → move/fight/use resource → receive feedback → progress/adjust. If the level introduces a mechanic, make sure there is enough space/time for its affordance and feedback to be recognized before it becomes a high-cost test.

## B. Variety from a small ruleset

Simple games can produce depth through interaction rather than feature count. For the current game, candidate design dimensions include:

- **Space:** open vs constrained, direct vs bent approach, long sightline vs broken composition, room vs transition.
- **Threat relation:** enemy alone vs overlapping routes, at objective vs guarding access, player chooses encounter order vs encounters are forced.
- **Movement choice:** enter/retreat, approach from sides, circle around wall geometry, separate or draw enemies (only if behavior permits).
- **Resource choice:** save/plant bomb, but account for self-damage and wall-agnostic blast behavior; automatic pickup means placement is also a route decision.
- **Objective structure:** checkpoint location/order, short detour, return leg, clear endpoint.
- **Rhythm:** low-pressure read, commitment, resolution, recovery, next pressure.

Vary one main dimension at a time while teaching; later combine familiar dimensions to create mastery. Changing only texture/color does not create gameplay variety. Conversely, a new feature is not automatically useful: it adds code, UI, edge cases, and another rule to teach.

## C. Campaign and within-level progression

### Teaching and mastery

Use a flexible learning arc: **introduce a rule with low penalty → let players practice it → vary its spatial context → combine it with a known demand → offer resolution**. The sequence can recur at different scales; don't turn it into five mandatory rooms. Give the player a “concentrated sample” of a mechanic (several clear examples) if later levels will require mastery. Avoid dumping every control/rule into the opening tutorial.

For a campaign map, track for each level: primary verb/lesson, supporting mechanics, dominant space pattern, pressure type, resource use, expected duration, novelty vs repetition, checkpoint/exit rhythm, and what it prepares next. This helps distinguish authored levels without demanding a new gimmick in each. Since the project task mentions 20–30 non-tutorial levels, build a campaign progression matrix before map-by-map implementation; do not assume all current/planned mechanics will be present.

### Challenge and relief

Plan a contour with relative intensity and novelty rather than a numeric “difficulty score.” Change intensity through number and direction of threats, exposure, route complexity, commitment/recovery, or resource constraints. Reserve simple beats between demanding ones. A capstone should combine the level's trained idea; an unrelated surprise tests memory of a new rule rather than mastery.

Research on reward/difficulty sequence argues that adaptation and memory can make a simple crescendo or U-shaped curve suboptimal. That's a useful warning, not a formula: the model's assumptions may not fit a fast action map. State a proposed contour, then compare it with observed play (hesitation, repeated damage, rapid completion, fatigue, disengagement). Avoid tuning to the designer's practiced speed alone.

## D. Composition, topology, and guidance

### The map as a choice graph

Draw a graph before drawing detailed walls: nodes represent meaningful spaces (spawn, decision point, encounter, pickup, checkpoint, exit); edges represent traversable connections. Annotate each route with time/exposure/threat/resource payoff. Remove branches that don't make players decide, discover, or change their route. Ordered pointers constrain objective order, but players can still choose paths between them; ensure any optional route joins back cleanly and isn't accidentally a dead end.

Within spaces, use walls to make openings, loops, pinch points, protected pauses, and cross-approaches with a purpose. A wall should influence movement, composition, enemy flow, or silhouette; otherwise ask whether it is clutter. Since bombs ignore walls in the current runtime, never use walls to imply blast-safe cover. Since documented NPCs lack a vision-cone stealth system, occlusion can shape anticipation and visual composition but cannot promise undetected movement.

### Guide without stealing agency

People choose routes based partly on environmental information they can currently see; a navigation study of a 3D adventure space found structural composition patterns influenced movement, and landmark research links informative landmarks with route learning. Transfer carefully to a fixed top-down camera:

1. Reveal the next important opening/goal or a clue to it.
2. Make safe, traversable, threatening, and interactive elements visually distinguishable.
3. Place a recognizable landmark at a decision/transition when useful; distinguish repeated locations rather than decorating them identically.
4. Align wall edges, floor bands, color/value contrast, object placement, and objective indicators so they support the same route hypothesis.
5. Let optional exploration remain possible unless the objective order or stakes require a gate.

Guidance can be layered: world composition first, consistent markers/text second, stronger explicit prompts only where first-time evidence shows they are needed. Multiple cues can compete; more arrows/audio isn't always clearer. The objective arrow already exists, so compose the map to support it instead of adding a second dominant competing cue.

### Positive and negative space

Empty space is content when it gives a player time to read, reorient, retreat, move freely, or feel exposed. It is wasted when it only adds travel. Tight space can create pressure or a decision but can remove maneuverability. Decide which is intended and check actual entity sizes, movement speed, camera bounds, and blast radius. Avoid designing from nominal pixel measures alone; walk the space in the running game.

## E. Encounter design for a top-down action map

Before adding an enemy, write an encounter card:

```text
Intent / intended emotion:
Player entry and visible information:
Threats, spawn points, patrol nodes and route:
Objective / pickup / exit relation:
Player options and their tradeoffs:
Likely failure and recovery:
How the encounter resolves:
What playtest observation would show it works:
```

Useful encounter functions can include a low-pressure introduction, a cross-lane timing decision, a choice of route/order, a resource-use opportunity, a recovery beat, or a synthesis/capstone. These are functions, not a mandatory taxonomy.

Use an encounter diagram to check:

- Entry/exit is not accidentally sealed unless a deliberate lock-in is tested.
- The player can perceive the focal threat before collision/combat becomes unavoidable.
- Enemy spawn and patrol-node graph support the behavior actually implemented; nodes are outside walls and have valid connections.
- The walkable space offers required maneuvering and bomb escape.
- Objective approach does not put the pointer directly under a hostile or cause unavoidable damage.
- Challenge is caused by an understandable decision and rules, not a collision edge case or AI bug.
- The space has an intended use; the player doesn't solve everything from one doorway or ignore most of the layout.

The player should have a legible response, but not necessarily multiple equally safe answers. A constrained route can be compelling if its commitment is communicated, the rule is consistent, and failure remains intelligible. “Fair” does not mean harmless; it means players can form a reliable expectation from cues and prior learning.

## F. Visual identity, feedback, and game feel

Treat rendering and sound as part of rule communication. A useful game-feel survey vocabulary separates **tuning** (physicality, cohesion, predictability), **amplification** (making a meaningful event legible/impactful), and **support** (helping the player's intent execute). Apply it to the action loop: intent → input → game response → perceptible feedback → revised intent. Player movement, enemy facing/telegraph, knife hit, bomb pickup/plant/detonation, checkpoint progress, health loss, and level completion should each have distinct timely cues if the game supports them. A cue must correspond to actual state; contradictory polish damages trust. Before adding shake/blood/flash, check the functional cue first: can the player identify what happened and make the next action?

“Juice” is not a universal good. Screen shake, color flash, blood, sound, and animation can increase impact but also obscure whether damage occurred, where an enemy is, or which checkpoint is active. Preserve visual hierarchy: player > current threat/interaction > goal > scenery. Keep repeated wall/floor semantics consistent. Add art only after blockout decisions work; do a fresh clarity pass after final assets because decorative contrast and silhouettes can change affordances.

## G. Narrative and environmental story

Tie story to what the player does and sees. Make a room's props, barriers, routes, condition, and checkpoint text reinforce the objective or reveal stakes. Avoid putting lore where the player is simultaneously managing immediate danger unless the intended choice is to ignore it. Use mission text for concise, timely orientation and tone; each function maps to the ordered pointer index, so verify module names and progression. A short, coherent story beat is stronger than decorative exposition that doesn't affect experience.

## H. Technical production in this repository

Respect the editor/runtime boundary in [project-context.md](project-context.md). All geometry/objects must be valid after generation; map sketch is not enough. Re-run generation after source changes; don't edit generated assets as the source of truth. Validate route reachability and enemy path graph in each grid cell. Check seams, boundaries, and grid transitions across 1280×720 cells. Use current Pygame coordinate semantics: integer Rect right/bottom edges are exclusive. Current game notes indicate rectangle collision; don't plan circular contact zones until that work is verified in source.

## I. Evidence-based iteration loop

1. State intent and success evidence.
2. Draft route graph and encounter cards.
3. Graybox the smallest version that can test the decision.
4. Generate and launch through the normal flow.
5. Observe uncoached first-time play; take timestamped location/action notes.
6. Ask neutral post-run questions; combine with a few simple counts/timing if useful.
7. Find the mismatch between intent and observed behavior; revise geometry/teaching/feedback.
8. Retest; once stable, art and polish; retest visual hierarchy.
9. Run full completion and regression checks from the project checklist.

Use failures as diagnostic evidence: repeated hesitation at an unseen branch suggests guidance/composition; repeated damage before a reaction suggests threat preview/space/timing; repeated bombs from doorway suggest low-risk dominant strategy; bypassed pickup suggests poor placement/incentive; rapid clear with no decisions suggests flat topology or noninteractive clutter. These diagnoses are hypotheses—confirm by asking players and inspecting gameplay.

## J. Templates

### Beat sheet

| Beat | Player intent | What is visible/known | Choice or skill | Pressure | Feedback/recovery | Exit condition |
| --- | --- | --- | --- | --- | --- | --- |
| Orientation | | | | | | |
| Introduction | | | | | | |
| Variation | | | | | | |
| Combination | | | | | | |
| Capstone/resolution | | | | | | |

### Campaign matrix

| Level | Core lesson/verb | Familiar mechanic | New combination | Space/topology | Pressure/recovery | Expected player evidence |
| --- | --- | --- | --- | --- | --- | --- |

### Decision log

| Decision | Intended player effect | Evidence/source | Implementation dependency | Playtest result / change |
| --- | --- | --- | --- | --- |

Use templates to expose missing thinking, not to enforce a fixed structure on every level.
