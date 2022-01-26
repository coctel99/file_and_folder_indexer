from django.http import HttpResponseNotFound
from rest_framework.decorators import api_view


@api_view(['GET'])
def api(request):
    return HttpResponseNotFound()
