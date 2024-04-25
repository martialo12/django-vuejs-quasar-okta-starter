from django.http import JsonResponse
from django.views.generic import RedirectView


def healthz(request):
    return JsonResponse({"status": "ok"})


class AdminLoginView(RedirectView):
    def get_redirect_url(self) -> str:
        return self.request.build_absolute_uri("/login")
