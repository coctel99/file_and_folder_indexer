def convert_to_url(path: str) -> str:
    url = path.replace(':', '')
    url = url.replace('\\', '/')
    url = url.replace(' ', '%20')
    url = url.replace('%', '%25')
    return url


def convert_to_path(url: str) -> str:
    index = url.find('/')
    if index > 0:
        path = url[:index] + ':' + url[index:]
        path = path.replace('/', '\\')
    # If is a disk root
    else:
        path = url + ':\\'
    return path
