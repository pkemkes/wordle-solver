from wordle import Game, LetterResult, check_guess, \
    is_won, get_guess_result_str
import random
from multiprocessing import Pool
from typing import List
from argparse import ArgumentParser, Namespace


def main():
    args = get_args()
    pool = Pool(args.processes)
    results = pool.map(play_game, [Game(args.wordfile) for _ in range(args.games)])
    print(f"\nWon: {results.count(True)}, Lost: {results.count(False)}")


def play_game(game: Game, verbose="") -> bool:
    remaining_words = game.words
    guesses = []
    guess_results = []
    while True:
        remaining_words = remove_words_with_result_list(remaining_words, guesses, guess_results)
        guesses.append(random.choice(remaining_words))
        guess_results.append(game.guess(guesses[-1]))
        if verbose.count("v") > 0:
            print(get_guess_result_str(guess_results[-1]))
        if not game.active:
            break
    won = is_won(guess_results[-1])
    print("W" if won else "L", end="")
    return won


def remove_words_with_result_list(remaining_words: List[str], guesses: List[str],
                                  guess_results: List[List[LetterResult]]) -> List[str]:
    for g, gr in zip(guesses, guess_results):
        remaining_words = remove_words(remaining_words, g, gr)
    return remaining_words


def remove_words(words: List[str], guess: str, guess_result: List[LetterResult]) -> List[str]:
    return [word for word in words
            if not result_is_worse(check_guess(guess, word), guess_result) and word != guess]


def result_is_worse(this: List[LetterResult], other: List[LetterResult]) -> bool:
    return any([this[i] < other[i] for i in range(5)])


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-g", "--games", type=int, nargs="?", default=1000,
                        help="Number of games to be played.")
    parser.add_argument("-p", "--processes", type=int, nargs="?", default=16,
                        help="Number of processes to be used for the multiprocessing pool.")
    parser.add_argument("-w", "--wordfile", type=str, nargs="?", default="valid_words.json",
                        help="Path to the JSON file containing a list of words to be used.")
    return parser.parse_args()


if __name__ == "__main__":
    main()
