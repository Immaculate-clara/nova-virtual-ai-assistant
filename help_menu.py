"""Help menu listing every supported command (FR-10)."""
COMMANDS = [
    ("time", "show current time"),
    ("date", "show current date"),
    ("calculate", "do a calculation, e.g. calculate 12 + 8"),
    ("joke", "tell a joke"),
    ("quote", "motivational quote"),
    ("fact", "random fact"),
    ("game", "play number guessing game"),
    ("recommend", "rule-based activity suggestion"),
    ("perceptron", "neuron demo (deep learning idea)"),
    ("concepts", "where AI/ML/DL ideas live in my code"),
    ("call me <name>", "change the name I use for you"),
    ("help", "show this menu"),
    ("exit", "quit the assistant (also: quit, bye)"),
]


def help_text():
    """Formatted command list (one line per command)."""
    return "Here's what I can do:\n" + "\n".join(f"  - {c:<15} {d}" for c, d in COMMANDS)


def print_help(say=print):
    say(help_text())
