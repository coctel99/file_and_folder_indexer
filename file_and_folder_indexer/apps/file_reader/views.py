import os
import json

# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import path

from file_and_folder_indexer.apps.file_reader.convertation import (
    convert_to_path, convert_to_url)
from file_and_folder_indexer.apps.file_reader.indexer import (get_objects_list,
                                                              read_file)


def filesystem_view(request, url_path: path = None):
    allowed_extensions = [".txt", ".md", ".docx", ""]
    if not url_path:
        return HttpResponseNotFound("Specify path to folder, file or word in "
                                    "the text file.")
    path = convert_to_path(url_path)

    if os.path.isdir(path):
        files = get_objects_list(path)
        return HttpResponse("; ".join(files))
    elif os.path.isfile(path):
        file_ext = os.path.splitext(path)[1]
        if file_ext in allowed_extensions:
            info = read_file(path)
            info = json.dumps(info, indent=4, ensure_ascii=False)
            return HttpResponse(info)
        return HttpResponseNotFound("File extension is not in allowed "
                                    "extensions list.")
    else:
        return HttpResponseNotFound("No such file or directory.")


if __name__ == '__main__':
    print(convert_to_url('D:\\Files\\Folder\\Subfolder'))
    print(convert_to_path('D/Files/Folder/Subfolder'))
    print(convert_to_url('D:\\Files\\Folder\\File+Name%20n'))
