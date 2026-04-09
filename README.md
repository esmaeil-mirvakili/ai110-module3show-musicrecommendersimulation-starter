# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify or YouTube learn from listening history, skips, and likes to find patterns across millions of users and songs. This version takes a simpler, transparent approach called content-based filtering: it compares what a user says they want directly against the measurable features of each song. It prioritizes clarity over complexity — genre and mood are the strongest signals, with energy used as a continuous tie-breaker based on closeness to the user's target value.

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
  - Each `Song` stores: `genre`, `mood`, `energy` (0–1), `tempo_bpm`, `valence`, `danceability`, and `acousticness` (0–1). The most useful for scoring are genre, mood, energy, and acousticness.
- What information does your `UserProfile` store
  - `UserProfile` stores: `favorite_genre`, `favorite_mood`, `target_energy` (a float between 0 and 1), and `likes_acoustic` (a boolean).
- How does your `Recommender` compute a score for each song
  - It adds up points: +3.0 if genre matches, +2.0 if mood matches, +(1 - |song.energy - user.target_energy|) for energy closeness, and +song.acousticness if the user likes acoustic sound.
- How do you choose which songs to recommend
  - All songs are scored, then sorted by score descending. The top `k` songs (default 5) are returned.

You can include a simple diagram or bullet list if helpful.

### Algorithm Recipe

For every song in the catalog, a score is computed by summing these rules:

| Rule | Points |
|------|--------|
| Song's genre matches `favorite_genre` | +3.0 |
| Song's mood matches `favorite_mood` | +2.0 |
| Energy closeness: `1 - abs(song.energy - target_energy)` | +0.0 to +1.0 |
| Song's `acousticness` (only if `likes_acoustic = True`) | +0.0 to +1.0 |

Maximum possible score: ~7.0. After scoring all songs, they are sorted by score descending and the top `k` (default 5) are returned.

### Flowchart

```mermaid
flowchart TD
    A([User Preferences\ngenre · mood · energy · likes_acoustic]) --> B[Load songs.csv]
    B --> C{For each song\nin catalog}

    C --> D[+3.0 if genre matches]
    C --> E[+2.0 if mood matches]
    C --> F[+0.0 to 1.0 energy closeness\n1 - abs song.energy - target]
    C --> G[+acousticness\nif likes_acoustic = True]

    D & E & F & G --> H[Sum = total score]
    H --> I{More songs?}
    I -- Yes --> C
    I -- No --> J[Sort all songs\nby score descending]
    J --> K([Top K Recommendations\ntitle · score · explanation])
```

### Potential Biases

- **Genre/mood dominance:** The +3.0 and +2.0 bonuses are so large that a genre or mood mismatch is almost impossible to overcome. Songs outside the user's preferred genre are systematically ranked low even if they would otherwise be a good fit.
- **Catalog bias:** The 18-song dataset skews toward certain genres (lofi, ambient, rock). Underrepresented genres like classical or r&b will rarely surface regardless of user preferences.
- **Acoustic preference asymmetry:** `likes_acoustic = True` adds up to +1.0, but there is no equivalent penalty when `likes_acoustic = False`, so users who dislike acoustic sound are not actively steered away from it.
- **No personalization over time:** The system only reflects what the user explicitly states. It cannot learn from skips, replays, or changing taste.

---

## Demo

![Terminal output showing top 5 recommendations](screenshot.png)

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Adversarial Profiles — Edge Case Testing

These profiles were designed to stress-test the scoring logic by presenting conflicting, missing, or extreme preferences. Each one targets a specific weakness in the algorithm.

---

### #1 — The Impossible Combo

**Profile:** `genre: lofi, mood: chill, energy: 0.9, likes_acoustic: False`

> Chill mood but very high energy target. Lofi/chill songs have energy ~0.35–0.42, so mood match and energy closeness pull in opposite directions.

