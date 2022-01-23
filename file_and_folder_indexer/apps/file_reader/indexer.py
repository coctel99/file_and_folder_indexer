import os
from string import ascii_lowercase
from typing import List, TextIO
from unicodedata import category

from unidecode import unidecode

from file_and_folder_indexer.apps.file_reader.apps import FileReaderConfig

VOWELS = set("aeiou")
CONSONANTS = set(ascii_lowercase).difference(VOWELS)
TOP_N = 5


def get_objects_list(target_path: str) -> List:
    """
    Get list of files and folders for the specified path
    :param target_path: Path to check
    :return: List of files and folders
    """
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


def get_word_statistics(path: str) -> dict or None:
    """
    Get number of vowels and consonants in word
    :param path: Path to the word in text file
    :return: Dict of 2 values: the number of vowels and the number of
    consonants
    """
    word = os.path.split(path)[-1]
    path = os.path.dirname(path)
    unique_words, *_ = get_file_statistics(path).values()
    times_in_text = unique_words.get(word, 0)
    if times_in_text == 0:
        return None

    vowel_number = 0
    consonant_number = 0

    for char in word:
        ascii_char = unidecode(char.lower())
        if ascii_char in VOWELS:
            vowel_number += 1
        elif ascii_char in CONSONANTS:
            consonant_number += 1

    return {'times_in_text': times_in_text,
            'vowel_number': vowel_number,
            'consonant_number': consonant_number}


def get_file_statistics(path: str) -> dict:
    """
    Reads specified text file by char
    :param path: File path
    :return: Dict of 3 values: dict of unique words, vowels number and
    consonants number
    """
    word = ""
    unique_words = {}
    vowel_number = 0
    consonant_number = 0
    most_recent = []
    least_recent = []
    total_words_number = 0
    total_words_length = 0
    average_word_length = 0

    encodings_queue = FileReaderConfig.encodings_queue
    for encoding in encodings_queue:
        try:
            with open(path, encoding=encoding) as fi:
                for char in get_next_char(fi):
                    # If character is an any unicode Letter character
                    if category(char).startswith("L"):
                        word += char
                        ascii_char = set(unidecode(char.lower()))
                        if ascii_char.issubset(VOWELS):
                            vowel_number += 1
                        elif ascii_char.issubset(CONSONANTS):
                            consonant_number += 1
                    elif word:
                        unique_words[word] = unique_words.get(word, 0) + 1
                        total_words_number += 1
                        total_words_length += len(word)
                        word = ""
                # If word buffer is not empty
                if word:
                    unique_words[word] = unique_words.get(word, 0) + 1
                    total_words_number += 1
                    total_words_length += len(word)

                sorted_words = sorted(unique_words, key=unique_words.get,
                                      reverse=True)
                # sorted_pairs = [(word, unique_words.get(word))
                #                 for word in sorted_words]
                most_recent = sorted_words[:TOP_N]
                least_recent = sorted_words[-TOP_N:]
                least_recent.reverse()
                if total_words_number:
                    average_word_length = (total_words_length /
                                           total_words_number)

                break
        except UnicodeError as err:
            print(f"Read file in {path} with {encoding} encoding "
                  f"failed:\n{err}")

    return {'unique_words': unique_words,
            'most_recent': most_recent,
            'least_recent': least_recent,
            'total_words_number': total_words_number,
            'total_words_length': total_words_length,
            'average_word_length': average_word_length,
            'vowel_number': vowel_number,
            'consonant_number': consonant_number}


def get_folder_statistics(root_path: os.path) -> dict:
    files_and_folders = get_objects_list(root_path)
    number_of_files = len([file for file in files_and_folders
                           if os.path.isfile(file)])
    unique_words = {}
    vowel_number = 0
    consonant_number = 0
    total_words_number = 0
    total_words_length = 0
    average_word_length = 0
    files_read = 0

    for path in files_and_folders:
        if os.path.isfile(path):
            file_ext = os.path.splitext(path)[1]
            if file_ext in FileReaderConfig.allowed_file_extensions:
                files_read += 1
                file_statistics = get_file_statistics(path)
                unique_words.update(file_statistics.get('unique_words'))
                vowel_number += file_statistics.get('vowel_number')
                consonant_number += file_statistics.get('consonant_number')
                total_words_number += file_statistics.get('total_words_number')
                total_words_length += file_statistics.get('total_words_length')

    sorted_words = sorted(unique_words, key=unique_words.get, reverse=True)
    most_recent = sorted_words[:TOP_N]
    least_recent = sorted_words[-TOP_N:]
    least_recent.reverse()
    # word_lengths = [len(word) for word in unique_words]
    # average_word_length = sum(word_lengths) / len(unique_words)
    if total_words_number:
        average_word_length = total_words_length / total_words_number

    return {"files_and_folders": files_and_folders,
            "number_of_files": number_of_files,
            "most_recent": most_recent,
            "least_recent": least_recent,
            "average_word_length": average_word_length,
            "vowel_number": vowel_number,
            "consonant_number": consonant_number}
