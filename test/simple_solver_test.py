import unittest
from wordle import LetterResult
from simple_solver import remove_words, remove_words_with_result_list


class TestSimpleSolver(unittest.TestCase):

    words_cases = [
        ["abcde", "aaaaa"],
        ["azcxd", "adcll", "bbbbb", "dbcue", "abcde"]
    ]
    guess_cases = [
        "aabba",
        "abcde"
    ]
    guess_result_cases = [
        [LetterResult.GREEN, LetterResult.GREEN, LetterResult.GREY, LetterResult.GREY, LetterResult.GREEN],
        [LetterResult.GREEN, LetterResult.GREY, LetterResult.GREEN, LetterResult.YELLOW, LetterResult.GREY]
    ]
    expected_cases = [
        ["aaaaa"],
        ["azcxd", "adcll"]
    ]

    def test_remove_words(self):
        for i, (words, guess, guess_result, expected) in enumerate(
            zip(self.words_cases, self.guess_cases, self.guess_result_cases, self.expected_cases)):
            with self.subTest(i=i):
                actual = remove_words(words, guess, guess_result)
                self.assertSequenceEqual(expected, actual)

    def test_remove_words_with_result_list(self):
        words = ["abcde", "aaaaa", "aabbd"]
        guesses = ["fgcdd", "bjufd"]
        results = [
            [LetterResult.GREY, LetterResult.GREY, LetterResult.GREY, LetterResult.GREY, LetterResult.GREEN],
            [LetterResult.YELLOW, LetterResult.GREY, LetterResult.GREY, LetterResult.GREY, LetterResult.GREEN]
        ]
        expected = ["aabbd"]
        
        self.assertSequenceEqual(expected, remove_words_with_result_list(words, guesses, results))

    def test_remove_words_with_result_list_failed(self):
        words = ["koori", "liane", "sieth", "eight"]
        guesses = ["koori", "liane", "sieth"]
        results = [
            [LetterResult.GREY, LetterResult.GREY, LetterResult.GREY, LetterResult.GREY, LetterResult.YELLOW], 
            [LetterResult.GREY, LetterResult.GREEN, LetterResult.GREY, LetterResult.GREY, LetterResult.YELLOW], 
            [LetterResult.GREY, LetterResult.GREEN, LetterResult.YELLOW, LetterResult.YELLOW, LetterResult.YELLOW]
        ]
        expected = ["eight"]
        
        self.assertSequenceEqual(expected, remove_words_with_result_list(words, guesses, results))