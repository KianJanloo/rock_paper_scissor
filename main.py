import json
import random
import tkinter as tk
from pathlib import Path
from tkinter import font as tkfont
from tkinter import messagebox


CHOICE_EMOJI = {
    "r": "🪨",
    "p": "📄",
    "s": "✂️",
    "l": "🦎",
    "k": "🖖",
}

DEFAULT_EMOJIS = [
    "🪨",
    "📄",
    "✂️",
    "🦎",
    "🖖",
    "🔥",
    "💧",
    "🌪️",
    "⚡",
    "❄️",
    "🌙",
    "☀️",
    "⚔️",
    "🛡️",
    "🏹",
    "🪄",
]

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
    "danger": "#ef4444",
    "danger_hover": "#dc2626",
}

CUSTOM_RULES_PATH = Path(__file__).with_name("custom_rules.json")


def get_full_choice(short_choice, challenge=None):
    if challenge and "names" in challenge:
        return challenge["names"].get(short_choice, "unknown")
    choices = {"r": "rock", "p": "paper", "s": "scissors", "l": "lizard", "k": "spock"}
    return choices.get(short_choice, "unknown")


def choice_emoji(option, challenge=None):
    if challenge and "emojis" in challenge:
        return challenge["emojis"].get(option, CHOICE_EMOJI.get(option, "❔"))
    return CHOICE_EMOJI.get(option, "❔")


def get_builtin_challenges():
    return [
        {
            "name": "Classic",
            "subtitle": "Rock · Paper · Scissors",
            "options": ["r", "p", "s"],
            "names": {"r": "rock", "p": "paper", "s": "scissors"},
            "emojis": {"r": "🪨", "p": "📄", "s": "✂️"},
            "winning_cases": [["r", "s"], ["p", "r"], ["s", "p"]],
            "builtin": True,
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
            "emojis": {"r": "🪨", "p": "📄", "s": "✂️", "l": "🦎", "k": "🖖"},
            "winning_cases": [
                ["r", "s"],
                ["r", "l"],
                ["p", "r"],
                ["p", "k"],
                ["s", "p"],
                ["s", "l"],
                ["l", "p"],
                ["l", "k"],
                ["k", "s"],
                ["k", "r"],
            ],
            "builtin": True,
        },
    ]


def load_custom_challenges():
    if not CUSTOM_RULES_PATH.exists():
        return []
    try:
        with CUSTOM_RULES_PATH.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            return []
        challenges = []
        for item in data:
            normalized = normalize_challenge(item, builtin=False)
            if normalized:
                challenges.append(normalized)
        return challenges
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return []


def save_custom_challenges(challenges):
    payload = []
    for challenge in challenges:
        payload.append(
            {
                "name": challenge["name"],
                "subtitle": challenge.get("subtitle", ""),
                "options": list(challenge["options"]),
                "names": dict(challenge["names"]),
                "emojis": dict(challenge["emojis"]),
                "winning_cases": [list(pair) for pair in challenge["winning_cases"]],
            }
        )
    with CUSTOM_RULES_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def normalize_challenge(raw, builtin=False):
    try:
        name = str(raw["name"]).strip()
        options = [str(option) for option in raw["options"]]
        names = {str(key): str(value) for key, value in raw["names"].items()}
        emojis = {
            str(key): str(value)
            for key, value in raw.get("emojis", {}).items()
        }
        winning_cases = []
        for pair in raw["winning_cases"]:
            winner, loser = pair
            winning_cases.append([str(winner), str(loser)])
    except (KeyError, TypeError, ValueError):
        return None

    if not name or len(options) < 2:
        return None
    if any(option not in names for option in options):
        return None

    for option in options:
        emojis.setdefault(option, CHOICE_EMOJI.get(option, "❔"))

    subtitle = str(raw.get("subtitle") or " · ".join(names[o].title() for o in options))
    return {
        "name": name,
        "subtitle": subtitle,
        "options": options,
        "names": names,
        "emojis": emojis,
        "winning_cases": winning_cases,
        "builtin": builtin,
    }


