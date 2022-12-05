# Wordle Solver

This repository contains the following implementations:

- `wordle.py`: A custom version of the Wordle game. Can either be played interactively on the CLI, or automated as a library.
- `simple_solver.py`: A naive Wordle solver that simply picks the next word by eliminating all words from its pool that would not at least yield the same score as the previous one. Plays a default of 1000 games and reports the statistics of wins vs. losses.

This can be played with two word sets:

- `valid_words.json` contains all valid 5 letter words from the English dictionary.
- `used_words.json` contains all words that have been used as a target in the past in [the original Wordle game](https://www.nytimes.com/games/wordle/index.html).

**Note**
This only affects the pool of words used to pick a target (and choosing words in case of the simple_solver). The validity of words is always checked with the `valid_words.json`.

## Usage:

To play a game of Wordle on the CLI:

```bash
python wordle.py
```

To run the simple_solver[^1]:

```bash
python -u simple_solver.py
```

In all cases the `-h` flag can be supplied to get an overview of optional arguments.

[^1]: The `-u` starts python in `unbuffered` mode which enables a smoother output of the current status.