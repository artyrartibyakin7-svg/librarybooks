from django.db import models

from django.contrib.auth.models import User

class Reader(models.Model):
    """Модель читателя, представляющая пользователя библиотеки"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(max_length=254, verbose_name='Электронная почта', unique=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True, unique=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
        ordering = ['last_name', 'first_name']
