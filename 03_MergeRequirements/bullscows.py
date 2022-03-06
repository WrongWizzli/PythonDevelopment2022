import textdistance


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = len(guess) - textdistance.hamming(guess, secret)
    cows = len(guess) - textdistance.bag(guess, secret)
    return (bulls, cows)


def ask(prompt: str, valid: list[str] = None) -> str:
    if valid is not None:
        print("Доступные слова:", valid)
        in_word = input(prompt)
        while in_word not in valid:
            in_word = input(prompt)
    return in_word

