# Nova — Virtual AI Assistant

Nexbridge Technologies · AI Internship Program · Project AI-INT-P1-VAA

A text-based, rule-based assistant that runs offline in the terminal. Python 3 standard library only: no internet, no database, no ML libraries, no files written. All state (the user's name) lives in memory and resets on restart.

## Run

    python main.py              # start the assistant
    python -m unittest -v       # run the automated test checklist

## Commands

| Command | What it does |
|---|---|
| `time` / `date` | current time / date |
| `calculate 12 + 8` | + - * / (also `12+8`, `5 plus 3`, `6 x 7`); safe on divide-by-zero and bad input |
| `joke` / `quote` / `fact` | random item from a predefined list (never the same one twice in a row) |
| `game` | number guessing game, 1–20, 5 tries, higher/lower hints (`quit` to leave) |
| `recommend` | rule-based activity suggestion for the current hour |
| `perceptron` | one artificial neuron plus a tiny hidden layer |
| `concepts` | where each AI / ML / DL idea lives in the code |
| `call me <name>` | changes the name Nova uses for you |
| `help` | lists every command |
| `exit` / `quit` / `bye` | ends the session (Ctrl+C also exits cleanly) |

Anything else gets a friendly fallback message.

## Structure (PRD s24)

    virtual-ai-assistant/
    |-- main.py            main loop: input -> normalize -> classify -> respond_*()
    |-- greetings.py       get_user_name(), build_greeting()
    |-- datetime_utils.py  get_current_time(), get_current_date()
    |-- calculator.py      parse_expression(), calculate()
    |-- content.py         QUOTES, JOKES, FACTS + get_random_quote/joke/fact()
    |-- game.py            play_guessing_game()
    |-- ai_concepts.py     recommend_activity(), perceptron_demo()
    |-- help_menu.py       print_help()
    |-- test_assistant.py  automated tests (extra, optional)
    `-- README.md

## Requirements coverage

| ID | Where |
|---|---|
| FR-01, FR-02 | `greetings.py`; name reused in greeting, jokes/quotes/facts, recommend, goodbye |
| FR-03, FR-04 | `datetime_utils.py` |
| FR-05 | `calculator.py` |
| FR-06–08 | `content.py` |
| FR-09 | `game.py` |
| FR-10 | `help_menu.py` |
| FR-11 | `main.run()` ends the loop on exit/quit/bye |
| FR-12 | fallback in `main.py`, plus a catch-all so one bad command cannot end the session |
| FR-13 | `ai_concepts.recommend_activity()` |
| FR-14 | `ai_concepts.neuron()` and `perceptron_demo()` (includes a hidden layer) |

## AI / ML / DL concept map

| Concept | Code |
|---|---|
| Rule-based system, intent recognition | `main.py`: `INTENTS`, `HANDLERS` |
| Keyword detection, pattern matching | `main.py`: `classify()`; `calculator.py` regex |
| Similarity matching (ML analogy) | `classify()` scores keyword overlap for each intent |
| Classification, decision tree (ML analogy) | `recommend_activity()` if/elif chain on the hour |
| Learning preferences in a session (ML analogy) | `call me <name>` updates the stored name |
| Recommendation logic (ML analogy) | `content._pick()` |
| Neuron, weights, bias, activation, forward propagation, hidden layer (DL) | `neuron()`, `perceptron_demo()` |

No model is trained: the perceptron weights are fixed by hand, as the PRD requires.

## Manual test checklist (PRD s33)

All items are covered by `test_assistant.py` (13 tests, including a 27-input end-to-end session with invalid inputs).

- [x] Starts without errors · [x] Name requested and reused
- [x] Date and time correct · [x] Calculator + − * / · [x] divide by zero · [x] non-numeric input
- [x] Joke / quote / fact vary on repeat · [x] Game attempt limit · [x] higher/lower hints
- [x] Help lists every command · [x] Unknown input → fallback · [x] Exit ends cleanly
- [x] Recommendation differs by hour · [x] Perceptron outputs 0 or 1

## Design notes

- **Fast start:** only `re`, `random`, `datetime`, `math` are imported (no web server, no JSON). Startup is about 21 ms versus about 46 ms for the earlier web version.
- **Short routing:** one `INTENTS` table and one `HANDLERS` table replace a long if/elif chain, and matching is by whole words, so "sometimes" no longer triggers `time`.
- **Testable:** modules take `ask`/`say` parameters, so tests drive the real code without a keyboard.
