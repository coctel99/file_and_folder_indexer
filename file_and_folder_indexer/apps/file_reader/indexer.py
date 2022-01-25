import json
import logging
import os
from dataclasses import dataclass, field
from string import ascii_lowercase

from typing import Dict, List, TextIO
from unicodedata import category

from unidecode import unidecode

from file_and_folder_indexer.apps.file_reader.apps import FileReaderConfig

VOWELS = set("aeiou")
CONSONANTS = set(ascii_lowercase).difference(VOWELS)
TOP_N = 5
logger = logging.getLogger(__name__)


@dataclass
class Statistics:
    files_and_folders: List = field(default_factory=list)
    number_of_files: int = 0
    unique_words: Dict = field(default_factory=dict)
    most_recent: List = field(default_factory=list)
    least_recent: List = field(default_factory=list)
    total_words_number: int = 0
    total_words_length: int = 0
    average_word_length: float = 0.0
    times_in_text: int = 0
    vowel_number: int = 0
    consonant_number: int = 0

    def update_unique_words(self, word: str) -> None:
        """Add new word in dict or increment words counter"""
        self.unique_words[word] = self.unique_words.get(word, 0) + 1

    def set_recent_words(self) -> None:
        """Calculate TOP_N most recent and least recent words and set
        corresponding attribute values"""
        sorted_words = sorted(
            self.unique_words,
            key=self.unique_words.get,
            reverse=True
        )
        most_recent = sorted_words[:TOP_N]
        least_recent = sorted_words[-TOP_N:]
        least_recent.reverse()
        self.most_recent = most_recent
        self.least_recent = least_recent

    def set_average_word_length(self) -> None:
        """Calculate and set average words length attribute value"""
        if self.total_words_number:
            avg_words_len = self.total_words_length / self.total_words_number
            self.average_word_length = avg_words_len
        else:
            self.average_word_length = 0.0

    def validate_as_dict(self, valid_parameters: List) -> Dict:
        """
        Get statistics only with valid parameters if they are specified, else
        get all statistics
        :param valid_parameters: List of valid parameters
        :return: Statistics as dict
        """
        valid_statistics = {}
        for parameter in valid_parameters:
            if parameter and type(getattr(self, parameter)) is not bool:
                valid_statistics.update({parameter: getattr(self, parameter)})
        if valid_statistics:
            return valid_statistics
        for attr, value in self.__dict__.items():
            if value and type(value) is not bool:
                valid_statistics.update({attr: value})
        return valid_statistics


class FileSystemException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


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


def get_word_statistics(path: str, statistics: Statistics) -> type(Statistics):
    """
    Get number of vowels and consonants in word
    :param path: Path to the word in text file
    :param statistics: Requested information
    :return: Dict of 2 values: the number of vowels and the number of
    consonants
    """
    word = os.path.split(path)[-1]
    path = os.path.dirname(path)
    file_statistics = get_file_statistics(path, Statistics())
    statistics.times_in_text = file_statistics.unique_words.get(word, 0)

    statistics.vowel_number = 0
    statistics.consonant_number = 0
    for char in word:
        ascii_char = unidecode(char.lower())
        if ascii_char in VOWELS:
            statistics.vowel_number += 1
        elif ascii_char in CONSONANTS:
            statistics.consonant_number += 1

    return statistics


def get_file_statistics(path: str,
                        statistics: Statistics) -> type(Statistics):
    """
    Reads specified text file by char
    :param path: File path
    :param statistics: Requested information
    :return: Dict of 3 values: dict of unique words, vowels number and
    consonants number
    """
    file_ext = os.path.splitext(path)[1]
    if file_ext not in FileReaderConfig.allowed_file_extensions:
        raise FileSystemException("File extension is not in allowed "
                                  "extensions list.")
    word = ""
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
                            statistics.vowel_number += 1
                        elif ascii_char.issubset(CONSONANTS):
                            statistics.consonant_number += 1
                    elif word:
                        statistics.update_unique_words(word)
                        statistics.total_words_number += 1
                        statistics.total_words_length += len(word)
                        word = ""
                # If word buffer is not empty
                if word:
                    statistics.update_unique_words(word)
                    statistics.total_words_number += 1
                    statistics.total_words_length += len(word)

                statistics.set_recent_words()
                statistics.set_average_word_length()

                break
        except ValueError as err:
            logger.warning(f"Reading file in {path} with {encoding} encoding "
                           f"failed:\n{err}")
    return statistics


def get_folder_statistics(root_path: os.path,
                          statistics: Statistics) -> type(Statistics):
    """
    Iterates through all subfolders and files
    :param root_path: Folder path
    :param statistics: Requested information types
    :return:
    """
    parse_files = not any([val for param, val in statistics.__dict__.items()])
    for param, val in statistics.__dict__.items():
        if val and param not in ['files_and_folders', 'number_of_files']:
            parse_files = True
            break

    files_and_folders = get_objects_list(root_path)
    statistics.files_and_folders = files_and_folders
    statistics.number_of_files = len([file for file in files_and_folders
                                      if os.path.isfile(file)])

    if not parse_files:
        return statistics

    for path in statistics.files_and_folders:
        if os.path.isfile(path):
            file_ext = os.path.splitext(path)[1]
            if file_ext in FileReaderConfig.allowed_file_extensions:
                file_statistics = get_file_statistics(path, Statistics())
                statistics.unique_words.update(file_statistics.unique_words)
                statistics.vowel_number += file_statistics.vowel_number
                statistics.consonant_number += file_statistics.consonant_number
                statistics.total_words_number += (
                    file_statistics.total_words_number)
                statistics.total_words_length += (
                    file_statistics.total_words_length)

    statistics.set_recent_words()
    statistics.set_average_word_length()

    return statistics


def indexate(path: os.path, statistics: Statistics) -> type(Statistics):
    """
    Get statistics from specified path
    :param path: Path to check
    :param statistics: Statistics to gather
    """
    valid_parameters = [param for param, value in statistics.__dict__.items()
                        if value]
    if os.path.isdir(path):
        info = get_folder_statistics(path, statistics)
        info = info.validate_as_dict(valid_parameters)
        return info
    elif os.path.isfile(path):
        info = get_file_statistics(path, statistics)
        info = info.validate_as_dict(valid_parameters)
        return info
    elif os.path.isfile(os.path.dirname(path)):
        info = get_word_statistics(path, statistics)
        if info:
            info = info.validate_as_dict(valid_parameters)
            return info
        raise FileSystemException("No such word in file.")
    raise FileSystemException("No such file or directory.")