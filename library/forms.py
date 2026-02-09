from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Book, Loan, Reader


class ReaderForm(forms.ModelForm):
    """Форма для создания и редактирования читателя"""

    class Meta:
        model = Reader
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
        ]

        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Электронная почта",
            "phone": "Телефон",
            "address": "Адрес",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Проверка, является ли это операцией обновления
        if self.instance.pk:
            if Reader.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError(
                    "Читатель с таким адресом электронной почты уже существует."
                )
        else:
            if Reader.objects.filter(email=email).exists():
                raise ValidationError(
                    "Читатель с таким адресом электронной почты уже существует."
                )
        return email


from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Book, Loan, Reader


class ReaderForm(forms.ModelForm):
    """Форма для создания и редактирования читателя"""

    class Meta:
        model = Reader
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
        ]

        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Электронная почта",
            "phone": "Телефон",
            "address": "Адрес",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Проверка, является ли это операцией обновления
        if self.instance.pk:
            if Reader.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError(
                    "Читатель с таким адресом электронной почты уже существует."
                )
        else:
            if Reader.objects.filter(email=email).exists():
                raise ValidationError(
                    "Читатель с таким адресом электронной почты уже существует."
                )
        return email


class BookForm(forms.ModelForm):
    """Форма для создания и редактирования книги"""

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "isbn",
            "publication_date",
            "genre",
            "total_copies",
        ]
        widgets = {
            "publication_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "title": "Название",
            "author": "Автор",
            "isbn": "ISBN",
            "publication_date": "Дата публикации",
            "genre": "Жанр",
            "total_copies": "Общее количество копий",
        }

    def clean_isbn(self):
        isbn = self.cleaned_data.get("isbn")
        # Проверка, является ли это операцией обновления
        if self.instance.pk:
            if Book.objects.filter(isbn=isbn).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Книга с таким ISBN уже существует.")
        else:
            if Book.objects.filter(isbn=isbn).exists():
                raise ValidationError("Книга с таким ISBN уже существует.")
        return isbn

    def clean_publication_date(self):
        publication_date = self.cleaned_data.get("publication_date")
        if publication_date and publication_date > timezone.now().date():
            raise ValidationError("Дата публикации не может быть в будущем.")
        return publication_date

    def clean_total_copies(self):
        total_copies = self.cleaned_data.get("total_copies")
        if total_copies < 1:
            raise ValidationError("Общее количество копий должно быть не менее 1.")
        return total_copies


class LoanForm(forms.ModelForm):
    """Форма для создания выдачи книги"""

    class Meta:
        model = Loan
        fields = ["reader", "book", "loan_date", "due_date"]
        widgets = {
            "loan_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "reader": "Читатель",
            "book": "Книга",
            "loan_date": "Дата выдачи",
            "due_date": "Срок возврата",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показывать только книги с доступными копиями
        self.fields["book"].queryset = Book.objects.filter(available_copies__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        loan_date = cleaned_data.get("loan_date")
        due_date = cleaned_data.get("due_date")

        if loan_date and due_date and due_date <= loan_date:
            raise ValidationError("Срок возврата должен быть после даты выдачи.")

        return cleaned_data

    def clean_loan_date(self):
        loan_date = self.cleaned_data.get("loan_date")
        if loan_date and loan_date > timezone.now().date():
            raise ValidationError("Дата выдачи не может быть в будущем.")
        return loan_date


class LoanForm(forms.ModelForm):
    """Форма для создания выдачи книги"""

    class Meta:
        model = Loan
        fields = ["reader", "book", "loan_date", "due_date"]
        widgets = {
            "loan_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "reader": "Читатель",
            "book": "Книга",
            "loan_date": "Дата выдачи",
            "due_date": "Срок возврата",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показывать только книги с доступными копиями
        self.fields["book"].queryset = Book.objects.filter(available_copies__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        loan_date = cleaned_data.get("loan_date")
        due_date = cleaned_data.get("due_date")

        if loan_date and due_date and due_date <= loan_date:
            raise ValidationError("Срок возврата должен быть после даты выдачи.")

        return cleaned_data

    def clean_loan_date(self):
        loan_date = self.cleaned_data.get("loan_date")
        if loan_date and loan_date > timezone.now().date():
            raise ValidationError("Дата выдачи не может быть в будущем.")
        return loan_date
