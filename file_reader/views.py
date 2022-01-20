import os

# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import path


class FileSystem:
    target_path = 'D:\\Files'
    target_path = target_path.split(':')[1]
    if not target_path:
        pass    # Invalid path

    @staticmethod
    def get_objects_list():
        filesystem = [FileSystem.target_path]
        for root, subdirectories, files in os.walk(FileSystem.target_path):
            for subdirectory in subdirectories:
                filesystem.append(os.path.join(root, subdirectory))
            for file in files:
                filesystem.append(os.path.join(root, file))
        return filesystem

    @staticmethod
    def setup(path: str):
        FileSystem.target_path = path


class Converter:
    @staticmethod
    def convert_to_url(path: str):
        url = path.replace(':', '').replace('\\', '/')
        return url

    @staticmethod
    def convert_to_path(url: str):
        index = url.find('/')
        path = url[:index] + ':' + url[index:]
        path = path.replace('/', '\\')
        return path


def filesystem_view(request, url_path: path = None):
    paths = FileSystem.get_objects_list()
    paths = [Converter.convert_to_url(path) for path in paths]

    if not url_path:
        return HttpResponse(";".join(paths))
    url_path = "/" + url_path

    if url_path not in paths:
        return HttpResponseNotFound('Invalid filepath.')

    return HttpResponse('File or folder page.')


if __name__ == '__main__':
    print(Converter.convert_to_url('D:\\Files\\Folder\\Subfolder'))
    print(Converter.convert_to_path('D/Files/Folder/Subfolder'))
