from django.shortcuts import render
from articles.models import Article, Student

def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'
    articles = Article.objects.all().order_by(ordering)
    context = {'object_list': articles}
    return render(request, template, context)


def students_list(request):
    template = 'articles/students_list.html'
    students = Student.objects.prefetch_related('teachers').all()
    context = {'students': students}
    return render(request, template, context)
