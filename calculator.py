"""Basic calculator: parse "12 + 8" style text and compute it (FR-05)."""
import re
from math import isfinite

# number, operator, number. Digits only, so words like "abc" never reach float().
_EXPR = re.compile(r"(-?\d+(?:\.\d+)?)\s*([-+*/x×÷])\s*(-?\d+(?:\.\d+)?)")
# Spoken operators are rewritten to symbols before matching ("5 plus 3" -> "5 + 3").
_WORDS = {" plus ": "+", " minus ": "-", " times ": "*", " multiplied by ": "*",
          " divided by ": "/", " over ": "/"}
USAGE = "Try something like: calculate 12 + 8"


def parse_expression(text):
    """Return (a, op, b) as (float, str, float), or None if no expression found."""
    for word, symbol in _WORDS.items():
        text = text.replace(word, symbol)
    m = _EXPR.search(text)
    if not m:
        return None
    op = {"x": "*", "×": "*", "÷": "/"}.get(m.group(2), m.group(2))
    return float(m.group(1)), op, float(m.group(3))


def calculate(text):
    """Return a friendly answer string. Never raises (reliability NFR)."""
    parsed = parse_expression(text)
    if not parsed:
        return USAGE
    a, op, b = parsed
    if op == "/" and b == 0:
        return "I can't divide by zero — try a different number."
    r = {"+": a + b, "-": a - b, "*": a * b}.get(op) if op != "/" else a / b
    if not isfinite(r):  # float overflow, e.g. 1e308 * 10
        return "That number is too big for me — try smaller numbers."
    return f"The result is {int(r) if r == int(r) else round(r, 6)}"
