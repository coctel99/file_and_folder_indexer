import json
import os

from django.test import Client, TestCase

from file_and_folder_indexer.apps.file_reader.conversion import convert_to_url
from file_and_folder_indexer.apps.file_reader.indexer import (
    Statistics, get_file_statistics, get_folder_statistics, get_objects_list,
    get_word_statistics)

test_dir = 'test_dir'
test_file = os.path.join(test_dir, 'test.txt')
empty_dir = os.path.join(test_dir, 'Empty Folder')


class IndexerTestCase(TestCase):
    def setUp(self) -> None:
        """Create test directories in project root folder."""
        if not os.path.exists(test_dir):
            os.mkdir(test_dir)
            os.mkdir(empty_dir)

    def tearDown(self) -> None:
        """Remove test directories and files."""
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(test_dir):
            os.rmdir(empty_dir)
        if os.path.exists(test_dir):
            os.rmdir(test_dir)

    @staticmethod
    def set_up_file(test_text: str) -> None:
        """Creates test '.txt' file with specified text."""
        with open(file=test_file, mode='w', encoding='utf-8') as f:
            f.write(test_text)

    def test_get_files_and_folders_paths(self):
        """Testing that list of folders and files of specified directory is
        returned."""
        self.set_up_file('test')
        lst = get_objects_list(test_dir)
        files_and_folders = [test_dir]
        for root, subdirectories, files in os.walk(test_dir):
            for subdirectory in subdirectories:
                files_and_folders.append(os.path.join(root, subdirectory))
            for file in files:
                files_and_folders.append(os.path.join(root, file))

        self.assertEqual(lst, files_and_folders)

    def test_get_word_statistics_(self):
        """Testing that statistics about word in the text file is returned."""
        text = 'test'
        self.set_up_file(text)
        word_path = os.path.join(test_file, 'test')
        statistics = get_word_statistics(word_path, Statistics())
        times_in_text = 1
        vowel_number = 1
        consonant_number = 3
        self.assertTrue(all([
            statistics.times_in_text == times_in_text,
            statistics.vowel_number == vowel_number,
            statistics.consonant_number == consonant_number
        ]))

    def test_get_word_statistics_russian_file(self):
        """Testing that statistics about word in the russian text file is
        returned."""
        text = '???????? ?????? ?????????? ?? ?????????????? ?????? ??????????.'
        target = '??????????'
        self.set_up_file(text)
        word_path = os.path.join(test_file, target)
        statistics = get_word_statistics(word_path, Statistics())
        times_in_text = text.count(target)
        vowel_number = 2
        consonant_number = 3
        self.assertTrue(all([
            statistics.times_in_text == times_in_text,
            statistics.vowel_number == vowel_number,
            statistics.consonant_number == consonant_number
        ]))

    def test_get_file_statistics(self):
        """Testing that statistics about the text file is returned."""
        text = ('test test test test test words words words words in in in '
                'a a file')
        self.set_up_file(text)
        statistics = get_file_statistics(test_file, Statistics())
        most_recent = ['test', 'words', 'in', 'a', 'file']
        least_recent = ['file', 'a', 'in', 'words', 'test']
        average_word_length = (sum([len(word) for word in text.split()]) /
                               len(text.split()))
        vowel_number = 16
        consonant_number = 36
        self.assertTrue(all([
            statistics.most_recent == most_recent,
            statistics.least_recent == least_recent,
            statistics.average_word_length == average_word_length,
            statistics.vowel_number == vowel_number,
            statistics.consonant_number == consonant_number
        ]))

    def test_get_folder_statistics(self):
        """Testing that statistics about the folder is returned."""
        text = 'test text'
        self.set_up_file('test text')
        statistics = get_folder_statistics(test_dir, Statistics())
        files_and_folders = get_objects_list(test_dir)
        number_of_files = 1
        most_recent = ['test', 'text']
        least_recent = ['text', 'test']
        average_word_length = (sum([len(word) for word in text.split()]) /
                               len(text.split()))
        vowel_number = 2
        consonant_number = 6
        self.assertTrue(all([
            statistics.files_and_folders == files_and_folders,
            statistics.number_of_files == number_of_files,
            statistics.most_recent == most_recent,
            statistics.least_recent == least_recent,
            statistics.average_word_length == average_word_length,
            statistics.vowel_number == vowel_number,
            statistics.consonant_number == consonant_number
        ]))


