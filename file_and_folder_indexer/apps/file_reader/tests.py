import os

from django.test import TestCase

from file_and_folder_indexer.apps.file_reader.indexer import (
    get_file_statistics, get_folder_statistics, get_objects_list,
    get_word_statistics)

test_dir = 'test_dir'
test_file = os.path.join(test_dir, 'test.txt')
empty_dir = os.path.join(test_dir, 'Empty Folder')


class IndexerTestCase(TestCase):
    def setUp(self) -> None:
        if not os.path.exists(test_dir):
            os.mkdir(test_dir)
            os.mkdir(empty_dir)

    def tearDown(self) -> None:
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(test_dir):
            os.rmdir(empty_dir)
        if os.path.exists(test_dir):
            os.rmdir(test_dir)

    @staticmethod
    def set_up_file(test_text: str) -> None:
        with open(file=test_file, mode='w', encoding='utf-8') as f:
            f.write(test_text)

    def test_get_files_and_folders_paths(self):
        self.set_up_file('test')
        lst = get_objects_list(test_dir)
        files_and_folders = [test_dir]
        dir_list = os.listdir(test_dir)
        for element in dir_list:
            element = os.path.join(test_dir, element)
            if os.path.isdir(element) or os.path.isfile(element):
                files_and_folders.append(element)

        self.assertEqual(lst, files_and_folders)

    def test_get_word_statistics_(self):
        text = 'test'
        self.set_up_file(text)
        word_path = os.path.join(test_file, 'test')
        info = get_word_statistics(word_path)
        times_in_text = 1
        vowel_number = 1
        consonant_number = 3
        self.assertTrue(all([
            info.get('times_in_text') == times_in_text,
            info.get('vowel_number') == vowel_number,
            info.get('consonant_number') == consonant_number
        ]))

    def test_get_word_statistics_russian_file(self):
        text = 'Файл для теста с текстом для теста.'
        target = 'теста'
        self.set_up_file(text)
        word_path = os.path.join(test_file, target)
        info = get_word_statistics(word_path)
        times_in_text = text.count(target)
        vowel_number = 2
        consonant_number = 3
        self.assertTrue(all([
            info.get('times_in_text') == times_in_text,
            info.get('vowel_number') == vowel_number,
            info.get('consonant_number') == consonant_number
        ]))

    def test_get_file_statistics(self):
        text = ('test test test test test words words words words in in in '
                'a a file')
        self.set_up_file(text)
        info = get_file_statistics(test_file)
        most_recent = ['test', 'words', 'in', 'a', 'file']
        least_recent = ['file', 'a', 'in', 'words', 'test']
        average_word_length = (sum([len(word) for word in text.split()]) /
                               len(text.split()))
        vowel_number = 16
        consonant_number = 36
        self.assertTrue(all([
            info.get('most_recent') == most_recent,
            info.get('least_recent') == least_recent,
            info.get('average_word_length') == average_word_length,
            info.get('vowel_number') == vowel_number,
            info.get('consonant_number') == consonant_number
        ]))

    def test_get_folder_statistics(self):
        text = 'test text'
        self.set_up_file('test text')
        info = get_folder_statistics(test_dir)
        files_and_folders = get_objects_list(test_dir)
        number_of_files = 1
        most_recent = ['test', 'text']
        least_recent = ['text', 'test']
        average_word_length = (sum([len(word) for word in text.split()]) /
                               len(text.split()))
        vowel_number = 2
        consonant_number = 6
        self.assertTrue(all([
            info.get('files_and_folders') == files_and_folders,
            info.get('number_of_files') == number_of_files,
            info.get('most_recent') == most_recent,
            info.get('least_recent') == least_recent,
            info.get('average_word_length') == average_word_length,
            info.get('vowel_number') == vowel_number,
            info.get('consonant_number') == consonant_number
        ]))
