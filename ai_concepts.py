"""AI / ML / DL concept demos, all plain Python with no training (FR-13, FR-14)."""
from datetime import datetime
from math import isfinite

# ---------------------------------------------------------------------------
# FR-13  Rule-based decision  (AI: rule-based system, intelligent decision-making)
# ML analogy: a classifier that predicts a category (activity) from one feature
# (the hour). The if/elif chain is also a one-level decision tree.
# ---------------------------------------------------------------------------
def recommend_activity(hour=None):
    """Return an activity for the hour (0-23) and the rule that fired."""
    hour = datetime.now().hour if hour is None else hour
    if 5 <= hour < 9:
        activity, rule = "have a healthy breakfast", "5 <= hour < 9"
    elif 9 <= hour < 12:
        activity, rule = "focus on study or work", "9 <= hour < 12"
    elif 12 <= hour < 14:
        activity, rule = "have lunch", "12 <= hour < 14"
    elif 14 <= hour < 17:
        activity, rule = "take a walk, then learn something new", "14 <= hour < 17"
    elif 17 <= hour < 22:
        activity, rule = "relax and have dinner", "17 <= hour < 22"
    else:
        activity, rule = "get some rest", "hour >= 22 or hour < 5"
    return f"The hour is {hour:02d}:00, so I suggest you {activity}. (Rule fired: {rule})"


# ---------------------------------------------------------------------------
# FR-14  Perceptron  (DL: artificial neuron, weights, bias, activation function,
# forward propagation, hidden layer). Weights are fixed by hand, not learned.
# ---------------------------------------------------------------------------
LABELS = ("sunshine", "free time", "energy")  # the 3 inputs, each scored 0-10
WEIGHTS = (0.5, 0.3, 0.2)   # how much each input matters
BIAS = -5.0                 # how hard it is to say yes
HIDDEN = (((0.6, 0.2, 0.2), -4.0), ((0.2, 0.4, 0.4), -4.0))  # two hidden neurons
OUT_WEIGHTS, OUT_BIAS = (1.0, 1.0), -1.0                      # output neuron


def neuron(inputs, weights, bias):
    """One artificial neuron: weighted sum + bias, then step activation -> (sum, 0 or 1)."""
    total = sum(x * w for x, w in zip(inputs, weights)) + bias
    return total, 1 if total > 0 else 0


def _read_numbers(ask, say):
    """Ask for each input; return a list of floats, or None if the user cancels."""
    values = []
    for label in LABELS:
        while True:
            say(f"Enter {label} (0-10):")
            raw = ask().strip().lower()
            if raw in ("exit", "quit", "cancel"):
                return None
            try:
                value = float(raw)
                if isfinite(value):
                    values.append(value)
                    break
            except ValueError:
                pass
            say("That's not a number. Try again, or type 'cancel'.")
    return values


def perceptron_demo(ask=input, say=print):
    """Should I go for a walk? One neuron, then a tiny hidden layer."""
    say("Perceptron demo: a single artificial neuron decides 'go for a walk?'")
    x = _read_numbers(ask, say)
    if x is None:
        say("Demo cancelled.")
        return None
    total, out = neuron(x, WEIGHTS, BIAS)
    lines = ["Forward propagation: inputs -> weights + bias -> activation -> output"]
    lines += [f"  {v:g} x {w:g} = {v * w:g}   ({lab})" for v, w, lab in zip(x, WEIGHTS, LABELS)]
    lines += [f"  weighted sum + bias ({BIAS:g}) = {total:g}",
              f"  step activation (1 if sum > 0 else 0) -> output {out}"]
    hidden = [neuron(x, w, b) for w, b in HIDDEN]
    h_out = [h[1] for h in hidden]
    _, final = neuron(h_out, OUT_WEIGHTS, OUT_BIAS)
    lines += ["Hidden layer: 2 neurons feed 1 output neuron",
              f"  hidden outputs = {h_out}, final output = {final}",
              f"Answer: {'Yes, go for a walk!' if out else 'Maybe stay in today.'}",
              "No training happened: the weights were set by hand. A real network learns them from data."]
    say("\n".join(lines))
    return out


# ---------------------------------------------------------------------------
# Concept map: where each AI / ML / DL idea lives in the code (success criteria).
# ---------------------------------------------------------------------------
CONCEPTS = [
    ("Rule-based system / intent recognition", "main.py: INTENTS + HANDLERS"),
    ("Keyword detection / pattern matching", "main.py: classify() word sets; calculator.py regex"),
    ("Similarity matching (ML analogy)", "main.py: classify() scores keyword overlap per intent"),
    ("Classification by if-else (ML analogy)", "ai_concepts.py: recommend_activity()"),
    ("Decision tree (ML analogy)", "ai_concepts.py: the if/elif chain on the hour"),
    ("Learning preferences in a session (ML analogy)", "main.py: 'call me X' updates the stored name"),
    ("Recommendation logic (ML analogy)", "content.py: _pick() chooses a different item each time"),
    ("Neuron, weights, bias, activation (DL)", "ai_concepts.py: neuron()"),
    ("Forward propagation, hidden layer (DL)", "ai_concepts.py: perceptron_demo()"),
]


def explain_concepts():
    """Printable table of concept -> code location."""
    return "Where the AI / ML / DL ideas live in my code:\n" + "\n".join(
        f"  - {c}: {where}" for c, where in CONCEPTS)
