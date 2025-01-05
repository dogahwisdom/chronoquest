from chronoquest.main import (
    load_inventions,
    load_high_score,
    save_high_score,
    display_invention,
    get_user_choice,
    show_hint,
    play_round,
)


MOCK_INVENTIONS = [
    {"year": 1876, "name": "Telephone", "inventor": "Alexander Graham Bell", "summary": "Device for communication"},
    {"year": 1903, "name": "Airplane", "inventor": "Wright Brothers", "summary": "First powered flight"},
    {"year": 1859, "name": "Oil Drill", "inventor": "Edwin Drake", "summary": "Drilled the first oil well"},
]


def test_load_inventions(monkeypatch):
    mock_data = (
        "year,name,inventor,summary\n"
        "1876,Telephone,Alexander Graham Bell,Device for communication\n"
        "1903,Airplane,Wright Brothers,First powered flight\n"
    )

    def mock_open(*args, **kwargs):
        from io import StringIO
        return StringIO(mock_data)

    monkeypatch.setattr("builtins.open", mock_open)
    inventions = load_inventions()

    assert len(inventions) == 2
    assert inventions[0]["name"] == "Telephone"
    assert inventions[1]["inventor"] == "Wright Brothers"


def test_load_high_score(monkeypatch):
    def mock_open(*args, **kwargs):
        from io import StringIO
        return StringIO("42")

    monkeypatch.setattr("builtins.open", mock_open)
    high_score = load_high_score()
    assert high_score == 42


def test_save_high_score(tmpdir):
    temp_file = tmpdir.join("high_score.txt")
    save_high_score(100, filename=str(temp_file))

    with open(temp_file, "r") as file:
        saved_score = int(file.read())
    assert saved_score == 100


def test_display_invention(capfd):
    invention = {"name": "Telephone"}
    display_invention(invention)
    captured = capfd.readouterr()
    assert "Telephone" in captured.out


def test_get_user_choice(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "A")
    assert get_user_choice() == "A"

    monkeypatch.setattr("builtins.input", lambda _: "B")
    assert get_user_choice() == "B"

    monkeypatch.setattr("builtins.input", lambda _: "H")
    assert get_user_choice() == "H"


def test_show_hint(capfd):
    invention = {"inventor": "Wright Brothers", "summary": "First powered flight"}
    show_hint(invention)
    captured = capfd.readouterr()
    assert "Wright Brothers" in captured.out
    assert "First powered flight" in captured.out


def test_play_round(monkeypatch, capfd):

    def mock_get_user_choice():
        return "A"

    monkeypatch.setattr("chronoquest.main.get_user_choice", mock_get_user_choice)

    mistakes = set()
    score = 0
    high_score = 0
    difficulty = "easy"

    correct, score, high_score, difficulty = play_round(
        MOCK_INVENTIONS, mistakes, score, high_score, difficulty
    )


    assert correct
    assert score == 1
    assert high_score == 1
    assert "Correct!" in capfd.readouterr().out
