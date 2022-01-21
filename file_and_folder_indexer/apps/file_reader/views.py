import os

# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import path


class FileSystem:
    @staticmethod
    def get_objects_list(target_path: str):
        filesystem = [target_path]
        for root, subdirectories, files in os.walk(target_path):
            for subdirectory in subdirectories:
                filesystem.append(os.path.join(root, subdirectory))
            for file in files:
                filesystem.append(os.path.join(root, file))
        return filesystem

    @staticmethod
    def read_file(path: str):
        with open(path, encoding='utf-8') as fi:
            file = fi.read()
        return file


class Converter:
    @staticmethod
    def convert_to_url(path: str):
        url = path.replace(':', '').replace('\\', '/')
        return url

    @staticmethod
    def convert_to_path(url: str):
        index = url.find('/')
        if index > 0:
            path = url[:index] + ':' + url[index:]
            path = path.replace('/', '\\')
        else:
            path = url + ':\\'
        return path


def filesystem_view(request, url_path: path = None):
    if not url_path:
        return HttpResponseNotFound("Specify path to folder, file or word in "
                                    "the text file.")
    path = Converter.convert_to_path(url_path)

    if os.path.isdir(path):
        files = FileSystem.get_objects_list(path)
        return HttpResponse("; ".join(files))
    elif os.path.isfile(path):
        file = FileSystem.read_file(path)
        return HttpResponse(file)
    else:
        return HttpResponseNotFound("No such file or directory.")


if __name__ == '__main__':
    print(Converter.convert_to_url('D:\\Files\\Folder\\Subfolder'))
    print(Converter.convert_to_path('D/Files/Folder/Subfolder'))
