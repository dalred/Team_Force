from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

def root(request: WSGIRequest) -> JsonResponse:
    return JsonResponse({
        "status": "ok"
    })