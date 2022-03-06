import textdistance
from random import randint
import sys
import urllib.request


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = len(guess) - textdistance.hamming(guess, secret)
    cows = len(guess) - textdistance.bag(guess, secret)
    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    if valid is not None:
        print(valid)
        in_word = input(prompt)
        while in_word not in valid:
            in_word = input(prompt)
    else:
        in_word = None
    return in_word


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret_word = words[randint(0, len(words))]
    c, counter = 0, 0
    while c != len(secret_word): 
        in_word = ask("Введите слово: ", words)
        counter += 1
        b, c = bullscows(in_word, secret_word)
        inform("Быки: {}, Коровы: {}", b, c)
    return counter


def main():
    dict_url = sys.argv[1]
    if len(sys.argv) >= 3:
        needed_len = sys.argv[2]
    else:
        needed_len = 5
    with urllib.request.urlopen(dict_url) as f:
        words = [word.decode('utf-8').strip() for word in f.readlines()]
    words = [word for word in words if len(word) == needed_len]
    print(gameplay(ask, inform, words))


main()
