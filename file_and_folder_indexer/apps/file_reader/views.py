import json

from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound)
from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from file_and_folder_indexer.apps.file_reader.conversion import (
    convert_to_path, split_params)
from file_and_folder_indexer.apps.file_reader.indexer import (
    FileSystemException, Statistics, indexate)


@swagger_auto_schema(
    method='get',
    operation_summary="Get statistics about folder, file or word in the text",
    responses={
        '200': 'Ok',
        '400': 'Unable to process the specified path',
        '404': 'Path destination not found',
    }
)
@api_view(['GET'])
def filesystem_view(request, url_path: path = None,):
    """
    Get HTTP response with statistics about folder, file or word in the text.

    If 'get' query parameter is specified:
    Returns only specified in query parameter string types of statistics.
    To specify a number of types of statistics use ';', ',', or ' ' delimiters.

    If no query parameters are specified, returns all types of statistics.

    :param request: Get HTTP request
    :param url_path: Path to check
    :return: Statistics about folder, file or word in the text if path is
    valid, else Bad Request or Not Found error
    """
    if not url_path:
        return HttpResponseBadRequest("Specify path to folder, file or word"
                                      "in the text file.")
    try:
        path = convert_to_path(url_path)
    except ValueError as err:
        return HttpResponseBadRequest(err)

    statistics = Statistics()
    query_params = request.GET.dict()
    if 'get' in query_params:
        params_list = split_params(query_params.get('get'))
        for param in params_list:
            if param in statistics.__dict__:
                setattr(statistics, param, True)

    try:
        statistics = indexate(path, statistics)
        statistics = json.dumps(statistics, indent=4, ensure_ascii=False)
        return HttpResponse(statistics, content_type='application/json')
    except FileSystemException as err:
        return HttpResponseNotFound(err)
