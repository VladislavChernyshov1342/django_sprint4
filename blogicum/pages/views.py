from django.shortcuts import render
from django.views.generic import TemplateView

# View функции были заменены на view CBV.


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'
