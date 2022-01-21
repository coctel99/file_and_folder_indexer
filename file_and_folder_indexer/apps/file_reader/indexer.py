import os
from string import ascii_lowercase
from typing import List, TextIO
from unicodedata import category

from unidecode import unidecode

VOWELS = set("aeiou")
CONSONANTS = set(ascii_lowercase).difference(VOWELS)
TOP_N = 5


def get_objects_list(target_path: str) -> List:
    filesystem = [target_path]
    for root, subdirectories, files in os.walk(target_path):
        for subdirectory in subdirectories:
            filesystem.append(os.path.join(root, subdirectory))
        for file in files:
            filesystem.append(os.path.join(root, file))
    return filesystem


def get_next_char(file: TextIO) -> str:
    """
    Read next character from file
    :param file: Opened file
    """
    while True:
        char = file.read(1)
        if not char:
            break
        yield char


def read_file(path: str) -> dict:
    """
    Reads specified text file by char
    :param path: File path
    :return: Dict of 5 values: N most recent words in text, N least recent
    words in text, average words length, the number of vowel letters and the
    number of consonant letters
    """
    word = ""
    unique_words = {}
    vowel_number = 0
    consonant_number = 0

    with open(path, encoding='utf-8') as fi:
        text = ""
        for char in get_next_char(fi):
            text += char
            # If character is an any unicode Letter character
            if category(char).startswith("L"):
                word += char
                ascii_char = unidecode(char)
                if ascii_char in VOWELS:
                    vowel_number += 1
                elif ascii_char in CONSONANTS:
                    consonant_number += 1
            elif word:
                unique_words[word] = unique_words.get(word, 0) + 1
                word = ""

        sorted_words = sorted(unique_words, key=unique_words.get, reverse=True)
        most_recent = sorted_words[:TOP_N]
        least_recent = sorted_words[-TOP_N:]
        average_word_length = sum(unique_words.values()) / len(unique_words)
        return {"most_recent": most_recent,
                "least_recent": least_recent,
                "average_word_length": average_word_length,
                "vowel_number": vowel_number,
                "consonant_number": consonant_number,
                }


if __name__ == '__main__':
    print(read_file('D:\\Files\\Texts\\text1.txt'))
