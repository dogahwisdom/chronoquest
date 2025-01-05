import pytest
from chronoquest.main import play_round

MOCK_INVENTIONS = [
    {"year": 1876, "name": "Telephone", "inventor": "Alexander Graham Bell", "summary": "A device for voice communication."},
    {"year": 1859, "name": "Oil Drill", "inventor": "Edwin Drake", "summary": "Drilled the first oil well."},
]

def test_play_round(monkeypatch, capfd):
    # Mock user input to always choose "B" (correct answer for this mock data)
    def mock_get_user_choice():
        return "B"

    # Mock random.sample to always return specific inventions
    def mock_random_sample(population, k):
        return [MOCK_INVENTIONS[0], MOCK_INVENTIONS[1]]  # Always return "Telephone" and "Oil Drill"

    monkeypatch.setattr("chronoquest.main.get_user_choice", mock_get_user_choice)
    monkeypatch.setattr("random.sample", mock_random_sample)

    mistakes = set()
    score = 0
    high_score = 0
    difficulty = "easy"

    # Call play_round
    correct, score, high_score, difficulty = play_round(
        MOCK_INVENTIONS, mistakes, score, high_score, difficulty
    )

    # Capture printed output
    output = capfd.readouterr().out

    print(f"DEBUG OUTPUT: {output}")

    # Assertions to validate behavior
    assert correct, "Expected 'correct' to be True."
    assert score == 1, f"Expected score to be 1, got {score}."
    assert high_score == 1, f"Expected high_score to be 1, got {high_score}."
    assert "Correct!" in output, "Expected 'Correct!' in the output."
