import textdistance


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = len(guess) - textdistance.hamming(guess, secret)
    cows = len(guess) - textdistance.bag(guess, secret)
    return (bulls, cows)
