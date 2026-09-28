import random


def get_full_choice(short_choice):
    choices = {"r": "rock", "p": "paper", "s": "scissors", "l": "lizard", "k": "spock"}
    return choices.get(short_choice, "unknown")


def get_player_choice(challenge=None):
    if challenge is None:
        valid = ["r", "p", "s", "q"]
        prompt = "Enter your choice (r: rock, p: paper, s: scissors, q: quit): "
    else:
        valid = challenge["options"] + ["q"]
        prompt = f"Enter your choice ({', '.join([f'{ch}: {challenge['names'][ch]}' for ch in challenge['options']])}, q: quit): "
    while True:
        choice = input(prompt).lower()
        if choice in valid:
            return choice
        else:
            print(f"Invalid input. Please enter one of {', '.join(valid)}.")


def print_score(player_score, computer_score, ties):
    print(f"Score - You: {player_score}, Computer: {computer_score}, Ties: {ties}")


def get_challenges():
    return [
        {
            "name": "Classic Rock, Paper, Scissors",
            "options": ["r", "p", "s"],
            "names": {"r": "rock", "p": "paper", "s": "scissors"},
            "winning_cases": {("r", "s"), ("p", "r"), ("s", "p")},
        },
        {
            "name": "Rock, Paper, Scissors, Lizard, Spock",
            "options": ["r", "p", "s", "l", "k"],
            "names": {
                "r": "rock",
                "p": "paper",
                "s": "scissors",
                "l": "lizard",
                "k": "spock",
            },
            "winning_cases": {
                ("r", "s"),
                ("r", "l"),  # Rock crushes Scissors and Lizard
                ("p", "r"),
                ("p", "k"),  # Paper covers Rock and disproves Spock
                ("s", "p"),
                ("s", "l"),  # Scissors cuts Paper and decapitates Lizard
                ("l", "p"),
                ("l", "k"),  # Lizard eats Paper and poisons Spock
                ("k", "s"),
                ("k", "r"),  # Spock smashes Scissors and vaporizes Rock
            },
        },
    ]


def select_challenge():
    challenges = get_challenges()
    print("Choose your challenge:")
    for idx, ch in enumerate(challenges):
        print(f"{idx + 1}: {ch['name']}")
    print("q: Quit")
    while True:
        sel = input("Enter your choice: ").strip().lower()
        if sel == "q":
            return None
        if sel.isdigit() and 1 <= int(sel) <= len(challenges):
            return challenges[int(sel) - 1]
        print("Invalid choice. Please select a valid challenge or 'q' to quit.")


def main():
    while True:
        challenge = select_challenge()
        if challenge is None:
            print("Goodbye!")
            break

        player_score = 0
        computer_score = 0
        ties = 0

        print(f"Starting challenge: {challenge['name']}")
        while True:
            player_choice = get_player_choice(challenge)
            if player_choice == "q":
                print("Exiting this challenge. Current scores:")
                print_score(player_score, computer_score, ties)
                print("-" * 20)
                break

            computer_choice = random.choice(challenge["options"])

            if player_choice == computer_choice:
                print("It's a tie!")
                ties += 1
            elif (player_choice, computer_choice) in challenge["winning_cases"]:
                print("You win!")
                player_score += 1
            else:
                print("You lose!")
                computer_score += 1

            print(
                f"You chose {get_full_choice(player_choice)} and the computer chose {get_full_choice(computer_choice)}."
            )
            print_score(player_score, computer_score, ties)
            print("-" * 20)


if __name__ == "__main__":
    main()
