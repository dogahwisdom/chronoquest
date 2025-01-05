import pytest
from chronoquest.main import play_round

MOCK_INVENTIONS = [
    {"year": 1876, "name": "Telephone", "inventor": "Alexander Graham Bell", "summary": "A device for voice communication."},
    {"year": 1879, "name": "Light Bulb", "inventor": "Thomas Edison", "summary": "An electric light source."},
    # Add more mock inventions as needed
]


def test_play_round(monkeypatch, capfd):
    def mock_get_user_choice():
        return "A"  # Simulate the user choosing "A"

    monkeypatch.setattr("chronoquest.main.get_user_choice", mock_get_user_choice)

    mistakes = set()
    score = 0
    high_score = 0
    difficulty = "easy"

    correct, score, high_score, difficulty = play_round(
        MOCK_INVENTIONS, mistakes, score, high_score, difficulty
    )

    # Debugging output
    output = capfd.readouterr().out
    print(f"DEBUG: {output}")

    # Assertions
    assert correct, "Expected 'correct' to be True."
    assert score == 1, f"Expected score to be 1, got {score}."
    assert high_score == 1, f"Expected high_score to be 1, got {high_score}."
    assert "Correct!" in output, "Expected 'Correct!' in the output."
