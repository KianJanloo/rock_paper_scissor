import random
import tkinter as tk
from tkinter import font as tkfont


CHOICE_EMOJI = {
    "r": "🪨",
    "p": "📄",
    "s": "✂️",
    "l": "🦎",
    "k": "🖖",
}

COLORS = {
    "bg": "#0f172a",
    "panel": "#1e293b",
    "accent": "#38bdf8",
    "accent_dark": "#0ea5e9",
    "win": "#4ade80",
    "lose": "#f87171",
    "tie": "#fbbf24",
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "button": "#334155",
    "button_hover": "#475569",
}


def get_full_choice(short_choice):
    choices = {"r": "rock", "p": "paper", "s": "scissors", "l": "lizard", "k": "spock"}
    return choices.get(short_choice, "unknown")


def get_challenges():
    return [
        {
            "name": "Classic",
            "subtitle": "Rock · Paper · Scissors",
            "options": ["r", "p", "s"],
            "names": {"r": "rock", "p": "paper", "s": "scissors"},
            "winning_cases": {("r", "s"), ("p", "r"), ("s", "p")},
        },
        {
            "name": "Lizard Spock",
            "subtitle": "Rock · Paper · Scissors · Lizard · Spock",
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
                ("r", "l"),
                ("p", "r"),
                ("p", "k"),
                ("s", "p"),
                ("s", "l"),
                ("l", "p"),
                ("l", "k"),
                ("k", "s"),
                ("k", "r"),
            },
        },
    ]


class HoverButton(tk.Button):
    def __init__(self, master, hover_bg=None, **kwargs):
        self.default_bg = kwargs.get("bg", COLORS["button"])
        self.hover_bg = hover_bg or COLORS["button_hover"]
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event):
        if self["state"] != "disabled":
            self.configure(bg=self.hover_bg)

    def _on_leave(self, _event):
        if self["state"] != "disabled":
            self.configure(bg=self.default_bg)


class RPSGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock · Paper · Scissors")
        self.geometry("720x560")
        self.minsize(640, 500)
        self.configure(bg=COLORS["bg"])
        self.resizable(True, True)

        self.title_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)
        self.heading_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.body_font = tkfont.Font(family="Segoe UI", size=12)
        self.score_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.emoji_font = tkfont.Font(family="Segoe UI Emoji", size=36)
        self.result_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")

        self.challenge = None
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True, padx=24, pady=24)

        self.show_menu()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear_container()
        self.challenge = None

        header = tk.Frame(self.container, bg=COLORS["bg"])
        header.pack(fill="x", pady=(20, 40))

        tk.Label(
            header,
            text="Rock · Paper · Scissors",
            font=self.title_font,
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack()
        tk.Label(
            header,
            text="Pick a challenge and outsmart the computer",
            font=self.subtitle_font,
            fg=COLORS["muted"],
            bg=COLORS["bg"],
        ).pack(pady=(8, 0))

        cards = tk.Frame(self.container, bg=COLORS["bg"])
        cards.pack(expand=True)

        for challenge in get_challenges():
            self._mode_card(cards, challenge).pack(side="left", padx=12, pady=8)

        footer = tk.Frame(self.container, bg=COLORS["bg"])
        footer.pack(side="bottom", fill="x", pady=(20, 0))
        HoverButton(
            footer,
            text="Quit",
            font=self.body_font,
            fg=COLORS["text"],
            bg=COLORS["button"],
            activebackground=COLORS["button_hover"],
            activeforeground=COLORS["text"],
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.destroy,
        ).pack(side="right")

    def _mode_card(self, parent, challenge):
        card = tk.Frame(parent, bg=COLORS["panel"], padx=28, pady=28)

        emoji_row = "  ".join(CHOICE_EMOJI[c] for c in challenge["options"])
        tk.Label(
            card,
            text=emoji_row,
            font=self.emoji_font,
            fg=COLORS["text"],
            bg=COLORS["panel"],
        ).pack(pady=(0, 16))

        tk.Label(
            card,
            text=challenge["name"],
            font=self.heading_font,
            fg=COLORS["text"],
            bg=COLORS["panel"],
        ).pack()
        tk.Label(
            card,
            text=challenge["subtitle"],
            font=self.subtitle_font,
            fg=COLORS["muted"],
            bg=COLORS["panel"],
            wraplength=220,
            justify="center",
        ).pack(pady=(6, 18))

        HoverButton(
            card,
            text="Play",
            font=self.body_font,
            fg=COLORS["bg"],
            bg=COLORS["accent"],
            hover_bg=COLORS["accent_dark"],
            activebackground=COLORS["accent_dark"],
            activeforeground=COLORS["bg"],
            relief="flat",
            cursor="hand2",
            padx=28,
            pady=10,
            command=lambda c=challenge: self.start_challenge(c),
        ).pack()

        return card

    def start_challenge(self, challenge):
        self.challenge = challenge
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.show_game()

    def show_game(self):
        self.clear_container()

        top = tk.Frame(self.container, bg=COLORS["bg"])
        top.pack(fill="x")

        HoverButton(
            top,
            text="← Menu",
            font=self.body_font,
            fg=COLORS["text"],
            bg=COLORS["button"],
            activebackground=COLORS["button_hover"],
            activeforeground=COLORS["text"],
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=6,
            command=self.show_menu,
        ).pack(side="left")

        tk.Label(
            top,
            text=self.challenge["name"],
            font=self.heading_font,
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(side="left", padx=16)

        self.score_label = tk.Label(
            top,
            text=self._score_text(),
            font=self.score_font,
            fg=COLORS["accent"],
            bg=COLORS["bg"],
        )
        self.score_label.pack(side="right")

        arena = tk.Frame(self.container, bg=COLORS["panel"], padx=24, pady=28)
        arena.pack(fill="both", expand=True, pady=20)

        sides = tk.Frame(arena, bg=COLORS["panel"])
        sides.pack(fill="x", pady=(0, 16))

        player_box = tk.Frame(sides, bg=COLORS["panel"])
        player_box.pack(side="left", expand=True)
        tk.Label(
            player_box,
            text="YOU",
            font=self.subtitle_font,
            fg=COLORS["muted"],
            bg=COLORS["panel"],
        ).pack()
        self.player_emoji = tk.Label(
            player_box,
            text="❔",
            font=self.emoji_font,
            fg=COLORS["text"],
            bg=COLORS["panel"],
        )
        self.player_emoji.pack(pady=8)
        self.player_name = tk.Label(
            player_box,
            text="—",
            font=self.body_font,
            fg=COLORS["muted"],
            bg=COLORS["panel"],
        )
        self.player_name.pack()

        vs = tk.Label(
            sides,
            text="VS",
            font=self.heading_font,
            fg=COLORS["accent"],
            bg=COLORS["panel"],
        )
        vs.pack(side="left", padx=20)

        computer_box = tk.Frame(sides, bg=COLORS["panel"])
        computer_box.pack(side="left", expand=True)
        tk.Label(
            computer_box,
            text="COMPUTER",
            font=self.subtitle_font,
            fg=COLORS["muted"],
            bg=COLORS["panel"],
        ).pack()
        self.computer_emoji = tk.Label(
            computer_box,
            text="❔",
            font=self.emoji_font,
            fg=COLORS["text"],
            bg=COLORS["panel"],
        )
        self.computer_emoji.pack(pady=8)
        self.computer_name = tk.Label(
            computer_box,
            text="—",
            font=self.body_font,
            fg=COLORS["muted"],
            bg=COLORS["panel"],
        )
        self.computer_name.pack()

        self.result_label = tk.Label(
            arena,
            text="Make your move",
            font=self.result_font,
            fg=COLORS["text"],
            bg=COLORS["panel"],
        )
        self.result_label.pack(pady=(8, 20))

        choices = tk.Frame(self.container, bg=COLORS["bg"])
        choices.pack(pady=(0, 8))

        for option in self.challenge["options"]:
            name = self.challenge["names"][option]
            btn = HoverButton(
                choices,
                text=f"{CHOICE_EMOJI[option]}\n{name.title()}",
                font=self.body_font,
                fg=COLORS["text"],
                bg=COLORS["button"],
                activebackground=COLORS["button_hover"],
                activeforeground=COLORS["text"],
                relief="flat",
                cursor="hand2",
                width=10,
                height=3,
                justify="center",
                command=lambda o=option: self.play_round(o),
            )
            btn.pack(side="left", padx=8)

    def _score_text(self):
        return (
            f"You {self.player_score}  ·  "
            f"CPU {self.computer_score}  ·  "
            f"Ties {self.ties}"
        )

    def play_round(self, player_choice):
        computer_choice = random.choice(self.challenge["options"])

        self.player_emoji.config(text=CHOICE_EMOJI[player_choice])
        self.computer_emoji.config(text=CHOICE_EMOJI[computer_choice])
        self.player_name.config(text=get_full_choice(player_choice).title())
        self.computer_name.config(text=get_full_choice(computer_choice).title())

        if player_choice == computer_choice:
            self.ties += 1
            self.result_label.config(text="It's a tie!", fg=COLORS["tie"])
        elif (player_choice, computer_choice) in self.challenge["winning_cases"]:
            self.player_score += 1
            self.result_label.config(text="You win!", fg=COLORS["win"])
        else:
            self.computer_score += 1
            self.result_label.config(text="You lose!", fg=COLORS["lose"])

        self.score_label.config(text=self._score_text())


def main():
    app = RPSGame()
    app.mainloop()


if __name__ == "__main__":
    main()
