import json
import os

from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound)
from django.urls import path

from file_and_folder_indexer.apps.file_reader.apps import FileReaderConfig
from file_and_folder_indexer.apps.file_reader.convertation import \
    convert_to_path
from file_and_folder_indexer.apps.file_reader.indexer import (
    get_file_statistics, get_folder_statistics, get_word_statistics)


def filesystem_view(request, url_path: path = None):
    """
    Get HTTP response with statistics about folder, file or word in the text
    :param request: Get HTTP request
    :param url_path: Path to check
    :return: Statistics about folder, file or word in the text if path is
    valid, else Bad Request or Not Found error
    """
    if not url_path:
        return HttpResponseBadRequest("Specify path to folder, file or word"
                                      "in the text file.")
    path = convert_to_path(url_path)

    if os.path.isdir(path):
        info = get_folder_statistics(path)
        info = json.dumps(info, indent=4, ensure_ascii=False)
        return HttpResponse(info, content_type='application/json')
    elif os.path.isfile(path):
        file_ext = os.path.splitext(path)[1]
        if file_ext in FileReaderConfig.allowed_file_extensions:
            info = get_file_statistics(path)
            info = json.dumps(info, indent=4, ensure_ascii=False)
            return HttpResponse(info, content_type='application/json')
        return HttpResponseNotFound("File extension is not in allowed "
                                    "extensions list.")
    elif os.path.isfile(os.path.dirname(path)):
        word = path.split("\\")[-1]
        info = get_word_statistics(word)
        info = json.dumps(info, indent=4, ensure_ascii=False)
        return HttpResponse(info, content_type='application/json')
    return HttpResponseNotFound("No such file or directory.")
