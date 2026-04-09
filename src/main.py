"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations(
    label: str,
    user_prefs: dict,
    songs: list,
    k: int = 5,
    genre_weight: float = 3.0,
    mood_weight: float = 2.0,
    energy_weight: float = 1.0,
) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k, genre_weight=genre_weight, mood_weight=mood_weight, energy_weight=energy_weight)
    print("\n" + "=" * 60)
    print(f"  {label}")
    print(f"  Profile: {user_prefs}")
    print(f"  Weights: genre={genre_weight}, mood={mood_weight}, energy={energy_weight}")
    print("=" * 60)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']}  —  {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Why   : {explanation}")
    print("\n" + "=" * 60)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print("Loaded songs: ", len(songs))

    # --- Normal profile ---
    # Baseline: a lofi/chill listener who likes acoustic sound and calm energy.
    print_recommendations(
        "Normal Profile — Lofi Chill Listener",
        {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            "likes_acoustic": True,
        },
        songs,
    )

    # --- Adversarial #1: The Impossible Combo ---
    # Chill mood but very high energy target. Chill songs in the catalog have
    # low energy (0.35–0.42), so mood match and energy closeness pull in opposite
    # directions. Does a chill song win (mood bonus) or a high-energy song win?
    print_recommendations(
        "Adversarial #1 — The Impossible Combo (chill mood + high energy)",
        {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.9,
            "likes_acoustic": False,
        },
        songs,
    )

    # --- Adversarial #2: The Ghost Genre ---
    # 'metal' does not exist in the catalog, so the +3.0 genre bonus never fires.
    # Tests whether the system falls back gracefully to mood and energy signals,
    # or whether the ranking feels arbitrary without the strongest signal.
    print_recommendations(
        "Adversarial #2 — The Ghost Genre (genre not in catalog)",
        {
            "genre": "metal",
            "mood": "intense",
            "energy": 0.95,
            "likes_acoustic": False,
        },
        songs,
    )

    # --- Adversarial #3: The Missing Mood ---
    # 'sad' does not appear in any song's mood field. The +2.0 mood bonus is
    # permanently dead. Reveals how dominant the mood signal normally is by
    # showing what rankings look like when it can never fire.
    print_recommendations(
        "Adversarial #3 — The Missing Mood (mood not in catalog)",
        {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.7,
            "likes_acoustic": False,
        },
        songs,
    )

    # --- Adversarial #4: The Acoustic Trap ---
    # Highly acoustic songs (classical, ambient) also have very low energy.
    # likes_acoustic rewards them with up to +1.0, but energy: 0.9 punishes
    # them heavily. Exposes the tension between acousticness and energy when
    # they point at completely different songs.
    print_recommendations(
        "Adversarial #4 — The Acoustic Trap (high energy + likes_acoustic)",
        {
            "genre": "ambient",
            "mood": "chill",
            "energy": 0.9,
            "likes_acoustic": True,
        },
        songs,
    )

    # --- Adversarial #5: The Neutral Energy ---
    # energy: 0.5 is the midpoint, so every song scores at least +0.5 on that
    # rule, compressing the spread across the whole catalog. Tests whether the
    # remaining signals (genre, mood) still produce a meaningful ranking or
    # whether scores cluster too tightly to differentiate songs.
    print_recommendations(
        "Adversarial #5 — The Neutral Energy (energy: 0.5, compressed spread)",
        {
            "genre": "synthwave",
            "mood": "moody",
            "energy": 0.5,
            "likes_acoustic": False,
        },
        songs,
    )

    # --- Adversarial #6: The Blank Slate ---
    # 'melancholic' is not in the catalog (mood bonus never fires), and 'jazz'
    # only has 2 songs. With most signals silent, the ranking collapses almost
    # entirely to energy closeness (~0.5 for everyone). Tests whether the system
    # still produces a meaningful list when nearly all scoring rules are dead.
    print_recommendations(
        "Adversarial #6 — The Blank Slate (most signals silent)",
        {
            "genre": "jazz",
            "mood": "melancholic",
            "energy": 0.5,
            "likes_acoustic": False,
        },
        songs,
    )

    # Baseline profile reused for both sensitivity experiments so results are
    # directly comparable to the normal run above.
    baseline = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
    }

    # --- Experiment A: Weight Shift ---
    # Genre weight halved (3.0 → 1.5), energy weight doubled (1.0 → 2.0).
    # Energy can now contribute up to +2.0 instead of +1.0, while a genre match
    # is worth less than before. Expect songs whose energy is close to 0.4 to
    # climb the ranking even if they don't match the genre.
    print_recommendations(
        "Experiment A — Weight Shift (genre ×0.5, energy ×2)",
        baseline,
        songs,
        genre_weight=1.5,
        mood_weight=2.0,
        energy_weight=2.0,
    )

    # --- Experiment B: Feature Removal (mood disabled) ---
    # Mood weight set to 0.0, effectively removing it from scoring.
    # Equivalent to commenting out the mood check in score_song.
    # Expect songs that matched on mood to drop in rank as that +2.0 bonus
    # disappears, and energy/acousticness to gain relative influence.
    print_recommendations(
        "Experiment B — Feature Removal (mood weight = 0)",
        baseline,
        songs,
        genre_weight=3.0,
        mood_weight=0.0,
        energy_weight=1.0,
    )


if __name__ == "__main__":
    main()
