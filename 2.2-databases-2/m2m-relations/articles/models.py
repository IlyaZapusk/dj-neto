from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО учителя')
    subject = models.CharField(max_length=100, verbose_name='Предмет')

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО ученика')
    teachers = models.ManyToManyField('Teacher', related_name='students', verbose_name='Учителя')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Раздел')

    class Meta:
        ordering = ['name']
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    tags = models.ManyToManyField(Tag, through='Scope', related_name='articles', verbose_name='Разделы')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Scope(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Раздел')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        ordering = ['-is_main', 'tag__name']
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'

    def __str__(self):
        return f'{self.article} — {self.tag} ({ "основной" if self.is_main else "доп." })'
