# Rock, Paper, Scissors (and Friends!) - Python CLI Game

This is a simple command-line implementation of the classic game Rock, Paper, Scissors, as well as the extended Rock, Paper, Scissors, Lizard, Spock variant.

## Features

- **Two Game Modes:**
  - Classic Rock, Paper, Scissors
  - Rock, Paper, Scissors, Lizard, Spock
- Scores tracked for player, computer, and ties
- Easy text-based interface
- Quit at any time

## Getting Started

### Prerequisites

- Python 3.x

### Running the Game

1. Clone or download this repository.
2. Open your terminal or command prompt.
3. Navigate to the project directory.
4. Run the game:

```bash
python main.py
```

## How to Play

1. When the game starts, you'll be prompted to choose a challenge:
    - Enter the number corresponding to your preferred game mode.
    - Enter `q` at any menu to quit.

2. For each round:
    - Enter the code for your choice as shown in the prompt (e.g., `r` for rock, `k` for spock, etc.).
    - Results and updated scores are displayed after each round.

3. Quit at any time by entering `q`.

## Example Gameplay

```
Choose your challenge:
1: Classic Rock, Paper, Scissors
2: Rock, Paper, Scissors, Lizard, Spock
q: Quit
Enter your choice: 2
Starting challenge: Rock, Paper, Scissors, Lizard, Spock
Enter your choice (r: rock, p: paper, s: scissors, l: lizard, k: spock, q: quit): r
You win!
You chose rock and the computer chose scissors.
Score - You: 1, Computer: 0, Ties: 0
--------------------
```

## Game Rules

- **Classic Version:**  
  - Rock beats Scissors  
  - Paper beats Rock  
  - Scissors beats Paper  

- **Lizard Spock Variant:**  
  - Rock crushes Scissors & Lizard  
  - Paper covers Rock & disproves Spock  
  - Scissors cuts Paper & decapitates Lizard  
  - Lizard eats Paper & poisons Spock  
  - Spock smashes Scissors & vaporizes Rock  

## License

MIT License. See [LICENSE](LICENSE) file for details.

## Acknowledgements

Inspired by the [Big Bang Theory's](https://bigbangtheory.fandom.com/wiki/Rock,_Paper,_Scissors,_Lizard,_Spock) variant.

Enjoy the game!