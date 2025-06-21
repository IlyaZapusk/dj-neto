from django.urls import path
from articles.views import articles_list, students_list

urlpatterns = [
    path('', articles_list, name='articles'),
    path('students/', students_list, name='students'),
]
