from django.http import JsonResponse
import time


def health_check(request):
    time.sleep(1)
    return JsonResponse(
        {
            "status": "ok",
            "message": "Django API is running.",
        }
    )
