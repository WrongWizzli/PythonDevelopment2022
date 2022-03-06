from bullscows import gameplay, ask, inform
import urllib.request
import sys


if __name__ == "__main__":
    dict_url = sys.argv[1]
    if len(sys.argv) >= 3:
        needed_len = sys.argv[2]
    else:
        needed_len = 5
    with urllib.request.urlopen(dict_url) as f:
        words = [word.decode('utf-8').strip() for word in f.readlines()]
    words = [word for word in words if len(word) == needed_len]
    print(gameplay(ask, inform, words))
