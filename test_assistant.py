"""Automated version of the PRD testing checklist (s33) and acceptance tests (s30).
Run:  python -m unittest -v
"""
import unittest
from datetime import datetime

import ai_concepts
import calculator
import content
import datetime_utils
import game
import greetings
import main


def play(secret, guesses):
    """Run the game with scripted guesses; return (result, printed lines)."""
    feed, out = iter(guesses), []
    return game.play_guessing_game(lambda: next(feed), out.append, secret), out


class Calculator(unittest.TestCase):
    def test_operators(self):
        for text, want in [("calculate 12 + 8", "20"), ("9 - 4", "5"), ("6 * 7", "42"),
                           ("calculate 7 / 2", "3.5"), ("5 plus 3", "8"), ("2x3", "6")]:
            self.assertEqual(calculator.calculate(text), f"The result is {want}")

    def test_divide_by_zero(self):
        self.assertIn("can't divide by zero", calculator.calculate("calculate 5 / 0"))

    def test_bad_input_and_overflow(self):
        self.assertEqual(calculator.calculate("calculate abc + 2"), calculator.USAGE)
        self.assertIn("too big", calculator.calculate("1" + "0" * 400 + " * 10"))


class Content(unittest.TestCase):
    def test_randomness_and_no_repeat(self):
        for pick in (content.get_random_quote, content.get_random_joke, content.get_random_fact):
            seen = [pick() for _ in range(6)]
            self.assertGreaterEqual(len(set(seen)), 2)
            self.assertTrue(all(a != b for a, b in zip(seen, seen[1:])))


class Game(unittest.TestCase):
    def test_hints_and_win(self):
        result, out = play(10, ["5", "15", "10"])
        self.assertTrue(result)
        self.assertIn("higher", out[1]); self.assertIn("lower", out[2])

    def test_attempt_limit(self):
        result, out = play(10, ["1"] * 5)
        self.assertFalse(result); self.assertIn("Out of tries", out[-1])

    def test_invalid_guess_is_free_and_quit_works(self):
        result, _ = play(10, ["abc", "99", "1", "2", "3", "4", "10"])
        self.assertTrue(result)  # 2 invalid inputs did not use tries
        self.assertIsNone(play(10, ["quit"])[0])


class Concepts(unittest.TestCase):
    def test_recommendation_changes_with_time(self):
        texts = {ai_concepts.recommend_activity(h) for h in (7, 10, 13, 15, 19, 23)}
        self.assertEqual(len(texts), 6)

    def test_perceptron_is_0_or_1_and_demo_runs(self):
        self.assertEqual(ai_concepts.neuron([10, 10, 10], ai_concepts.WEIGHTS, ai_concepts.BIAS)[1], 1)
        self.assertEqual(ai_concepts.neuron([0, 0, 0], ai_concepts.WEIGHTS, ai_concepts.BIAS)[1], 0)
        feed, out = iter(["8", "x", "6", "7"]), []
        self.assertEqual(ai_concepts.perceptron_demo(lambda: next(feed), out.append), 1)
        self.assertIn("not a number", "\n".join(out))
        self.assertIn("Hidden layer", out[-1])


class DateTime(unittest.TestCase):
    def test_format(self):
        now = datetime(2026, 11, 7, 15, 45)
        self.assertEqual(datetime_utils.get_current_time(now), "It's currently 3:45 PM.")
        self.assertIn("Saturday, 07 November 2026", datetime_utils.get_current_date(now))


class EndToEnd(unittest.TestCase):
    """Drive the real main loop with scripted input (>= 20 inputs incl. invalid)."""
    SCRIPT = ["my name is priya", "hello", "time", "date", "calculate 12 + 8", "calculate 5 / 0",
              "calculate abc", "joke", "quote", "fact", "asdkfj", "", "!!!", "recommend",
              "what is the time today", "sometimes", "concepts", "help", "call me Sam",
              "game", "5", "quit", "perceptron", "8", "6", "7", "bye"]

    def test_full_session(self):
        feed, out = iter(self.SCRIPT), []
        main.ask = lambda: next(feed)
        main.say = out.append
        main.print = lambda *a: None
        main.run()
        text = "\n".join(out)
        self.assertEqual(text.count("Nice to meet you, Priya"), 1)
        self.assertGreaterEqual(text.count("Priya"), 4)            # name reused
        self.assertIn("The result is 20", text)
        self.assertIn("can't divide by zero", text)
        self.assertEqual(text.count(main.FALLBACK), 4)             # asdkfj, '', !!!, sometimes
        self.assertIn("I'll call you Sam", text)
        self.assertEqual(out[-1], "Goodbye, Sam! Have a great day.")

    def test_classify(self):
        for text, want in [("tell me a joke", "joke"), ("what's the date", "date"),
                           ("12+8", "calculate"), ("sometimes", "fallback"), ("bye", "exit"),
                           ("hello there", "greeting"), ("help me", "help")]:
            self.assertEqual(main.classify(text), want)

    def test_name_cleanup(self):
        self.assertEqual(greetings.clean_name("  my name is priya "), "Priya")
        self.assertEqual(greetings.clean_name("   "), "Friend")


if __name__ == "__main__":
    unittest.main()
