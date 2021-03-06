import os
import re
from typing import List


def convert_to_url(path: str) -> str:
    """
    Convert path string to url string
    :param path: Path to convert
    :return: Url string
    """
    url = path.replace('\\', '/')
    url = url.replace(' ', '%20')
    url = url.replace('%', '%25')
    return url


def convert_to_path(url: str) -> str:
    """
    Convert url string to path string
    :param url: Url to convert
    :return: Path string
    """
    path = os.path.normpath(url + "/")
    return path


def split_params(params_str: str) -> List:
    """
    Split URL query string into a list of parameters
    :param params_str: URL query string
    :return: List of parameters
    """
    separators = '[;, ]'
    params_list = re.split(separators, params_str)
    if params_list.count(""):
        params_list.remove("")
    return params_list
