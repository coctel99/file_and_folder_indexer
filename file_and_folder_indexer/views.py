from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the index page.")


def api(request):
    return HttpResponse("Api page.")
