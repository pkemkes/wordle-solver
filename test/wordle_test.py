import unittest
from wordle import LetterResult, get_guess_result_str, check_guess


class TestWordle(unittest.TestCase):

    def test_check_guess_case_1(self):
        target = "abcde"
        guesses = ["bbbbb", "babbb", "abcde", "fghij", "eabcd"]
        expecteds = [
            [LetterResult.GREY, LetterResult.GREEN, LetterResult.GREY,
             LetterResult.GREY, LetterResult.GREY],
            [LetterResult.YELLOW, LetterResult.YELLOW, LetterResult.GREY,
             LetterResult.GREY, LetterResult.GREY],
            [LetterResult.GREEN, LetterResult.GREEN, LetterResult.GREEN,
             LetterResult.GREEN, LetterResult.GREEN],
            [LetterResult.GREY, LetterResult.GREY, LetterResult.GREY,
             LetterResult.GREY, LetterResult.GREY],
            [LetterResult.YELLOW, LetterResult.YELLOW, LetterResult.YELLOW,
             LetterResult.YELLOW, LetterResult.YELLOW]
        ]

        for i, (guess, expected) in enumerate(zip(guesses, expecteds)):
            with self.subTest(i=i):
                actual = check_guess(guess, target)
                self.assertSequenceEqual(
                    expected, actual,
                    f"{get_guess_result_str(expected)} != \
                      {get_guess_result_str(actual)}"
                )

    def test_check_guess_case_2(self):
        target = "purrs"
        guesses = ["puers", "pures"]
        expecteds = [
            [LetterResult.GREEN, LetterResult.GREEN, LetterResult.GREY,
             LetterResult.GREEN, LetterResult.GREEN],
            [LetterResult.GREEN, LetterResult.GREEN, LetterResult.GREEN,
             LetterResult.GREY, LetterResult.GREEN]
        ]

        for i, (guess, expected) in enumerate(zip(guesses, expecteds)):
            with self.subTest(i=i):
                actual = check_guess(guess, target)
                self.assertSequenceEqual(
                    expected,
                    actual, f"{get_guess_result_str(expected)} != \
                              {get_guess_result_str(actual)}"
                )


if __name__ == "__main__":
    unittest.main()
