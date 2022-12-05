from functools import total_ordering
import json
import random
from typing import List
from enum import Enum
from argparse import ArgumentParser, Namespace


@total_ordering
class LetterResult(Enum):
    GREEN = 2
    YELLOW = 1
    GREY = 0

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def get_words(words_path: str) -> List[str]:
    with open(words_path) as f:
        return json.load(f)


def check_guess(guessed: str, target: str) -> List[LetterResult]:
    # First mark every correct letter as GREEN.
    # The rest gets the default: GREY.
    guess_result = [
        LetterResult.GREEN if target[i] == guessed[i] else LetterResult.GREY for i in range(5)
    ]
    yellowed = []
    # We then take the indices of all GREY letters and iterate over those.
    ind_grey_letters = [i for i in range(5) if guess_result[i] == LetterResult.GREY]
    for ind in ind_grey_letters:
        # Now we check if the current GREY letter occurs
        # in any position of the target word that has not yet been YELLOWed.
        rest = [i for i in ind_grey_letters if i != ind and i not in yellowed]
        result = [i for i in rest if guessed[ind] == target[i]]
        # If this is the case, we mark the current GREY letter as YELLOW
        # and mark the first of the occurrences of this letter as YELLOWed
        # for further checking.
        if len(result) > 0:
            guess_result[ind] = LetterResult.YELLOW
            yellowed.append(result[0])
    return guess_result


def is_won(guess_result: List[LetterResult]) -> bool:
    return all([gr == LetterResult.GREEN for gr in guess_result])


def get_guess_result_str(guess_result: List[LetterResult]):
    result = ""
    for lr in guess_result:
        if lr == LetterResult.GREY:
            result += "⬜"
        elif lr == LetterResult.YELLOW:
            result += "🟨"
        else:
            result += "🟩"
    return result


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-w", "--wordfile", type=str, nargs="?", default="valid_words.json",
                        help="Path to the JSON file containing a list of words to be used.")
    return parser.parse_args()


class Game:
    guess_limit = 6

    def __init__(self, words_path="valid_words.json",
                 words: List[str] = None, interactive: bool = False) -> None:
        self.words = words if words is not None else get_words(words_path)
        self.target = random.choice(self.words)
        self.valid_words = get_words("valid_words.json")
        self.guesses = 0
        self.active = True
        self.interactive = interactive
        self.won = False

    def play_interactively(self):
        while self.active:
            user_guess = input("Your guess: ")
            result = self.guess(user_guess)
            print(get_guess_result_str(result))
        if self.won:
            print("You won! :)")
        else:
            print("You lost! :(")

    def guess(self, word: str) -> List[LetterResult]:
        if not self.active:
            self.game_over()
            return
        if word not in self.valid_words:
            self.invalid_guess(word)
            return
        guess_result = check_guess(word, self.target)
        self.guesses += 1
        self.won = is_won(guess_result)
        if self.guesses == self.guess_limit or self.won:
            self.active = False
        return guess_result

    def game_over(self):
        if self.interactive:
            print("Game over!")
            return
        raise Exception("Game over!")

    def invalid_guess(self, word):
        if self.interactive:
            print(f"Invalid guess: {word}")
            return
        raise Exception(f"Invalid guess: {word}")


def main():
    args = get_args()
    g = Game(args.wordfile, interactive=True)
    g.play_interactively()


if __name__ == "__main__":
    main()
