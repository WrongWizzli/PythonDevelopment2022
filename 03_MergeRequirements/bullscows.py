import textdistance
from random import randint


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = len(guess) - textdistance.hamming(guess, secret)
    cows = max(len(guess) - textdistance.bag(guess, secret) - bulls, 0)
    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    if valid is not None:
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