class ApiRequestTestCase(TestCase):
    def setUp(self) -> None:
        """Create test directories in project root folder."""
        if not os.path.exists(test_dir):
            os.mkdir(test_dir)
            os.mkdir(empty_dir)

    def tearDown(self) -> None:
        """Remove test directories and files."""
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(test_dir):
            os.rmdir(empty_dir)
        if os.path.exists(test_dir):
            os.rmdir(test_dir)

    @staticmethod
    def set_up_file(test_text: str) -> None:
        """Creates test '.txt' file with specified text."""
        with open(file=test_file, mode='w', encoding='utf-8') as f:
            f.write(test_text)

    def test_get_filesystem_page(self):
        """Testing that request to '/filesystem/' without specifying
        'url_path' gets response with 404 status code."""
        client = Client()
        response = client.get('/api/filesystem/')
        self.assertTrue(response.status_code == 404)

    def test_get_swagger_page(self):
        """Testing that request to '/swagger/' gets response with 200 status
        code."""
        client = Client()
        response = client.get('/swagger/')
        self.assertTrue(response.status_code == 200)

    def test_get_filesystem_word_statistics(self):
        """Testing that valid word statistics is returned."""
        self.set_up_file('text')
        client = Client()
        url = convert_to_url('/api/filesystem/' + test_file + '/text/')
        info = {
            "times_in_text": 1,
            "vowel_number": 1,
            "consonant_number": 3
        }
        info = json.dumps(info, indent=4, ensure_ascii=False)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, info)

    def test_get_filesystem_file_statistics(self):
        """Testing that valid file statistics is returned."""
        self.set_up_file('text')
        client = Client()
        url = convert_to_url('/api/filesystem/' + test_file + '/')
        info = {
            "most_recent": [
                "text"
            ],
            "least_recent": [
                "text"
            ],
            "total_words_number": 1,
            "total_words_length": 4,
            "average_word_length": 4.0,
            "vowel_number": 1,
            "consonant_number": 3
        }
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, info)

    def test_get_filesystem_folder_statistics(self):
        """Testing that valid folder statistics is returned."""
        self.set_up_file('text')
        client = Client()
        url = convert_to_url('/api/filesystem/' + test_dir + '/')
        info = {
            "files_and_folders": [
                test_dir,
                empty_dir,
                test_file
            ],
            "number_of_files": 1,
            "most_recent": [
                "text"
            ],
            "least_recent": [
                "text"
            ],
            "total_words_number": 1,
            "total_words_length": 4,
            "average_word_length": 4.0,
            "vowel_number": 1,
            "consonant_number": 3
        }
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, info)

    def test_get_files_and_folders_one_query_param(self):
        """Testing that valid folder statistics is returned if one query param
        is specified."""
        self.set_up_file('text')
        client = Client()
        url = convert_to_url('/api/filesystem/' + test_dir)
        query_string = '/?get=files_and_folders'
        url = url + query_string
        info = {
            "files_and_folders": [
                test_dir,
                empty_dir,
                test_file
            ]
        }
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, info)

    def test_get_files_and_folders_multiple_query_param(self):
        """Testing that valid folder statistics is returned if multiple
         query params are specified."""
        self.set_up_file('text')
        client = Client()
        url = convert_to_url('/api/filesystem/' + test_dir)
        query_string = '/?get=files_and_folders,vowel_number'
        url = url + query_string
        info = {
            "files_and_folders": [
                test_dir,
                empty_dir,
                test_file
            ],
            "vowel_number": 1,
        }
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, info)
