import os


def convert_to_url(path: str) -> str:
    """
    Convert path string to url string
    :param path: Path to convert
    :return: Url string
    """
    url = path.replace(':', '')
    url = url.replace('\\', '/')
    url = url.replace(' ', '%20')
    url = url.replace('%', '%25')
    return url


def convert_to_path(url: str) -> str:
    """
    Convert url string to path string
    :param url: Url to convert
    :return: Path string
    """
    if ':' not in url:
        raise ValueError('No ":" symbol found. Please, specify the absolute'
                         'path to the folder, file or word in the text file.')
    path = os.path.normpath(url + "/")
    return path
