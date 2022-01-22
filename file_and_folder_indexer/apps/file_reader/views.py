import json
import os

# from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound)
from django.urls import path

from file_and_folder_indexer.apps.file_reader.convertation import (
    convert_to_path, convert_to_url)
from file_and_folder_indexer.apps.file_reader.indexer import (
    get_objects_list, get_word_statistics, read_file)


def filesystem_view(request, url_path: path = None):
    """
    Get HTTP response with statistics about folder, file or word in the text
    :param request: Get HTTP request
    :param url_path: Path to check
    :return: Statistics about folder, file or word in the text if path is
    valid, else Bad Request or Not Found error
    """
    allowed_extensions = [".txt", ".md", ".docx", ""]
    if not url_path:
        return HttpResponseBadRequest("Specify path to folder, file or word"
                                      "in the text file.")
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
    elif os.path.isfile(os.path.dirname(path)):
        word = path.split("\\")[-1]
        info = get_word_statistics(word)
        info = json.dumps(info, indent=4, ensure_ascii=False)
        return HttpResponse(info)
    return HttpResponseNotFound("No such file or directory.")
