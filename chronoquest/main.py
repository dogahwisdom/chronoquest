import random
import os


def load_inventions(filename="game_data.txt"):
    inventions = []
    try:
        with open(filename, "r") as file:
            next(file)  # Skip the header
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
        print(f"Error: {filename} not found!")
        exit(1)
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


def play_round(inventions, mistakes, score, high_score, difficulty):
    if len(inventions) < 2:
        raise ValueError("Insufficient inventions to play a round.")

    max_attempts = 10  # Prevent infinite loop
    attempts = 0

    while attempts < max_attempts:
        invention1, invention2 = random.sample(inventions, 2)
        year_diff = abs(invention1["year"] - invention2["year"])

        pair1 = (invention1["name"], invention2["name"])
        pair2 = (invention2["name"], invention1["name"])

        if pair1 not in mistakes and pair2 not in mistakes and \
           ((difficulty == 'easy' and year_diff >= 10) or
            (difficulty == 'medium' and 5 <= year_diff < 10) or
            (difficulty == 'hard' and year_diff < 5)):
            break
        attempts += 1

    if attempts == max_attempts:
        raise ValueError("Unable to find valid invention pair for this round.")

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

        difficulty = 'easy' if score <= 5 else 'medium' if score <= 10 else 'hard'
    else:
        print("Incorrect!")
        mistakes.add(pair1)
        correct_answer = invention1 if invention1["year"] < invention2["year"] else invention2
        print(f"The correct answer is: {correct_answer['name']} was invented in {correct_answer['year']}.")
        return False, score, high_score, difficulty

    return True, score, high_score, difficulty


def play_game(inventions):
    score = 0
    high_score = load_high_score()
    mistakes = set()
    difficulty = 'easy'

    while True:
        try:
            continue_game, score, high_score, difficulty = play_round(inventions, mistakes, score, high_score, difficulty)
            if not continue_game:
                break
        except ValueError as e:
            print(e)
            break

    print(f"Game over! Your final score is {score}.")


def main():
    print("\nWelcome to ChronoQuest: The Invention's Challenge!\n")
    nickname = input("Enter your nickname: ")
    print(f"\nHello, {nickname}!\n")

    challenge_choice = input("Do you want to participate in the Invention Challenge? (y/n): ").lower()
    if challenge_choice == "y":
        inventions = load_inventions()
        if not inventions:
            print("No inventions available to play. Exiting.")
            return
        play_game(inventions)
    else:
        print("Maybe next time! Thank you for visiting ChronoQuest.")


if __name__ == "__main__":
    main()
