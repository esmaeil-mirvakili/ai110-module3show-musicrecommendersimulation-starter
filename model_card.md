# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeMatch 1.0**

A simple, transparent music recommender that matches songs to a user's stated taste using a point-based scoring system.

---

## 2. Goal / Task

VibeMatch tries to answer one question: given what a user tells me they like, which songs in the catalog are the closest fit?

It does not learn from listening history. It does not track skips or replays. It takes four preferences — genre, mood, energy level, and whether the user likes acoustic sound — and uses those to score every song in the catalog. The top five scores become the recommendations.

This is for classroom exploration, not for real users. It is designed to make the recommendation process visible and easy to reason about.

---

## 3. Algorithm Summary

Each song gets a numeric score based on how well it matches the user's preferences. The rules are:

- **+3.0 points** if the song's genre matches what the user said they like
- **+2.0 points** if the song's mood matches what the user said they want
- **Up to +1.0 points** based on how close the song's energy is to the user's target — a perfect match gives +1.0, a song at the opposite extreme gives +0.0
- **Up to +1.0 points** from the song's acousticness score, but only if the user said they like acoustic music

After every song in the catalog is scored, they are sorted from highest to lowest. The top five are returned as recommendations, along with the score and a breakdown of what points came from which rule.

The maximum possible score is about 7.0. A song that matches genre, mood, energy perfectly, and is fully acoustic would reach it.

---

## 4. Data Used

The catalog has **18 songs** stored in a CSV file. Each song has 10 fields:

- **Text fields:** title, artist, genre, mood
- **Number fields (0–1 scale):** energy, valence, danceability, acousticness
- **Number fields (other scale):** id, tempo in BPM

**Genres represented:** lofi, pop, rock, ambient, jazz, hip-hop, classical, electronic, synthwave, indie pop, r&b

**Moods represented:** chill, happy, intense, relaxed, focused, moody

**Limits:** The catalog is tiny. Some genres appear only once or twice (classical, synthwave, r&b). Some moods that real users might want — like "sad," "melancholic," or "energetic" — do not exist in the data at all. The dataset was built by hand for this project, so it reflects the choices of one person, not a broad sample of musical taste.

---

## 5. Strengths

The system works best when the user's preferences are well represented in the catalog.

- A user who likes **lofi and chill** gets strong, sensible results. Three lofi songs exist with matching moods, so the scoring has enough material to produce a real ranking.
- The **explanation output** is a strength. Every recommendation shows exactly which rules fired and how many points each contributed. There is no mystery about why a song ranked where it did.
- For **calm, acoustic-leaning profiles**, the acousticness bonus adds useful nuance — it reliably surfaces jazz, classical, and ambient songs that feel right for a quiet-listening context.
- The system **never crashes on bad input**. If a genre or mood does not exist in the catalog, it falls back gracefully to the remaining signals instead of throwing an error.

---

## 6. Limitations and Bias

**Genre dominance creates a filter bubble.** The genre bonus (+3.0) is so large relative to the other signals that the system almost always returns songs from the user's stated genre, regardless of how well those songs fit everything else. In the Impossible Combo test, two lofi songs with energy around 0.4 still ranked first and second even though the user's energy target was 0.9. Storm Runner, whose energy of 0.91 was nearly a perfect match, ranked last because it failed the genre check. A user who says "I like lofi" will only ever see lofi songs, even when their other preferences point toward something completely different. Halving the genre weight in Experiment A was enough to let energy and acousticness meaningfully influence the ranking for the first time, confirming the default weight is the direct cause of this bias.

**The system cannot say "I don't know."** When a user asks for a genre or mood that does not exist in the catalog — like "metal" or "sad" — the system does not flag it. It silently returns whatever scores highest on the remaining signals. The user has no way to tell that their main preference was ignored.

**Acoustic preference only adds, never subtracts.** Setting `likes_acoustic: True` rewards high-acousticness songs with up to +1.0 points. But setting it to `False` gives no penalty to acoustic songs. A user who dislikes acoustic music still gets recommended highly acoustic songs if they match on genre and mood.

**Small catalog, uneven genre coverage.** Classical, r&b, and synthwave each have one or two songs. A user who prefers those genres has almost no good matches available and will get weak recommendations by default.

---

## 7. Evaluation

Nine user profiles were tested in total: one normal baseline, six adversarial edge cases, and two weight experiments. All results are documented in the Adversarial Profiles and Experiments sections of the README.

**Profiles tested:**

