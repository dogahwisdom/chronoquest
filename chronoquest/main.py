import random
import os

def load_inventions(filename="game_data.txt"):
    inventions = []
    try:
        with open(filename, "r") as file:
            next(file)
            for line in file:
                try:
                    year, name, inventor, summary = line.strip().split(",", 3)
                    inventions.append({
                        "year": int(year),
                        "name": name.strip(),
                        "inventor": inventor.strip(),
                        "summary": summary.strip()
                    })
                except ValueError:
                    print(f"Skipping invalid line: {line}")
    except FileNotFoundError:
        print("Error: game_data.txt not found!")
        exit()
    return inventions

def load_high_score(filename="high_score.txt"):
    try:
        with open(filename, "r") as file:
            high_score = int(file.readline().strip())
    except (FileNotFoundError, ValueError):
        return 0
    return high_score

def save_high_score(score, filename="high_score.txt"):
    with open(filename, "w") as file:
        file.write(str(score))

def display_invention(invention):
    print(f"  {invention['name']}")

def get_user_choice():
    while True:
        choice = input("Which came first (A or B)? Enter 'H' for a hint: ").upper()
        if choice in ("A", "B", "H"):
            return choice
        print("Invalid choice. Please enter A, B, or H.")

def show_hint(invention):
    print(f"Hint: Inventor - {invention['inventor']}, Summary - {invention['summary']}")

def show_tutorial():
    print("Welcome to ChronoQuest!")
    print("You'll be presented with two inventions. Your task is to choose which one was invented earlier.")
    print("Enter 'A' or 'B' to make your selection.")
    print("You can request a hint by entering 'H'.")
    print("The difficulty increases as you progress.")

def play_round(inventions, mistakes, score, high_score, difficulty):
    while True:
        invention1, invention2 = random.sample(inventions, 2)
        year_diff = abs(invention1["year"] - invention2["year"])

        # Use tuples to represent pairs of inventions in mistakes
        pair1 = (invention1["name"], invention2["name"])
        pair2 = (invention2["name"], invention1["name"])

        if pair1 not in mistakes and pair2 not in mistakes and \
           ((difficulty == 'easy' and year_diff >= 10) or
            (difficulty == 'medium' and 5 <= year_diff < 10) or
            (difficulty == 'hard' and year_diff < 5)):
            break

    display_invention(invention1)
    display_invention(invention2)

    while True:
        choice = get_user_choice()
        if choice == 'H':
            show_hint(invention1)
            show_hint(invention2)
            continue
        break

    correct = (choice == "A" and invention1["year"] < invention2["year"]) or \
              (choice == "B" and invention2["year"] < invention1["year"])

    if correct:
        score += 1
        print("Correct!")
        if score > high_score:
            high_score = score
            save_high_score(high_score)
            print("New high score!")
        print(f"Current Score: {score}   High Score: {high_score}\n")

        if score <= 5:
            difficulty = 'easy'
        elif 5 < score <= 10:
            difficulty = 'medium'
        else:
            difficulty = 'hard'

    else:
        print("Incorrect!")
        mistakes.add(pair1)
        correct_answer = invention1 if invention1["year"] < invention2["year"] else invention2
        print(f"The correct answer is: {correct_answer['name']} was invented in {correct_answer['year']}.")
        return False, score, high_score, difficulty

    return True, score, high_score, difficulty

def play_game(inventions):
    mistakes = set()
    score = 0
    high_score = load_high_score()
    num_wrong = 0
    difficulty = 'easy'

    print("\nHow to Play:")
    print("1. Login: Enter a nickname to begin.")
    print("2. Gameplay: You'll be presented with two inventions. Choose which one was invented earlier.")
    print("3. Scoring: Earn points for correct answers. The game ends after three incorrect answers.")
    print("4. Hints: Request hints to see the inventor's name and a brief description of the invention.")
    print("5. High Scores: Your high score is saved and displayed at the end of the game.")

    while num_wrong < 3:
        correct, score, high_score, difficulty = play_round(inventions, mistakes, score, high_score, difficulty)
        if not correct:
            num_wrong += 1

    print(f"Game over! Final score: {score}")

    reset_choice = input("Do you want to reset the game data (high score and mistakes)? (y/n): ").lower()
    if reset_choice == "y":
        try:
            os.remove("../.venv/high_score.txt")
            print("Game data reset.")
        except FileNotFoundError:
            pass

def main():
    print("\nWelcome to ChronoQuest: The Invention's Challenge!\n")
    nickname = input("Enter your nickname: ")
    print(f"\nHello, {nickname}!\n")

    challenge_choice = input("Do you want to participate in the Invention Challenge? (y/n): ").lower()
    if challenge_choice == "y":
        inventions = load_inventions()
        play_game(inventions)
    else:
        print("Maybe next time! Thank you for visiting ChronoQuest.")

if __name__ == "__main__":
    main()
