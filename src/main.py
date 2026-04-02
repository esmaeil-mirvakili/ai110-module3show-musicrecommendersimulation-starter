"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print("Loaded songs: ", len(songs))

    # Taste profile: target values for each feature used in scoring
    user_prefs = {
        "genre": "lofi",        # preferred genre for direct match bonus
        "mood": "chill",        # preferred mood for direct match bonus
        "energy": 0.4,          # target energy level (0.0 = very calm, 1.0 = very intense)
        "likes_acoustic": True, # rewards high acousticness scores when True
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  Top Recommendations")
    print("=" * 50)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']}  —  {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Why   : {explanation}")
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
