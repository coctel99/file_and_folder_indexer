# Api for indexing files and folders

## Description:

API is designed to get statistics about a folder, a textfile or a word in
the text file through the HTTP GET request by specifying a path to the 
desired data.

### Gathered statistics

For the specified word in specified textfile:
1) Times in text
2) Vowel number
3) Consonant number

For the specified textfile:
1) Most recent words
2) Least recent words
3) Total words number
4) Total words length
5) Average word length
6) Number of all vowels in text
7) Number of all consonants in text

For the specified folder:
1) List of files and subfolders
2) Number of files
3) Most recent words
4) Least recent words
5) Total words number
6) Total words length
7) Average word length
8) Number of all vowels in text
9) Number of all consonants in text

## Technical information

Changing File Reader settings is not recommended and can result into
crashes and errors!

Settings are specified in 
*'.\file_and_folder_indexer\apps\file_reader\apps.py'*

### Change list of readable file extensions

By default, only *'.txt'* files are read, but other file extensions
could be specified in *allowed_file_extensions* parameter

### Change list of readable file encodings

Application is trying to open a file with different encoding settings
until it gets opened starting from the left one and going to the right
in the *'encodings_queue'* list.

Default encodings queue: [*'utf-8'*, *'Windows-1251'*, *'cp932'*, *'big5'*]

*Note: utf-8 is suitable for most number of textfiles: both English and 
Russian, Windows-1251 can open some Russian language files where utf-8
gives error, cp932 can open most of Japanese language files
and big5 is one of Chinese files encoding.*

## Installation

1) Download or Pull project code
2) Create virtual environment in the project root
3) Activate virtual environment
4) Run *python manage.py migrate* to apply basic Django migrations
5) Run *python manage.py createsuperuser* and set Login and Password 
to create a Django admin user
6) Run *python manage.py runserver*

## Endpoints

Currently, there are 2 endpoints in the project

### Statistics endpoint
Get HTTP response with statistics about folder, file or word in the
textfile.

If 'get' query parameter is specified:
Returns only specified in query parameter string types of statistics.
To specify a number of types of statistics use ';', ',', or ' ' delimiters.

If no query parameters are specified, returns all types of statistics.

*url_path*: Path to check (str)<br>
*query_params*: Types of statistics (str)

To get all statistics: 

    /api/filesystem/{url_path}/

To get only specified types of statistics: 

    /api/filesystem/{url_path}/?get={query_params}/

#### Examples:
To get all information about specified folder:
http://127.0.0.1:8000/api/filesystem/D:/Files/

To get only number of files and total number of words in files of
specified folder:
http://127.0.0.1:8000/api/filesystem/D:/Files/?get=number_of_files,total_words_number

To get all information about specified file:
http://127.0.0.1:8000/api/filesystem/D:/Files/Folder/File.txt/

To get information, how many times specified word meets in text file:
http://127.0.0.1:8000/api/filesystem/D:/Files/Folder/File.txt/text/?get=times_in_text

### Swagger UI endpoint

Swagger UI URL address:

    /swagger/

### Additional information

Django server secret key is sored in .env file