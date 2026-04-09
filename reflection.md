# Reflection: Comparing User Profile Outputs

This file compares pairs of user profiles side by side and explains what changed between them and why it makes sense.

---

## Pair 1: Normal Profile vs. Adversarial #1 (The Impossible Combo)

**Normal:** lofi, chill, energy 0.4, likes_acoustic
**Adversarial #1:** lofi, chill, energy 0.9, likes_acoustic: False

The only thing that changed was the energy target (0.4 → 0.9) and acoustic preference. You might expect that raising energy to 0.9 would push high-energy rock or electronic songs to the top. It did not. The same lofi songs — Library Rain and Midnight Coding — still came in first and second. That is because the system gives a huge bonus just for matching the genre label "lofi" and the mood label "chill." Those two bonuses add up to +5.0 points, which is so large that even a terrible energy match cannot cancel them out. Storm Runner, a rock song with energy 0.91 (almost exactly what the user asked for), ended up in last place at 0.99 points — while Midnight Coding, with energy 0.42, scored 5.52. This is like a music store employee recommending the same calm lofi playlist to someone who just said they want something to pump them up at the gym, simply because the person also mentioned they usually listen to lofi.

---

## Pair 2: Adversarial #2 (Ghost Genre) vs. Adversarial #3 (Missing Mood)

**Adversarial #2:** metal, intense, energy 0.95 — genre does not exist in catalog
**Adversarial #3:** pop, sad, energy 0.7 — mood does not exist in catalog

Both profiles lose one of their two major bonuses because a value is missing from the catalog. But the results feel very different. In the Ghost Genre run, only two songs match the "intense" mood, so they score ~2.97 while everything else sits below 1.0 — a huge gap. The ranking is functional but almost empty at the top. In the Missing Mood run, the two pop songs score ~3.8 and dominate everything else, because the +3.0 genre bonus alone is enough to create a clear leader. Everything below them scores under 1.0.

What this reveals: genre and mood are not equally powerful. Losing genre is more painful than losing mood because +3.0 is larger than +2.0. But more importantly, when genre is missing, the system has almost nothing useful to say — it is essentially guessing. When mood is missing, the genre label still provides a clear winner, even if it is not the right one. In both cases, the system never tells the user that it could not find a good match — it just quietly returns whatever is closest.

---

## Pair 3: Adversarial #4 (Acoustic Trap) vs. Normal Profile

**Normal:** ambient, chill, energy 0.4, likes_acoustic
**Adversarial #4:** ambient, chill, energy 0.9, likes_acoustic

Same genre and mood, same acoustic preference — only the energy target changed from 0.4 to 0.9. You would expect high-energy songs to climb. Instead, Spacewalk Thoughts (energy 0.28) won with a score of 6.30 because it matched genre, mood, and had acousticness 0.92. Its energy is 0.28 — the opposite of what the user asked for (0.9). The acoustic bonus rewarded it so generously that the energy mismatch was invisible. Think of it this way: the system is like a friend who knows you love acoustic coffee shop music. When you say "I want something high-energy today," they still hand you a quiet acoustic playlist because in their mind, acoustic always wins. The `likes_acoustic` flag adds points but never subtracts them, so it always pulls recommendations toward quiet songs, no matter what the energy target says.

---

## Pair 4: Adversarial #5 (Neutral Energy) vs. Adversarial #6 (Blank Slate)

**Adversarial #5:** synthwave, moody, energy 0.5
**Adversarial #6:** jazz, melancholic, energy 0.5

Both profiles set energy to 0.5, so every song gets at least a partial energy score regardless of its actual tempo or intensity. The difference is in how many other signals fire. In the Neutral Energy run, there is one synthwave song and several moody songs in the catalog, so Night Drive Loop hits genre, mood, and energy — landing at 5.75, far ahead of everyone else. The ranking has a clear winner. In the Blank Slate run, "melancholic" does not exist as a mood in the catalog, so the mood bonus never fires for anyone. The two jazz songs still dominate (scores ~3.85) purely on the genre bonus, but songs ranked #3 through #5 score between 0.90 and 0.95 — separated by fractions of a point. Their order is essentially arbitrary, like ranking people by height when they are all the same height. The system looks confident but is really just guessing for the bottom of the list.

---

## Pair 5: Experiment A (Weight Shift) vs. Experiment B (Feature Removal)

**Experiment A:** lofi, chill, energy 0.4, likes_acoustic — genre weight halved (1.5), energy weight doubled (2.0)
**Experiment B:** lofi, chill, energy 0.4, likes_acoustic — mood removed (weight 0.0)

These two experiments test the same baseline profile but pull it in different directions. Halving the genre weight (A) made the rankings more competitive — Spacewalk Thoughts climbed to #3 even without a genre match, because energy and acousticness now carried more weight. Coffee Shop Stories appeared in the top 5 for the first time. The system became less tunnel-visioned about genre. Removing mood (B) reshuffled the lofi songs internally — Focus Flow jumped from #4 to #2 because it has a perfect energy match, and Midnight Coding dropped to #3 because the mood bonus that used to inflate its score was gone. Two jazz songs entered the top 5, which never happens in the normal run. What this comparison shows: the genre bonus is the wall that keeps other songs out. The mood bonus is the tiebreaker inside that wall. Changing genre weight opens the door; removing mood changes who sits at the best table inside.

---

## Why Does "Gym Hero" Keep Showing Up for Happy Pop Fans?

Gym Hero is a pop song tagged as "intense" with energy 0.93. When a user asks for pop and happy, the system gives +3.0 for genre (pop matches) but 0 for mood (happy ≠ intense). Yet Gym Hero still ranks #2 in the Missing Mood experiment because the genre bonus carries it almost all the way. The gap between Gym Hero (3.77) and Urban Daydream (0.98) is enormous — not because Gym Hero is a better fit, but because it shares the "pop" label. The system does not understand that "happy" and "intense" are different feelings. It just counts how many labels match. A human recommender would notice immediately that a gym anthem is not the right vibe for someone who asked for happy, feel-good pop. The algorithm cannot make that distinction because it has no sense of what the words actually mean — it only knows whether they are the same string or not.
