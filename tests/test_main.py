from chronoquest.main import play_round

MOCK_INVENTIONS = [
    {"year": 1876, "name": "Telephone", "inventor": "Alexander Graham Bell", "summary": "A device for voice communication."},
    {"year": 1879, "name": "Light Bulb", "inventor": "Thomas Edison", "summary": "An electric light source."},
    # Add more mock inventions as needed
]

def test_play_round(monkeypatch, capfd):
    # Mock user input to return the expected correct answer
    def mock_get_user_choice():
        return "Telephone"  # Change from "A" to the actual expected answer

    monkeypatch.setattr("chronoquest.main.get_user_choice", mock_get_user_choice)

    # Initialize test variables
    mistakes = set()
    score = 0
    high_score = 0
    difficulty = "easy"

    # Call the function under test
    correct, score, high_score, difficulty = play_round(
        MOCK_INVENTIONS, mistakes, score, high_score, difficulty
    )

    # Debugging output
    print(f"DEBUG: correct={correct}, score={score}, high_score={high_score}, difficulty={difficulty}")

    # Assertions to validate expected behavior
    assert correct, "Test failed because 'correct' is False when it should be True."
    assert score == 1, f"Test failed: Expected score 1 but got {score}."
    assert high_score == 1, f"Test failed: Expected high_score 1 but got {high_score}."

    output = capfd.readouterr().out
    assert "Correct!" in output, f"Test failed: 'Correct!' not found in output: {output}"