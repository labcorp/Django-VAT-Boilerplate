from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.template import loader


class Home(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        salame = False
        return super().get(request, *args, **kwargs)

