# Rock, Paper, Scissors (and Friends!) — Python GUI Game

A desktop UI for classic Rock, Paper, Scissors and the Rock, Paper, Scissors, Lizard, Spock variant. Built with Python and tkinter (no extra packages).

## Features

- **Built-in game modes**
  - Classic Rock, Paper, Scissors
  - Rock, Paper, Scissors, Lizard, Spock
- **Custom rules** — create your own modes with any options and winning matchups
- Clickable emoji choice buttons
- Live scoreboard (you / computer / ties)
- Color-coded win / lose / tie results
- Menu to switch modes anytime
- Custom modes are saved in `custom_rules.json`

## Getting Started

### Prerequisites

- Python 3.x (tkinter is included with standard Python)

### Running the Game

```bash
python main.py
```

## How to Play

1. Choose **Classic**, **Lizard Spock**, or a saved custom mode on the menu.
2. Or click **Create** under Custom Rules to add your own options and “X beats Y” rules.
3. Click a choice button each round.
4. Watch the arena update with both moves, the result, and the score.
5. Use **← Menu** to change mode, or **Quit** to exit.

### Custom Rules

1. Open **Custom Rules → Create** (or **Edit** on a saved mode).
2. Name the mode.
3. Add options (name + emoji).
4. Add winning rules such as “Fire beats Ice”.
5. **Save** to keep it on the menu, or **Save & Play** to jump straight in.
6. Custom modes can be edited or deleted from the menu anytime.

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