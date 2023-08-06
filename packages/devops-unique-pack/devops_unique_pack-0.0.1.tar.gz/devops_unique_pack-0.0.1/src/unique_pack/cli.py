import argparse
from pathlib import Path
from collections import Counter
from functools import lru_cache


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', type=str, help='argument "text" should be a string')
    parser.add_argument('-f', '--file', type=str, help='argument "file" should be a name of file with text')
    args = parser.parse_args()
    if args.file:
        try:
            return unique(''.join(Path(args.file).read_text().splitlines()))
        except FileNotFoundError:
            raise FileNotFoundError('file not found')
    elif args.text:
        return unique(args.text)

@lru_cache(maxsize=8)
def unique(text):
    if not type(text) == str:
        raise TypeError('the text should be string')
    return sum(value for value in Counter(text).values() if value == 1)


if __name__ == '__main__':
    cli()
