from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class CategoryUni(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории университета')

    class Meta:
        verbose_name = 'Категорию университета'
        verbose_name_plural = 'Категории университетов'

    def __str__(self):
        return self.title




class Faculty(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название Факультета')


    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

    def __str__(self):
        return self.title




class University(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название Университета')
    description = models.TextField(verbose_name='Описание')
    requirements = models.TextField(verbose_name='Требование для поступление')
    fee = models.CharField(max_length=50, verbose_name='Стоимость обучения')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фото')
    views = models.ManyToManyField('Ip', verbose_name='Просмотры', blank=True, null=True)
    video_link = models.CharField(max_length=500, verbose_name='Видео')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    website_link = models.CharField(max_length=300, verbose_name='Ссылка для сайта институа', blank=True, null=True)
    education_language = models.CharField(max_length=100, verbose_name='Язык обучения')
    faculty = models.ManyToManyField(Faculty, verbose_name='Факультет',)
    category_uni = models.ForeignKey(CategoryUni, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Название категории университета')


    def __str__(self):
        return self.title

    def count_comment(self):
        if self.comment_set.all():
            return self.comment_set.all().count()
        else:
            return 0

    def count_views(self):
        if self.views:
            return self.views.count()
        else:
            return 0

    count_comment.short_description = 'Кол-во комметариев'
    count_views.short_description = 'Просмотры'

    class Meta:
        verbose_name = 'Университет'
        verbose_name_plural = 'Университеты'





class Major(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название учебной направление')
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Учебная направления'
        verbose_name_plural = 'Учебные направлении'

    def __str__(self):
        return self.title




class Program(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название учебной программы')
    description = models.TextField(verbose_name='Описания учебной программы')
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Учебная программа'
        verbose_name_plural = 'Учебные программы'

    def __str__(self):
        return self.title




#
class Comment(models.Model):
    text = models.CharField(max_length=300, verbose_name='Текст комментария')
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name='Университет')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменение')

    def __str__(self):
        return f'Комментарий от {self.author.username} для университета {self.university.title}'

    def get_photo(self):
        try:
            return self.author.profileuser.get_photo()
        except ProfileUser.DoesNotExist:
            return 'https://i.pinimg.com/originals/69/1b/66/691b66ef334e2c8a96ec9a76cd4589b1.jpg'


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'





class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='profile/', verbose_name='Фото профиля', null=True, blank=True)
    is_online = models.BooleanField(default=False, verbose_name='Статус профиля')
    about = models.CharField(max_length=250, verbose_name='О себе', null=True, blank=True)

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://i.pinimg.com/originals/69/1b/66/691b66ef334e2c8a96ec9a76cd4589b1.jpg'

    def count_comment(self):
        if self.user.comment_set.all():
            return self.user.comment_set.all().count()
        else:
            return 0

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'



class Ip(models.Model):
    ip = models.CharField(max_length=100, verbose_name='API посетителей')

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'API посетителя'
        verbose_name_plural = 'API посетителей'
