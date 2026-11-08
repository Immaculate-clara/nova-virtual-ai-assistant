"""Greeting and name capture (FR-01, FR-02)."""
import re

NAME_MAX = 30  # keep names short so responses stay tidy
# Lets "my name is Priya" or "I'm Priya" work as a name answer.
_PREFIX = re.compile(r"^(?:my name is|call me|i am|i'm|it's)\s+", re.I)


def clean_name(text):
    """Strip filler words and spaces, Title-Case the name, fall back to 'Friend'."""
    return _PREFIX.sub("", text.strip()).strip().title()[:NAME_MAX] or "Friend"


def get_user_name(ask=input, say=print):
    """Introduce the assistant, ask for the name and return it (stored by main)."""
    say("Hi! I'm Nova. What's your name?")
    return clean_name(ask())


def build_greeting(name):
    """Welcome line shown right after the name is captured."""
    return f"Nice to meet you, {name}! Type 'help' to see what I can do."
