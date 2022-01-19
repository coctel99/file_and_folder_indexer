from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the index page.")


def api(request):
    return HttpResponse("Api page.")


def file(request, path: str = None):
    if not path:
        return HttpResponse("Files tree page.   ")
    return HttpResponse("File page.")
