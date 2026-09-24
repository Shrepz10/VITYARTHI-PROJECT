import random

from words import SCRAMBLE_WORDS, WORD_GUESS_QUESTIONS, WORD_CHAIN_WORDS
from questions import QUIZ_QUESTIONS
from utils import show_title, pause, get_choice


def create_player():
    """Create and return a new player dictionary."""
    name = input("Enter your name: ").strip()

    if not name:
        name = "Player"

    return {
        "name": name,
        "score": 0,
        "lives": 3,
        "level": 1,
        "words_found": [],
        "hints_used": 0
    }


def add_score(player, points):
    """Add points to player's score."""
    player["score"] += points


def lose_life(player):
    """Remove one life from the player."""
    player["lives"] -= 1


def show_status(player):
    """Display player's current status."""
    print()
    print("-" * 45)
    print(f"Player : {player['name']}")
    print(f"Score  : {player['score']}")
    print(f"Lives  : {'❤️ ' * player['lives']}")
    print(f"Level  : {player['level']}")
    print("-" * 45)


def show_instructions():
    show_title("HOW TO PLAY")

    print("""
Word Quest is a text-based word adventure game.

Your goal is to complete different word challenges
and collect enough points to unlock the final challenge.

GAME RULES
----------
1. You start with 3 lives.
2. Correct answers give you points.
3. Wrong answers can cost you a life.
4. You can use hints in some challenges.
5. Complete all chapters to reach the final challenge.
6. Your final score can be saved to the leaderboard.

CHAPTERS
--------
1. Word Scramble
2. Word Guess
3. Word Quiz
4. Word Chain
5. Final Secret Word
""")

    pause()


def scramble_word(word):
    """Return a scrambled version of a word."""
    letters = list(word)

    while True:
        random.shuffle(letters)
        scrambled = "".join(letters)

        if scrambled != word:
            return scrambled


def play_scramble(player):
    show_title("CHAPTER 1 - WORD SCRAMBLE")

    word = random.choice(SCRAMBLE_WORDS)
    scrambled = scramble_word(word)

    print(f"\nUnscramble this word:")
    print(f"\n    {scrambled.upper()}")

    answer = input("\nYour answer: ").strip().lower()

    if answer == word.lower():
        print("\n✓ Correct!")
        add_score(player, 10)
        player["words_found"].append(word)
    else:
        print(f"\n✗ Wrong!")
        print(f"The correct word was: {word}")
        lose_life(player)

    show_status(player)
    pause()


def play_word_guess(player):
    show_title("CHAPTER 2 - WORD GUESS")

    question = random.choice(WORD_GUESS_QUESTIONS)

    print("\nYou have to guess the word using the clues.")

    for number, clue in enumerate(question["clues"], start=1):
        print(f"\nClue {number}: {clue}")

        answer = input("Your answer (or type 'hint'): ").strip().lower()

        if answer == "hint":
            print(f"Hint: The word starts with '{question['answer'][0].upper()}'")
            player["hints_used"] += 1
            answer = input("Your answer: ").strip().lower()

        if answer == question["answer"].lower():
            print("\n✓ Correct!")
            add_score(player, 15)
            player["words_found"].append(question["answer"])
            break

        if number < len(question["clues"]):
            print("✗ Not correct. Here's another clue.")
        else:
            print("\n✗ Wrong!")
            print(f"The correct answer was: {question['answer']}")
            lose_life(player)

    show_status(player)
    pause()


def play_quiz(player):
    show_title("CHAPTER 3 - WORD QUIZ")

    question = random.choice(QUIZ_QUESTIONS)

    print(f"\n{question['question']}\n")

    for option in question["options"]:
        print(option)

    answer = input("\nYour answer (A/B/C/D): ").strip().upper()

    if answer == question["answer"]:
        print("\n✓ Correct!")
        add_score(player, 20)
    else:
        print("\n✗ Wrong!")
        print(f"The correct answer is {question['answer']}.")
        lose_life(player)

    show_status(player)
    pause()