def winning_set(challenge):
    return {tuple(pair) for pair in challenge["winning_cases"]}


def slugify_option(name, existing):
    base = "".join(ch.lower() if ch.isalnum() else "_" for ch in name.strip())
    base = base.strip("_") or "option"
    candidate = base
    index = 2
    while candidate in existing:
        candidate = f"{base}_{index}"
        index += 1
    return candidate


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
        self.geometry("780x620")
        self.minsize(700, 560)
        self.configure(bg=COLORS["bg"])
        self.resizable(True, True)

        self.title_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)
        self.heading_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.body_font = tkfont.Font(family="Segoe UI", size=12)
        self.score_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.emoji_font = tkfont.Font(family="Segoe UI Emoji", size=36)
        self.result_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.small_font = tkfont.Font(family="Segoe UI", size=10)

        self.challenge = None
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.custom_challenges = load_custom_challenges()
        self.editor_options = []
        self.editor_rules = []
        self.editing_index = None

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True, padx=24, pady=24)

        self.show_menu()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def all_challenges(self):
        return get_builtin_challenges() + self.custom_challenges

    def show_menu(self):
        self.clear_container()
        self.challenge = None
        self.editing_index = None

        header = tk.Frame(self.container, bg=COLORS["bg"])
        header.pack(fill="x", pady=(8, 20))

        tk.Label(
            header,
            text="Rock · Paper · Scissors",
            font=self.title_font,
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack()
        tk.Label(
            header,
            text="Pick a challenge, or create your own rules",
            font=self.subtitle_font,
            fg=COLORS["muted"],
            bg=COLORS["bg"],
        ).pack(pady=(8, 0))

        canvas_frame = tk.Frame(self.container, bg=COLORS["bg"])
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        cards = tk.Frame(canvas, bg=COLORS["bg"])

        cards.bind(
            "<Configure>",
            lambda _event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        window_id = canvas.create_window((0, 0), window=cards, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _resize_cards(event):
            canvas.itemconfigure(window_id, width=event.width)

        canvas.bind("<Configure>", _resize_cards)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        challenges = self.all_challenges()
        row = tk.Frame(cards, bg=COLORS["bg"])
        row.pack(fill="x", pady=4)

        for index, challenge in enumerate(challenges):
            if index and index % 3 == 0:
                row = tk.Frame(cards, bg=COLORS["bg"])
                row.pack(fill="x", pady=4)
            self._mode_card(row, challenge).pack(side="left", padx=10, pady=8)

        if challenges and len(challenges) % 3 == 0:
            row = tk.Frame(cards, bg=COLORS["bg"])
            row.pack(fill="x", pady=4)

        create_card = tk.Frame(row, bg=COLORS["panel"], padx=28, pady=28)
        create_card.pack(side="left", padx=10, pady=8)

        tk.Label(
            create_card,
            text="＋",
            font=self.emoji_font,
            fg=COLORS["accent"],
            bg=COLORS["panel"],
        ).pack(pady=(0, 16))
        tk.Label(
            create_card,
            text="Custom Rules",
            font=self.heading_font,
            fg=COLORS["text"],
            bg=COLORS["panel"],
        ).pack()
        tk.Label(
            create_card,
            text="Add any options and decide what beats what",
            font=self.subtitle_font,
            fg=COLORS["muted"],
            bg=COLORS["panel"],
            wraplength=220,
            justify="center",
        ).pack(pady=(6, 18))
        HoverButton(
            create_card,
            text="Create",
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
            command=self.show_rule_editor,
        ).pack()

        footer = tk.Frame(self.container, bg=COLORS["bg"])
        footer.pack(side="bottom", fill="x", pady=(16, 0))
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
        card = tk.Frame(parent, bg=COLORS["panel"], padx=24, pady=24)

        emoji_row = "  ".join(choice_emoji(c, challenge) for c in challenge["options"][:5])
        if len(challenge["options"]) > 5:
            emoji_row += " …"

        tk.Label(
            card,
            text=emoji_row,
            font=self.emoji_font,
            fg=COLORS["text"],
            bg=COLORS["panel"],
        ).pack(pady=(0, 12))

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
            wraplength=200,
            justify="center",
        ).pack(pady=(6, 14))

        actions = tk.Frame(card, bg=COLORS["panel"])
        actions.pack()

        HoverButton(
            actions,
            text="Play",
            font=self.body_font,
            fg=COLORS["bg"],
            bg=COLORS["accent"],
            hover_bg=COLORS["accent_dark"],
            activebackground=COLORS["accent_dark"],
            activeforeground=COLORS["bg"],
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=8,
            command=lambda c=challenge: self.start_challenge(c),
        ).pack(side="left", padx=(0, 6))

        if not challenge.get("builtin"):
            HoverButton(
                actions,
                text="Edit",
                font=self.small_font,
                fg=COLORS["text"],
                bg=COLORS["button"],
                activebackground=COLORS["button_hover"],
                activeforeground=COLORS["text"],
                relief="flat",
                cursor="hand2",
                padx=12,
                pady=8,
                command=lambda c=challenge: self.show_rule_editor(c),
            ).pack(side="left", padx=3)
            HoverButton(
                actions,
                text="Delete",
                font=self.small_font,
                fg=COLORS["text"],
                bg=COLORS["danger"],
                hover_bg=COLORS["danger_hover"],
                activebackground=COLORS["danger_hover"],
                activeforeground=COLORS["text"],
                relief="flat",
                cursor="hand2",
                padx=12,
                pady=8,
                command=lambda c=challenge: self.delete_custom_challenge(c),
            ).pack(side="left", padx=3)

        return card

    def delete_custom_challenge(self, challenge):
        if not messagebox.askyesno(
            "Delete rules",
            f'Delete custom mode "{challenge["name"]}"?',
        ):
            return
        self.custom_challenges = [
            item for item in self.custom_challenges if item["name"] != challenge["name"]
        ]
        save_custom_challenges(self.custom_challenges)
        self.show_menu()

    def show_rule_editor(self, challenge=None):
        self.clear_container()
        self.editing_index = None

        if challenge and not challenge.get("builtin"):
            for index, item in enumerate(self.custom_challenges):
                if item["name"] == challenge["name"]:
                    self.editing_index = index
                    break
            self.editor_options = [
                {
                    "id": option,
                    "name": challenge["names"][option],
                    "emoji": choice_emoji(option, challenge),
                }
                for option in challenge["options"]
            ]
            self.editor_rules = [list(pair) for pair in challenge["winning_cases"]]
            title = "Edit Custom Rules"
            default_name = challenge["name"]
        else:
            self.editor_options = [
                {"id": "rock", "name": "rock", "emoji": "🪨"},
                {"id": "paper", "name": "paper", "emoji": "📄"},
                {"id": "scissors", "name": "scissors", "emoji": "✂️"},
            ]
            self.editor_rules = [["rock", "scissors"], ["paper", "rock"], ["scissors", "paper"]]
            title = "Create Custom Rules"
            default_name = ""

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
            text=title,
            font=self.heading_font,
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(side="left", padx=16)

        form = tk.Frame(self.container, bg=COLORS["panel"], padx=20, pady=18)
        form.pack(fill="both", expand=True, pady=16)

        name_row = tk.Frame(form, bg=COLORS["panel"])
        name_row.pack(fill="x", pady=(0, 12))
        tk.Label(
            name_row,
            text="Mode name",
            font=self.body_font,
            fg=COLORS["muted"],
            bg=COLORS["panel"],
        ).pack(anchor="w")
        self.name_var = tk.StringVar(value=default_name)
        name_entry = tk.Entry(
            name_row,
            textvariable=self.name_var,
            font=self.body_font,
            bg=COLORS["button"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
        )
        name_entry.pack(fill="x", pady=(6, 0), ipady=8)

        columns = tk.Frame(form, bg=COLORS["panel"])
        columns.pack(fill="both", expand=True)

        left = tk.Frame(columns, bg=COLORS["panel"])
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = tk.Frame(columns, bg=COLORS["panel"])
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))

        tk.Label(
            left,
            text="Options",
            font=self.heading_font,
            fg=COLORS["text"],
            bg=COLORS["panel"],
        ).pack(anchor="w")
        tk.Label(
            left,
            text="Add any choices you want in this mode",
            font=self.small_font,
            fg=COLORS["muted"],
            bg=COLORS["panel"],
        ).pack(anchor="w", pady=(2, 8))

        self.options_frame = tk.Frame(left, bg=COLORS["panel"])
        self.options_frame.pack(fill="both", expand=True)

        add_option_row = tk.Frame(left, bg=COLORS["panel"])
        add_option_row.pack(fill="x", pady=(8, 0))
        self.option_name_var = tk.StringVar()
        self.option_emoji_var = tk.StringVar(value=DEFAULT_EMOJIS[0])
        tk.Entry(
            add_option_row,
            textvariable=self.option_name_var,
            font=self.body_font,
            bg=COLORS["button"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            width=16,
        ).pack(side="left", ipady=6)
        emoji_menu = tk.OptionMenu(add_option_row, self.option_emoji_var, *DEFAULT_EMOJIS)
        emoji_menu.configure(
            font=self.body_font,
            bg=COLORS["button"],
            fg=COLORS["text"],
            activebackground=COLORS["button_hover"],
            activeforeground=COLORS["text"],
            highlightthickness=0,
            relief="flat",
        )
        emoji_menu["menu"].configure(bg=COLORS["panel"], fg=COLORS["text"])
        emoji_menu.pack(side="left", padx=6)
        HoverButton(
            add_option_row,
            text="Add option",
            font=self.small_font,
            fg=COLORS["bg"],
            bg=COLORS["accent"],
            hover_bg=COLORS["accent_dark"],
            activebackground=COLORS["accent_dark"],
            activeforeground=COLORS["bg"],
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self._add_editor_option,
        ).pack(side="left")

        tk.Label(
            right,
            text="Winning rules",
            font=self.heading_font,
            fg=COLORS["text"],
            bg=COLORS["panel"],
        ).pack(anchor="w")
        tk.Label(
            right,
            text="Pick what beats what — any matchups you want",
            font=self.small_font,
            fg=COLORS["muted"],
            bg=COLORS["panel"],
        ).pack(anchor="w", pady=(2, 8))

        self.rules_frame = tk.Frame(right, bg=COLORS["panel"])
        self.rules_frame.pack(fill="both", expand=True)

        add_rule_row = tk.Frame(right, bg=COLORS["panel"])
        add_rule_row.pack(fill="x", pady=(8, 0))
        self.winner_var = tk.StringVar()
        self.loser_var = tk.StringVar()
        self.winner_menu = tk.OptionMenu(add_rule_row, self.winner_var, "")
        self.loser_menu = tk.OptionMenu(add_rule_row, self.loser_var, "")
        for menu in (self.winner_menu, self.loser_menu):
            menu.configure(
                font=self.body_font,
                bg=COLORS["button"],
                fg=COLORS["text"],
                activebackground=COLORS["button_hover"],
                activeforeground=COLORS["text"],
                highlightthickness=0,
                relief="flat",
                width=12,
            )
            menu["menu"].configure(bg=COLORS["panel"], fg=COLORS["text"])
        self.winner_menu.pack(side="left", padx=(0, 6))
        tk.Label(
            add_rule_row,
            text="beats",
            font=self.body_font,
            fg=COLORS["muted"],
            bg=COLORS["panel"],
        ).pack(side="left", padx=(0, 6))
        self.loser_menu.pack(side="left", padx=(0, 6))
        HoverButton(
            add_rule_row,
            text="Add rule",
            font=self.small_font,
            fg=COLORS["bg"],
            bg=COLORS["accent"],
            hover_bg=COLORS["accent_dark"],
            activebackground=COLORS["accent_dark"],
            activeforeground=COLORS["bg"],
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self._add_editor_rule,
        ).pack(side="left")

        footer = tk.Frame(self.container, bg=COLORS["bg"])
        footer.pack(fill="x")
        HoverButton(
            footer,
            text="Save & Play",
            font=self.body_font,
            fg=COLORS["bg"],
            bg=COLORS["accent"],
            hover_bg=COLORS["accent_dark"],
            activebackground=COLORS["accent_dark"],
            activeforeground=COLORS["bg"],
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: self._save_editor(play=True),
        ).pack(side="right")
        HoverButton(
            footer,
            text="Save",
            font=self.body_font,
            fg=COLORS["text"],
            bg=COLORS["button"],
            activebackground=COLORS["button_hover"],
            activeforeground=COLORS["text"],
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: self._save_editor(play=False),
        ).pack(side="right", padx=(0, 8))

        self._refresh_editor_lists()

    def _refresh_editor_lists(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        for widget in self.rules_frame.winfo_children():
            widget.destroy()

        if not self.editor_options:
            tk.Label(
                self.options_frame,
                text="No options yet",
                font=self.small_font,
                fg=COLORS["muted"],
                bg=COLORS["panel"],
            ).pack(anchor="w")
        else:
            for option in self.editor_options:
                row = tk.Frame(self.options_frame, bg=COLORS["button"], padx=10, pady=6)
                row.pack(fill="x", pady=3)
                tk.Label(
                    row,
                    text=f'{option["emoji"]}  {option["name"].title()}',
                    font=self.body_font,
                    fg=COLORS["text"],
                    bg=COLORS["button"],
                ).pack(side="left")
                HoverButton(
                    row,
                    text="Remove",
                    font=self.small_font,
                    fg=COLORS["text"],
                    bg=COLORS["danger"],
                    hover_bg=COLORS["danger_hover"],
                    activebackground=COLORS["danger_hover"],
                    activeforeground=COLORS["text"],
                    relief="flat",
                    cursor="hand2",
                    padx=8,
                    pady=2,
                    command=lambda option_id=option["id"]: self._remove_editor_option(option_id),
                ).pack(side="right")

        labels = {option["id"]: f'{option["emoji"]} {option["name"].title()}' for option in self.editor_options}
        option_ids = [option["id"] for option in self.editor_options]

        if not self.editor_rules:
            tk.Label(
                self.rules_frame,
                text="No winning rules yet",
                font=self.small_font,
                fg=COLORS["muted"],
                bg=COLORS["panel"],
            ).pack(anchor="w")
        else:
            for index, (winner, loser) in enumerate(self.editor_rules):
                row = tk.Frame(self.rules_frame, bg=COLORS["button"], padx=10, pady=6)
                row.pack(fill="x", pady=3)
                text = f'{labels.get(winner, winner)} beats {labels.get(loser, loser)}'
                tk.Label(
                    row,
                    text=text,
                    font=self.body_font,
                    fg=COLORS["text"],
                    bg=COLORS["button"],
                ).pack(side="left")
                HoverButton(
                    row,
                    text="Remove",
                    font=self.small_font,
                    fg=COLORS["text"],
                    bg=COLORS["danger"],
                    hover_bg=COLORS["danger_hover"],
                    activebackground=COLORS["danger_hover"],
                    activeforeground=COLORS["text"],
                    relief="flat",
                    cursor="hand2",
                    padx=8,
                    pady=2,
                    command=lambda i=index: self._remove_editor_rule(i),
                ).pack(side="right")

        self._rebuild_option_menus(option_ids, labels)

    def _rebuild_option_menus(self, option_ids, labels):
        for menu_widget, var in (
            (self.winner_menu, self.winner_var),
            (self.loser_menu, self.loser_var),
        ):
            menu = menu_widget["menu"]
            menu.delete(0, "end")
            if not option_ids:
                var.set("")
                continue
            for option_id in option_ids:
                menu.add_command(
                    label=labels[option_id],
                    command=lambda value=option_id, current=var: current.set(value),
                )
            if var.get() not in option_ids:
                var.set(option_ids[0])

    def _add_editor_option(self):
        name = self.option_name_var.get().strip()
        emoji = self.option_emoji_var.get().strip() or "❔"
        if not name:
            messagebox.showwarning("Missing name", "Enter a name for the option.")
            return
        if any(option["name"].lower() == name.lower() for option in self.editor_options):
            messagebox.showwarning("Duplicate option", "That option already exists.")
            return

        option_id = slugify_option(name, {option["id"] for option in self.editor_options})
        self.editor_options.append({"id": option_id, "name": name.lower(), "emoji": emoji})
        self.option_name_var.set("")
        next_emoji = DEFAULT_EMOJIS[len(self.editor_options) % len(DEFAULT_EMOJIS)]
        self.option_emoji_var.set(next_emoji)
        self._refresh_editor_lists()

    def _remove_editor_option(self, option_id):
        self.editor_options = [option for option in self.editor_options if option["id"] != option_id]
        self.editor_rules = [
            pair for pair in self.editor_rules if option_id not in pair
        ]
        self._refresh_editor_lists()

    def _add_editor_rule(self):
        winner = self.winner_var.get()
        loser = self.loser_var.get()
        if not winner or not loser:
            messagebox.showwarning("Missing options", "Add at least two options first.")
            return
        if winner == loser:
            messagebox.showwarning("Invalid rule", "An option cannot beat itself.")
            return
        if [winner, loser] in self.editor_rules:
            messagebox.showwarning("Duplicate rule", "That winning rule already exists.")
            return
        self.editor_rules.append([winner, loser])
        self._refresh_editor_lists()

    def _remove_editor_rule(self, index):
        if 0 <= index < len(self.editor_rules):
            del self.editor_rules[index]
            self._refresh_editor_lists()

    def _save_editor(self, play=False):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Give your custom mode a name.")
            return
        if len(self.editor_options) < 2:
            messagebox.showwarning("Need options", "Add at least two options.")
            return
        if not self.editor_rules:
            messagebox.showwarning("Need rules", "Add at least one winning rule.")
            return

        for index, existing in enumerate(self.custom_challenges):
            if existing["name"].lower() == name.lower() and index != self.editing_index:
                messagebox.showwarning(
                    "Name taken",
                    "Another custom mode already uses that name.",
                )
                return

        challenge = {
            "name": name,
            "subtitle": " · ".join(option["name"].title() for option in self.editor_options),
            "options": [option["id"] for option in self.editor_options],
            "names": {option["id"]: option["name"] for option in self.editor_options},
            "emojis": {option["id"]: option["emoji"] for option in self.editor_options},
            "winning_cases": [list(pair) for pair in self.editor_rules],
            "builtin": False,
        }

        if self.editing_index is None:
            self.custom_challenges.append(challenge)
            self.editing_index = len(self.custom_challenges) - 1
        else:
            self.custom_challenges[self.editing_index] = challenge

        save_custom_challenges(self.custom_challenges)

        if play:
            self.start_challenge(challenge)
        else:
            messagebox.showinfo("Saved", f'Custom rules "{name}" saved.')
            self.show_menu()

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

        if not self.challenge.get("builtin"):
            HoverButton(
                top,
                text="Edit Rules",
                font=self.small_font,
                fg=COLORS["text"],
                bg=COLORS["button"],
                activebackground=COLORS["button_hover"],
                activeforeground=COLORS["text"],
                relief="flat",
                cursor="hand2",
                padx=10,
                pady=6,
                command=lambda: self.show_rule_editor(self.challenge),
            ).pack(side="left")

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
                text=f"{choice_emoji(option, self.challenge)}\n{name.title()}",
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

        self.player_emoji.config(text=choice_emoji(player_choice, self.challenge))
        self.computer_emoji.config(text=choice_emoji(computer_choice, self.challenge))
        self.player_name.config(
            text=get_full_choice(player_choice, self.challenge).title()
        )
        self.computer_name.config(
            text=get_full_choice(computer_choice, self.challenge).title()
        )

        if player_choice == computer_choice:
            self.ties += 1
            self.result_label.config(text="It's a tie!", fg=COLORS["tie"])
        elif (player_choice, computer_choice) in winning_set(self.challenge):
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
