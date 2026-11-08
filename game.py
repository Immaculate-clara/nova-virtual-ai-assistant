"""Number guessing game with a limited number of attempts (FR-09)."""
import random

LOW, HIGH = 1, 20   # secret number range
MAX_TRIES = 5       # attempt limit
_QUIT = {"exit", "quit", "stop", "cancel"}


def play_guessing_game(ask=input, say=print, secret=None):
    """Play one round. Returns True (won), False (lost) or None (cancelled).

    Invalid guesses do not use up a try. `secret` is only for testing.
    """
    secret = secret or random.randint(LOW, HIGH)
    say(f"I'm thinking of a number between {LOW} and {HIGH}. "
        f"You have {MAX_TRIES} tries. Guess a number:")
    tries = MAX_TRIES
    while tries:
        raw = ask().strip().lower()
        if raw in _QUIT:
            say(f"Game cancelled. The number was {secret}.")
            return None
        try:
            guess = int(raw)
        except ValueError:
            say(f"Please enter a whole number between {LOW} and {HIGH}.")
            continue
        if not LOW <= guess <= HIGH:
            say(f"Pick a number between {LOW} and {HIGH}.")
            continue
        tries -= 1
        if guess == secret:
            say(f"You got it! The number was {secret}. You win!")
            return True
        if tries:
            say(f"Go {'higher' if guess < secret else 'lower'}! "
                f"({tries} {'try' if tries == 1 else 'tries'} left)")
    say(f"Out of tries! The number was {secret}. You lose.")
    return False
