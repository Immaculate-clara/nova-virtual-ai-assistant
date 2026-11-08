"""Nova - Virtual AI Assistant: entry point and main loop.

Cycle (PRD s15/s16): input -> normalize -> keyword match -> respond -> loop.
Run:  python main.py
"""
import re

import ai_concepts
import calculator
import content
import datetime_utils
import game
import greetings
import help_menu

# Keyword detection (AI: intent recognition). Each intent has trigger words; the
# intent sharing the most words with the user's text wins. This overlap count is
# a tiny "similarity score" (ML analogy). Ties go to the earlier intent.
INTENTS = {
    "exit": {"exit", "quit", "bye", "goodbye"},
    "greeting": {"hello", "hi", "hey"},
    "time": {"time", "clock"},
    "date": {"date", "day", "today"},
    "calculate": {"calc", "calculate", "calculator", "math", "plus", "minus", "times"},
    "joke": {"joke", "jokes", "funny", "laugh"},
    "quote": {"quote", "quotes", "motivate", "motivation", "motivational", "inspire"},
    "fact": {"fact", "facts"},
    "game": {"game", "guess", "play"},
    "recommend": {"recommend", "recommendation", "suggest", "activity"},
    "perceptron": {"perceptron", "neuron"},
    "concepts": {"concepts", "explain"},
    "help": {"help", "commands", "menu"},
}
_WORD = re.compile(r"[a-z']+")
_RENAME = re.compile(r"\b(?:call me|my name is)\s+([a-z']+(?: [a-z']+)?)$")

BANNER = "=" * 43 + "\n        NOVA - VIRTUAL AI ASSISTANT\n" + "=" * 43
FALLBACK = "I'm not sure I understood that — type 'help' to see what I can do."


def say(text):
    """Print as the assistant; continuation lines are indented under the label."""
    print("Assistant: " + text.replace("\n", "\n           "))


def ask():
    return input("\nYou: ")


def classify(text):
    """Normalized text -> intent name ('fallback' if nothing matches)."""
    words = set(_WORD.findall(text))
    best, best_score = "fallback", 0
    for intent, keys in INTENTS.items():
        score = len(words & keys)
        if score > best_score:
            best, best_score = intent, score
    if best == "fallback" and calculator.parse_expression(text):
        return "calculate"  # bare "12 + 8" works without the word 'calculate'
    return best


# One respond_* function per intent (PRD s16). `n` is the user's name.
def respond_greeting(n, t): say(f"Hello, {n}! How can I help you today?")
def respond_time(n, t): say(datetime_utils.get_current_time())
def respond_date(n, t): say(datetime_utils.get_current_date())
def respond_calculator(n, t): say(calculator.calculate(t))
def respond_quote(n, t): say(f"Sure thing, {n}! {content.get_random_quote()}")
def respond_joke(n, t): say(f"Sure thing, {n}! {content.get_random_joke()}")
def respond_fact(n, t): say(f"Sure thing, {n}! {content.get_random_fact()}")
def respond_game(n, t): game.play_guessing_game(ask, say)
def respond_recommend(n, t): say(f"Hey {n}! {ai_concepts.recommend_activity()}")
def respond_perceptron(n, t): ai_concepts.perceptron_demo(ask, say)
def respond_concepts(n, t): say(ai_concepts.explain_concepts())
def respond_help(n, t): help_menu.print_help(say)
def respond_fallback(n, t): say(FALLBACK)


HANDLERS = {
    "greeting": respond_greeting, "time": respond_time, "date": respond_date,
    "calculate": respond_calculator, "quote": respond_quote, "joke": respond_joke,
    "fact": respond_fact, "game": respond_game, "recommend": respond_recommend,
    "perceptron": respond_perceptron, "concepts": respond_concepts,
    "help": respond_help, "fallback": respond_fallback,
}


def run():
    print(BANNER)
    name = greetings.get_user_name(ask, say)        # session state: just the name
    say(greetings.build_greeting(name))
    while True:
        text = ask().strip().lower()                # normalize
        rename = _RENAME.search(text)               # "learns" a preference mid-session
        if rename:
            name = greetings.clean_name(rename.group(1))
            say(f"Got it! I'll call you {name} from now on.")
            continue
        intent = classify(text)
        if intent == "exit":
            break
        try:
            HANDLERS[intent](name, text)
        except Exception:                           # one bad command must not end the session
            say("Oops, something went wrong with that one. Please try again.")
    say(f"Goodbye, {name}! Have a great day.")
    print(BANNER)


def main():
    try:
        run()
    except (KeyboardInterrupt, EOFError):           # Ctrl+C / Ctrl+D / closed input
        print("\nAssistant: Goodbye! Have a great day.")


if __name__ == "__main__":
    main()
