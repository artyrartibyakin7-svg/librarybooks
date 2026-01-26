from django.contrib.auth.models import User
from django.db import models


class Reader(models.Model):
    """Модель читателя, представляющая пользователя библиотеки"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(
        max_length=254, verbose_name="Электронная почта", unique=True
    )
    phone = models.CharField(
        max_length=20, verbose_name="Телефон", null=True, blank=True, unique=True
    )
    address = models.CharField(
        max_length=255, verbose_name="Адрес", null=True, blank=True
    )
    registration_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"
        ordering = ["last_name", "first_name"]


class Book(models.Model):
    """Модель книги в библиотеке"""

    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=200, verbose_name="Автор")
    isbn = models.CharField(max_length=13, verbose_name="ISBN", unique=True)
    publication_date = models.DateField(verbose_name="Дата публикации")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    total_copies = models.IntegerField(verbose_name="Количество экземпляров")
    available_copies = models.IntegerField(verbose_name="Доступные экземпляры")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["title"]


class Loan(models.Model):
    """Модель выдачи книги"""

    STATUS_CHOICES = [
        ("overdue", "Просрочена"),
        ("active", "Активная"),
        ("returned", "Возвращена"),
    ]

    reader = models.ForeignKey(
        Reader, on_delete=models.CASCADE, verbose_name="Читатель"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    loan_date = models.DateField(verbose_name="Дата выдачи книги")
    due_date = models.DateField(verbose_name="Срок возврата книги")
    return_date = models.DateField(
        verbose_name="Дата возврата книги", null=True, blank=True
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="active", verbose_name="Статус"
    )

    def __str__(self):
        return (
            f"{self.book.title} взято {self.reader.first_name} {self.reader.last_name}"
        )

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"
        ordering = ["return_date"]
