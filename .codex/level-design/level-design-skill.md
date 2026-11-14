---
name: infiltration-level-design
description: Research, plan, author, critique, and iterate INFILTRATION levels using the implemented Pygame mechanics and map pipeline. Use for mission progression, encounter layouts, player guidance, challenge pacing, and level playtesting.
---

# INFILTRATION Level Design Skill

Use when asked to prepare, design, author, review, or improve levels for this repository. This skill applies industry practice and research to the game's specific mechanics and editor. It does not presume permission to modify runtime code, generate levels, or change campaign scope; follow the user's request.

## Read project reality first

Use `.codex/overview.md`, `.codex/level-authoring-runbook.md`, `.codex/level-design-checklist.md`, and `.codex/tasks.md`, then inspect source files when behavior matters. `tasks.md` records desired/planned features; it is not proof they are implemented. Current notes describe a top-down Pygame action game with movement, knife, auto-pickup/plant/detonate bombs, simple patrol/chase enemies, ordered checkpoint triggers, and wall collision. Verify any presumed stealth, cover, visibility, alarm, branching, resource, or combat rule in code. A path-node line-of-sight link in the editor means graph connectivity; do not mistake it for enemy vision detection.

Important project constraints and hazards are in [project-context.md](project-context.md). Research synthesis and methods are in [design-principles.md](design-principles.md) and [playtest-method.md](playtest-method.md). The [reference library](references.md) annotates professional talks, academic work, practical case studies, and official documentation, including each source's evidential weight and transfer limits.

## Design workflow

### 1. Define the experience and contract

Write a brief design contract before opening the map editor:

- **Player promise:** what should the player get to do/feel/understand?
- **Core verbs:** which existing actions must carry the experience?
- **Learning/mastery objective:** what should players learn or demonstrate?
- **Constraints:** mandatory checkpoints, enemies, bombs, map cells, story/music, implementation scope, and what must remain unchanged.
- **Success evidence:** observable player behavior that would show the intended experience is happening.

Separate design intent from implementation facts. If the desired experience depends on a missing mechanic, report that dependency and offer a concept that works with current mechanics; do not quietly invent the feature in level logic.

### 2. Analyze mechanics and generate a small concept set

Describe the game's core loop in player-action terms and list mechanics with their affordances, costs, failure states, feedback, and interactions. Ask what decisions the current level system actually allows. Propose a few distinct level concepts by varying one or two dimensions (route topology, encounter arrangement, objective sequence, bomb risk, or pressure/recovery), then choose based on the requested campaign role and player promise. Keep scope around a few mechanics used meaningfully; new mechanics add teaching and implementation costs.

### 3. Map beats and routes on paper

Make a beat sheet and a top-down flow sketch before placing coordinates. Mark start, next goal, encounter boundaries, enemy paths, safe/recovery areas, resource placements, branching decisions, and exit. For each beat write player intent, information visible on entry, desired decision, likely failure, recovery/feedback, and exit condition. Establish a readable main route; each branch should offer an intelligible tradeoff or meaningful discovery. Annotate the intended pressure/recovery contour but allow the actual playtest to change it.

### 4. Block out and communicate

Use simple geometry with strong visual categories first. Shape paths and sightlines using the actual top-down view and collision. Make important affordances clear by form, placement, contrast, and consistent visual language. Guide attention with composed view, landmarks, directional structures, and the existing objective cue; put explicit text/UI guidance where it supplies needed information. Readable guidance should preserve choice when possible; avoid hiding necessary rules behind decorative ambiguity. Verify visual guidance still works when viewed at real play scale.

### 5. Tune encounters, difficulty, and pacing

Treat an encounter as the coupled arrangement of player entry/exit, threats, usable space, objectives, resources, response options, and consequences. Ask what the player can know before commitment, how they can respond, what each response costs, and how they recover. Space and timing can create challenge without adding enemies. Teach unfamiliar mechanics in a low-cost context, vary conditions, then combine mastered demands. Avoid escalating only enemy count, health, or traversal length. Use short tension/recovery changes and reserve the capstone for a combination that expresses the level's idea.

Do not assume a universal smooth difficulty curve or one fixed “teach/test” cadence. Sequencing research suggests reward/difficulty adaptation can make a simple crescendo suboptimal; empirical results from another genre are prompts to test, not a prescription. Make the desired progression explicit, then observe real players and revise.

### 6. Preserve technical authoring constraints

Follow [the authoring runbook](../level-authoring-runbook.md). Keep source `.map` and `.mapsupport`; generate runtime packages through the existing editor. Check world/grid coordinates, boundaries, player spawn, each patrol graph, ordered pointer reachability, bomb pickup order and blast escape, level registry/module consistency, and mission text. Current notes: 80-pixel editor snap, 1280×720 background cells, pointer functions bound by index, patrol nodes linked by line of sight, and bomb blasts that currently ignore walls and harm the player. Re-check source before relying on these values after code changes. Use the [project context](project-context.md) for the complete constraint list.

### 7. Test with people and evidence

Use [playtest-method.md](playtest-method.md). Run a clean build of the level, give a first-time player only the information a shipped player receives, and avoid coaching. Observe path choice, hesitation, objective comprehension, enemy contacts, damage/death, bomb use, and recovery. Ask neutral questions after the run. Triangulate interviews with simple event counts or timings when helpful. Prioritize a reproduced player problem over a speculative metric; distinguish usability/comprehension failures from the intended difficulty. Iterate geometry and messaging before expensive art, then re-check clarity after the art pass.

### 8. Review and hand off

Use the project's checklist and state evidence for each acceptance criterion. Separate (a) runtime validity, (b) authored gameplay quality, and (c) narrative/visual polish. A technically completable map can still be monotonous, confusing, unfair, or easily bypassed. Keep the design brief, map sketch, generated output, known constraints, playtest observations, and rationale together so another developer can review the intent.

## Design decision principles

- Design around **player decisions**, not a list of objects to place.
- Treat clarity, agency, challenge, surprise, mood, and narrative as tensions to balance for the stated experience, not maximizable absolutes.
- Prefer the smallest mechanic set that yields the intended variety. Simple systems can support deep play when choices and feedback are strong.
- A level communicates through action affordances, layout, feedback, and aesthetic framing. Decorative “juice” that contradicts material or rules can reduce trust/readability.
- Use measurements and flow charts as lenses to expose assumptions, never as a substitute for player experience.
- Borrow at the level of a design problem (e.g. “make a patrol crossing readable”) rather than copying a genre's solution (e.g. vision cones, cover, alarms) that this game does not support.

## Reference routing

- For level route composition and visual player guidance, read the relevant GDC entries and wayfinding studies in [references.md](references.md), then design principles §3.
- For encounter rhythm and challenge sequencing, use [references.md](references.md) and design principles §4–5; note transfer limits.
- For tutorialization and progression across a campaign, read the GDC teaching talks and sequencing research, then use the brief/beat-sheet template in [design-principles.md](design-principles.md).
- For playtest planning, use [playtest-method.md](playtest-method.md).
- For Pygame implementation details, use official docs listed in [references.md](references.md), then inspect project code; docs do not describe this game's architecture.
