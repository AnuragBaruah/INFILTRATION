# Playtesting and Evaluation Method

Use this when a playable level exists. This method combines professional blockout iteration practice with game user research (GUR) studies. It is intentionally lightweight for a small Pygame project; don't collect data that cannot inform a decision.

## 1. Write a testable question

Turn design intent into a question that could be answered by observing play:

- Can new players identify the first checkpoint goal without verbal help?
- Do players notice the alternate route before committing to the exposed crossing?
- Does the bomb pickup placement teach that the blast can also hurt the player?
- Does this encounter create a meaningful choice about approach, knife, or bomb?
- Can players recover from the patrol mistake and understand what happened?

Record the expected behavior and a signal of a problem before observing testers. Keep the level's intended difficulty separate from clarity problems.

## 2. Use the right method for the question

| Method | Best for | Limitation |
| --- | --- | --- |
| Uncoached observation | Discovering confusion, unexpected routes, timing, whether cues are seen | Observer interpretation can be biased; record concrete events rather than conclusions |
| Short interview | Why player chose an action, what they thought rules/goals were, fairness/readability | Recall is imperfect; ask neutral questions immediately after the relevant beat |
| Gameplay metrics | Route, timing, deaths, damage, retries, pickup/weapon use, checkpoint order | Numbers show what happened, not why; instrumentation has cost and can mislead |
| Screen recording | Revisit route/cues and annotate exact moments | Review takes time; privacy/consent and storage should be handled appropriately |
| Agent/simulation | Reachability, connectivity, obvious softlocks, broad route coverage | Agents embody assumptions and do not represent human perception or fun |
| Biometrics/psychophysiology | Research-grade arousal/response question with appropriate setup | Expensive, intrusive, noisy; not a default for small-team iteration |

A study comparing interviews, metrics, and psychophysiology for 2D platform levels reported interviews gave the clearest indications for improvement, while the other channels provided different information. The result is limited to that project/sample, but supports starting with observation and brief interviews, adding telemetry when a concrete question needs it. See source #53 in [references.md](references.md).

## 3. Prepare the run

- Generate the current source map and launch the game from repository root through the normal menu/selector.
- Confirm the run starts from the intended state and that recording/notes do not obscure play.
- Select a player unfamiliar with this level; note their familiarity with the game controls separately.
- Give only the normal game instructions. Don't teach the intended path or explain hidden design rationale.
- Ask the player to say what they are thinking only if this doesn't interfere with play; unobtrusive observation is often better for action.
- Prepare a top-down map with beat locations labeled A, B, C. Do not annotate the intended solution in the player's view.

## 4. What to record

At each key beat record timestamp/location and observable event:

- First movement, first objective-directed movement, and time to first checkpoint.
- Path taken, decision points, optional route use, backtracking, boundary collision, stuck time, accidental pointer activation, or objective bypass.
- Whether threat/pickup/exit was seen before encounter; player action and any delay before action.
- Knife/bomb use (or non-use), inventory change, damage taken, bomb self-damage, enemy attack, death/retry, checkpoint message display.
- Whether the player's observed route/action differs from intent; don't classify a harmless detour as a failure without learning what motivated it.
- End result: completion, location of failure, duration, most/least memorable beat, player confidence and fairness judgment.

Do not overread single-session timings. Use several runs or repeated observations before changing a level for a pattern, while fixing clear critical blockers immediately.

## 5. Ask neutral questions

After the run:

1. “What did you think the goal was?”
2. “What made you choose that route/action at [location]?”
3. “What did you think the enemy/bomb/wall would do?”
4. “Was there a moment you felt stuck, surprised, or unfairly hit? What happened just before it?”
5. “What would you try on another attempt?”
6. “Which part felt most tense/interesting, and which felt least engaging?”

Ask what they noticed before suggesting an interpretation. Avoid leading prompts (“Did you see the shortcut?”) and don't defend a design decision during the debrief.

## 6. Diagnose and iterate

Translate notes into a location-specific mismatch:

| Observation | Candidate cause to investigate | Possible response to test |
| --- | --- | --- |
| Player doesn't know next task | Goal cue/mission order/text not salient | Improve spatial framing, pointer visibility, short timely text |
| Player sees goal but cannot infer route | Route graph, opening contrast, blocking wall | Reshape connection, reveal route, add distinctive landmark |
| Player enters threat before noticing it | Threat preview, camera/composition, enemy color/position | Add approach space/sight opening, shift enemy or checkpoint |
| Player takes damage with no clear cause | Collision or AI behavior opaque, no recovery/time | Inspect code/physics first, improve telegraph/spacing, tune pressure |
| Player uses only one safe tactic | Encounter over-rewards doorway/one option | Adjust geometry, resources, enemy approach, or objective placement |
| Player ignores pickup | Pickup not visible, not worth detour, or no later use | Reposition or clarify affordance; validate resource relevance |
| Player stalls in an empty stretch | Distance doesn't support a choice, reveal, or tension | Shorten route or give space a purpose |
| Player is overwhelmed throughout | Too many novel demands, no recovery, unclear feedback | Remove/sequence demands, create breathing space, reinforce rule |
| Player completes with no decisions | Layout/encounters too flat or bypassable | Add meaningful tradeoff or use of trained mechanic, not just more enemies |

These are hypotheses, not automatic fixes. Check play recording/source code and ask what the player believed. Change the smallest relevant set of design variables; regenerate source maps after geometry changes and replay. Then check that the revision did not break another route, pointer, patrol graph, bomb escape, or aesthetic cue.

## 7. Separate kinds of success

- **Technical validity:** loads, traverses, and completes; mission and patrol systems don't error.
- **Comprehension:** player understands immediate goal, affordances, and why events happen.
- **Challenge:** player must make meaningful decisions and can learn from failure.
- **Engagement:** player wants to continue, experiment, or master the space.
- **Expression:** theme/narrative/visuals support the intended emotion without reducing readability.

Passing one dimension doesn't prove the others. Capture the evidence and remaining uncertainty in the level handoff.