- **Normal (lofi/chill/acoustic)** — calm listener baseline, used as the reference for all comparisons
- **The Impossible Combo** — lofi/chill genre but energy target 0.9, designed to pit genre against energy
- **The Ghost Genre** — asked for "metal," which does not exist in the catalog
- **The Missing Mood** — asked for "sad," which no song has
- **The Acoustic Trap** — ambient/chill with energy 0.9 and likes_acoustic, pulling energy and acousticness in opposite directions
- **The Neutral Energy** — energy set to 0.5 to compress the scoring spread across all songs
- **The Blank Slate** — jazz with a missing mood and energy 0.5, most signals silent
- **Experiment A** — same baseline with genre weight halved and energy weight doubled
- **Experiment B** — same baseline with mood completely removed

**What I was looking for:** Whether the top results made intuitive sense, and whether removing or changing one signal produced the expected shift in rankings.

**What surprised me:**

The genre bonus is far more powerful than I expected. Even when energy was set to 0.9 — a very specific preference — low-energy lofi songs still dominated because they matched the genre label. The system gave more weight to a single word ("lofi") than to a precise numeric preference. Removing mood in Experiment B also reshuffled results in a way that felt more honest: songs that were genuinely close in energy rose to the top instead of being pushed down by a mood-tag tiebreaker.

---

## 8. Intended Use and Non-Intended Use

**Intended use:**
- Learning how content-based recommenders work
- Exploring how scoring weights affect rankings
- Classroom discussion about bias, filter bubbles, and algorithmic fairness

**Not intended for:**
- Real music apps or production use
- Making recommendations for actual users with real listening history
- Replacing systems that learn from behavior, popularity, or social signals
- Any context where fairness to diverse musical tastes actually matters

---

## 9. Ideas for Improvement

**1. Cap the genre bonus or make it a multiplier, not a flat add.**
The +3.0 bonus is the root cause of the filter bubble. Changing it to a smaller bonus — or making it scale with how many matching songs exist — would let energy and mood matter more and break users out of their genre bubble.

**2. Add a "no match found" warning.**
When the user's genre or mood does not appear in any song in the catalog, the system should say so. Something like "No songs matched your preferred genre — showing closest alternatives." This makes the system honest instead of quietly pretending it found a good answer.

**3. Add a diversity rule to the final ranking.**
Right now the top five can all be from the same genre and artist. A simple rule — like "no more than two songs from the same genre" — would make recommendations feel broader and more useful, especially for users whose genre has many catalog entries.

---

## 10. Personal Reflection

### Biggest Learning Moment

The biggest moment was running the Impossible Combo test. I set the energy target to 0.9 — very high — and expected high-energy songs to rise to the top. They did not. Two quiet lofi songs still came in first and second. A rock song with almost exactly the right energy came in last. I had written the scoring function myself, so I knew why it happened. But seeing it in the output still felt wrong. That was the moment I understood what a filter bubble actually is — not a concept from a textbook, but a real output on my screen where the system looked confident and was giving the wrong answer. One number (the genre weight, set to 3.0) was making all the other preferences irrelevant. I had put it there. That felt like real responsibility.

### How AI Tools Helped — and Where I Had to Check

AI tools helped most during the design phase. When I needed to think through the scoring rules, writing out the algorithm recipe in plain language first — and then checking whether the code matched the description — was something I could go back and forth on quickly. That loop between "here is what I want it to do" and "here is what it actually does" was faster with AI assistance.

Where I had to double-check: the explanation strings in the output. Early on, the "Why" line showed the right numbers but did not always reflect the actual rule that fired. I had to read the code and the output side by side and ask myself whether the explanation was honest. A confident-looking output is not the same as a correct one. That is true of AI-assisted code just as much as it is true of the recommender itself.

### What Surprised Me About Simple Algorithms

I expected a point-based system to feel mechanical and obvious. It does not. When the normal profile runs and the output shows Library Rain at the top with a score of 6.81 and a reason like "genre match (lofi) +3.0 | mood match (chill) +2.0 | energy 0.35 vs target 0.4 +0.95 | acousticness +0.86" — it genuinely feels like a recommendation. It feels like the system understood something. But it did not understand anything. It added four numbers. The feeling of intelligence came entirely from the formatting and the fact that the answer happened to be reasonable. That gap — between what the system actually does and what it feels like it does — is something I will not forget. It made me much more skeptical of any system that presents confident output without showing its work.

### What I Would Try Next

**Weight learning.** Right now the weights (3.0, 2.0, 1.0) were chosen by hand. I would want to try letting users rate a few songs and then adjust the weights automatically based on their feedback. If a user keeps skipping genre matches but listening to energy matches, the system should figure that out.

**Mood similarity.** Right now "chill" and "relaxed" score zero points for each other even though a human would consider them close. I would add a small partial score for moods that are in the same family — so the system does not treat every non-match as a complete failure.

**A "why not" explanation.** The current output tells you why a song ranked high. I would also want to show why a song did not appear — for example, "Storm Runner was excluded because its genre (rock) did not match your preference (lofi), costing it 3.0 points." That would make the filter bubble visible to the user, not just to someone reading the code.