def play_word_chain(player):
    show_title("CHAPTER 4 - WORD CHAIN")

    print("""
Rules:
The next word must start with the LAST letter
of the previous word.

Example:
CAT → TIGER → ROBOT → TABLE
""")

    current_word = random.choice(WORD_CHAIN_WORDS)

    print(f"Starting word: {current_word.upper()}")

    used_words = {current_word.lower()}
    points = 0

    for _ in range(3):
        answer = input(
            f"\nEnter a word starting with '{current_word[-1].upper()}': "
        ).strip().lower()

        if answer in used_words:
            print("✗ You already used that word.")
            lose_life(player)
            continue

        if not answer.isalpha():
            print("✗ Please enter a word using letters only.")
            lose_life(player)
            continue

        if answer[0] != current_word[-1].lower():
            print(
                f"✗ Wrong! Your word must start with "
                f"'{current_word[-1].upper()}'."
            )
            lose_life(player)
            continue

        if answer not in WORD_CHAIN_WORDS:
            print("✗ That word is not in the game's word bank.")
            lose_life(player)
            continue

        print("✓ Good word!")

        used_words.add(answer)
        current_word = answer
        points += 5

    add_score(player, points)

    print(f"\nYou earned {points} points in the Word Chain!")

    show_status(player)
    pause()


def final_challenge(player):
    show_title("FINAL CHALLENGE - SECRET WORD")

    print("""
Congratulations!

You have completed all four chapters.

Now solve the final secret word.

The secret word is related to this game:

Hint:
I am a programming language.
I am also the name of a snake.
""")

    answer = input("\nWhat is the secret word? ").strip().lower()

    if answer == "python":
        print("""
╔══════════════════════════════════════════╗
║             YOU WON! 🎉                 ║
║                                          ║
║       You unlocked the Secret Book!      ║
╚══════════════════════════════════════════╝
""")

        add_score(player, 50)

    else:
        print("\n✗ Incorrect.")
        print("The secret word was PYTHON.")

    show_status(player)
    save_score(player)
    pause()


def save_score(player):
    """Save the player's score to scores.txt."""
    with open("scores.txt", "a") as file:
        file.write(
            f"{player['name']} - {player['score']}\n"
        )


def show_leaderboard():
    show_title("LEADERBOARD")

    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()

        if not scores:
            print("\nNo scores yet.")
            pause()
            return

        score_list = []

        for line in scores:
            line = line.strip()

            if " - " in line:
                name, score = line.rsplit(" - ", 1)

                try:
                    score = int(score)
                    score_list.append((name, score))
                except ValueError:
                    pass

        score_list.sort(key=lambda item: item[1], reverse=True)

        print()

        for position, (name, score) in enumerate(score_list[:10], start=1):
            print(f"{position}. {name} - {score} points")

    except FileNotFoundError:
        print("\nNo scores have been recorded yet.")

    pause()


def start_game():
    """Start the main game."""
    show_title("WORD QUEST")
    print("      The Library of Secrets")
    print()

    player = create_player()

    while player["lives"] > 0:

        show_title("MAIN MENU")

        print("1. Start / Continue Game")
        print("2. Instructions")
        print("3. Show Status")
        print("4. Leaderboard")
        print("5. Exit")

        choice = get_choice(
            "\nEnter your choice: ",
            ["1", "2", "3", "4", "5"]
        )

        if choice == "1":
            if player["level"] == 1:
                play_scramble(player)

                if player["lives"] > 0:
                    player["level"] = 2

            elif player["level"] == 2:
                play_word_guess(player)

                if player["lives"] > 0:
                    player["level"] = 3

            elif player["level"] == 3:
                play_quiz(player)

                if player["lives"] > 0:
                    player["level"] = 4

            elif player["level"] == 4:
                play_word_chain(player)

                if player["lives"] > 0:
                    player["level"] = 5

            elif player["level"] == 5:
                final_challenge(player)
                break

        elif choice == "2":
            show_instructions()

        elif choice == "3":
            show_status(player)
            pause()

        elif choice == "4":
            show_leaderboard()

        elif choice == "5":
            print("\nThanks for playing Word Quest!")
            break

    if player["lives"] <= 0:
        show_title("GAME OVER")

        print(f"""
Sorry, {player['name']}!

You ran out of lives.

Final Score: {player['score']}
""")

        save_score(player)
        pause()
