"""Predefined quotes, jokes and facts with random selection (FR-06/07/08)."""
import random

QUOTES = [
    "The only way to do great work is to love what you do.",
    "Believe you can and you're halfway there.",
    "Small steps every day lead to big results.",
    "Don't watch the clock; do what it does. Keep going.",
    "Your limitation is only your imagination.",
    "Dream big, start small, act now.",
    "Mistakes are proof that you are trying.",
    "Progress, not perfection.",
    "Done is better than perfect.",
    "Every expert was once a beginner.",
]
JOKES = [
    "Why did the developer go broke? Because they used up all their cache.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "There are 10 types of people: those who understand binary and those who don't.",
    "Why was the computer cold? It left its Windows open.",
    "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
    "Why did the Python programmer wear glasses? Because they couldn't C.",
    "Why did the neural network go to school? To improve its layers.",
    "I'd tell you a UDP joke, but you might not get it.",
    "Why was the function sad? It didn't get any arguments.",
    "What's a computer's favourite snack? Microchips.",
]
FACTS = [
    "The term 'Artificial Intelligence' was coined in 1956 at the Dartmouth Conference.",
    "The first computer bug was a real moth found in a Harvard Mark II relay in 1947.",
    "Python is named after Monty Python, not the snake.",
    "The first perceptron was introduced by Frank Rosenblatt in 1958.",
    "Honey never spoils; edible honey was found in ancient Egyptian tombs.",
    "A day on Venus is longer than a year on Venus.",
    "The first 1 GB hard drive (1980) weighed over 200 kg.",
    "ELIZA, a rule-based chatbot, was written at MIT in 1966.",
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries are not.",
]
_last = {}  # last item served per list, so the same one never repeats back-to-back


def _pick(items):
    """random.choice, but never the item we returned last time."""
    options = [i for i in items if i != _last.get(id(items))] or items
    _last[id(items)] = choice = random.choice(options)
    return choice


def get_random_quote(): return _pick(QUOTES)
def get_random_joke(): return _pick(JOKES)
def get_random_fact(): return _pick(FACTS)
