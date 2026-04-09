import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return them as a list of dicts."""
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(
    user_prefs: Dict,
    song: Dict,
    genre_weight: float = 3.0,
    mood_weight: float = 2.0,
    energy_weight: float = 1.0,
) -> float:
    """Return a numeric score for a song based on how well it matches user preferences."""
    score = 0.0
    if song["genre"] == user_prefs.get("genre"):
        score += genre_weight
    if song["mood"] == user_prefs.get("mood"):
        score += mood_weight
    score += energy_weight * (1 - abs(song["energy"] - user_prefs.get("energy", 0.5)))
    if user_prefs.get("likes_acoustic"):
        score += song["acousticness"]
    return score


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    genre_weight: float = 3.0,
    mood_weight: float = 2.0,
    energy_weight: float = 1.0,
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score, and return the top k as (song, score, explanation) tuples."""
    def build_explanation(song: Dict) -> str:
        """Build a human-readable string listing each scoring rule and its contribution."""
        reasons = []
        if song["genre"] == user_prefs.get("genre"):
            reasons.append(f"genre match ({song['genre']}) +{genre_weight:.1f}")
        if song["mood"] == user_prefs.get("mood"):
            reasons.append(f"mood match ({song['mood']}) +{mood_weight:.1f}")
        energy_points = energy_weight * (1 - abs(song["energy"] - user_prefs.get("energy", 0.5)))
        reasons.append(f"energy {song['energy']} vs target {user_prefs.get('energy', 0.5)} +{energy_points:.2f}")
        if user_prefs.get("likes_acoustic"):
            reasons.append(f"acousticness +{song['acousticness']:.2f}")
        return " | ".join(reasons)

    scored = [(song, score_song(user_prefs, song, genre_weight, mood_weight, energy_weight)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [(song, score, build_explanation(song)) for song, score in scored[:k]]
