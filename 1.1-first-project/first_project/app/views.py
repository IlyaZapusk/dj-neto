import os


from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from django.urls import reverse


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir'),
    }

    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    files = os.listdir()
    formatted = "<br>".join(files)
    return HttpResponse(f"Содержимое рабочей директории:<br>{formatted}")