![Adversarial #1 results](adv1.png)

**What happened:** Genre and mood dominance won completely. The two lofi/chill songs (Midnight Coding, Library Rain) ranked #1 and #2 despite having energy ~0.42 — nearly the opposite of the 0.9 target. Storm Runner, whose energy 0.91 is almost a perfect energy match, ranked dead last at 0.99 because it matched neither genre nor mood. The combined +5.0 genre+mood bonus cannot be overcome by energy alone.

---

### #2 — The Ghost Genre

**Profile:** `genre: metal, mood: intense, energy: 0.95, likes_acoustic: False`

> "metal" does not exist in the catalog, so the +3.0 genre bonus never fires for any song.

![Adversarial #2 results](adv2.png)

**What happened:** The system fell back gracefully to mood and energy. Gym Hero and Storm Runner rose to the top by matching mood "intense" (+2.0) and having high energy. However, without genre firing, there is a large scoring cliff: the top two songs score ~2.97, while everything else scores below 1.0. The ranking is functional but shallow — only 2 songs triggered any meaningful bonus.

---

### #3 — The Missing Mood

**Profile:** `genre: pop, mood: sad, energy: 0.7, likes_acoustic: False`

> "sad" does not appear in any song's mood field, so the +2.0 mood bonus is permanently dead.

![Adversarial #3 results](adv3.png)

**What happened:** Genre dominance is exposed clearly. The two pop songs (Sunrise City 3.88, Gym Hero 3.77) rank far ahead of everything else. Songs #3–#5 cluster tightly between 0.95 and 0.98, showing that energy alone barely differentiates songs when no other signal fires. A user who prefers "sad" music gets happy and intense pop songs — the system has no way to penalize a wrong mood, only reward a correct one.

---

### #4 — The Acoustic Trap

**Profile:** `genre: ambient, mood: chill, energy: 0.9, likes_acoustic: True`

> Highly acoustic songs also tend to have very low energy. The acousticness bonus and energy closeness pull at completely opposite songs.

![Adversarial #4 results](adv4.png)

**What happened:** Acousticness + genre + mood overwhelmed the energy preference entirely. Spacewalk Thoughts ranked #1 with energy 0.28 — nearly the opposite of the requested 0.9 — because its genre, mood, and acousticness bonuses added up to +5.92. The system recommended calm, quiet ambient songs to a user who explicitly asked for high-energy music. This is the starkest example of the acoustic asymmetry bias: `likes_acoustic` adds reward but there is no equivalent penalty when it conflicts with energy.

---

### #5 — The Neutral Energy

**Profile:** `genre: synthwave, mood: moody, energy: 0.5, likes_acoustic: False`

> energy: 0.5 is the midpoint, so every song scores at least +0.5 on that rule, compressing the spread.

![Adversarial #5 results](adv5.png)

**What happened:** The single synthwave song (Night Drive Loop) dominated at 5.75 — far ahead of the rest — because it hit all three active signals. Songs without a genre or mood match clustered between 0.90 and 0.95, a very narrow band where ordering is nearly arbitrary. The neutral energy did compress the tail of the ranking, but the top result was still unambiguous because genre+mood combined create a large enough gap.

---

### #6 — The Blank Slate

**Profile:** `genre: jazz, mood: melancholic, energy: 0.5, likes_acoustic: False`

> "melancholic" is not in the catalog and jazz only has 2 songs. With most signals silent, rankings should collapse to energy closeness.

![Adversarial #6 results](adv6.png)

**What happened:** The two jazz songs (Coffee Shop Stories 3.87, Late Night Sax 3.83) still dominated because the +3.0 genre bonus is powerful enough to carry them even without a mood match. The remaining three slots (#3–#5) scored between 0.90 and 0.95 — separated by fractions of a point — making their order essentially arbitrary. The mood preference "melancholic" was completely invisible in the output: the system had no way to signal that it failed to find what the user actually wanted.

---

## Experiments You Tried

Both experiments use the same baseline profile so results are directly comparable:
`genre: lofi, mood: chill, energy: 0.4, likes_acoustic: True`

Default weights for reference: `genre=3.0, mood=2.0, energy=1.0`

---

### Experiment A — Weight Shift (genre ×0.5, energy ×2)

**Change:** `genre_weight: 3.0 → 1.5` and `energy_weight: 1.0 → 2.0`

Energy can now contribute up to **+2.0** instead of +1.0. A genre match is worth **+1.5** instead of +3.0.

| Rank | Song | Score |
|------|------|-------|
| #1 | Library Rain — Paper Lanterns | 6.26 |
| #2 | Midnight Coding — LoRoom | 6.17 |
| #3 | Spacewalk Thoughts — Orbit Bloom | 4.68 |
| #4 | Focus Flow — LoRoom | 4.28 |
| #5 | Coffee Shop Stories — Slow Stereo | 2.83 |

**What changed vs. baseline:** The top 2 songs stayed the same (Library Rain, Midnight Coding) because they match on all signals. The bigger shift is in #3 and below — Spacewalk Thoughts (no genre match) climbed into top 3 because its energy 0.28 is close enough to 0.4 to earn +1.76, and Focus Flow jumped up thanks to a perfect energy match scoring +2.00. The ranking became more sensitive to how close a song's energy is to the target, and the genre bonus lost some of its dominance.

---

### Experiment B — Feature Removal (mood weight = 0)

**Change:** `mood_weight: 2.0 → 0.0` — equivalent to commenting out the mood check in `score_song`.

| Rank | Song | Score |
|------|------|-------|
| #1 | Library Rain — Paper Lanterns | 4.81 |
| #2 | Focus Flow — LoRoom | 4.78 |
| #3 | Midnight Coding — LoRoom | 4.69 |
| #4 | Coffee Shop Stories — Slow Stereo | 1.86 |
| #5 | Late Night Sax — Slow Stereo | 1.84 |

**What changed vs. baseline:** Removing mood reshuffled the lofi songs significantly. In the baseline, Midnight Coding ranked #1 because it matched mood "chill" (+2.0). Without that bonus, Focus Flow jumped to #2 — it has a perfect energy match (+1.00) and solid acousticness (+0.78), which now matter more. Library Rain held #1 due to strong acousticness (+0.86) edging it ahead. The bottom half changed entirely: jazz songs (Coffee Shop Stories, Late Night Sax) entered the top 5 purely on acousticness, showing that mood was previously blocking them from appearing.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

