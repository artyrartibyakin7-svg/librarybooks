from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BookForm, LoanForm, ReaderForm
from .models import Book, Loan, Reader


def home(request):
    """Главная страница с общей информацией"""
    total_readers = Reader.objects.count()
    total_books = Book.objects.count()
    active_loans = Loan.objects.filter(status="active").count()

    context = {
        "total_readers": total_readers,
        "total_books": total_books,
        "active_loans": active_loans,
    }
    return render(request, "library/home.html", context)


# Представления аутентификации пользователя
def user_login(request):
    """Представление входа пользователя"""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Проверка, является ли пользователь администратором
            if user.is_staff:
                return redirect(
                    "admin:index"
                )  # Перенаправление администратора в панель администратора Django
            else:
                return redirect(
                    "home"
                )  # Перенаправление обычных пользователей на главную страницу
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    return render(request, "library/login.html")


def user_register(request):
    """Представление регистрации пользователя"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создание профиля читателя для пользователя
            Reader.objects.create(
                user=user,
                first_name=user.first_name if user.first_name else "",
                last_name=user.last_name if user.last_name else "",
                email=user.email
                if user.email
                else f"{user.username}@example.com",  # Обеспечение уникальности электронной почты
                phone="",
                address="",
                registration_date=timezone.now().date(),
            )
            username = form.cleaned_data.get("username")
            messages.success(request, f"Учетная запись создана для {username}!")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "library/register.html", {"form": form})


def user_logout(request):
    """Представление выхода пользователя"""
    logout(request)
    messages.success(request, "Вы вышли из системы.")
    return redirect("home")


@login_required
def user_profile(request):
    """Представление профиля пользователя"""
    reader = Reader.objects.filter(user=request.user).first()
    if request.method == "POST":
        # Обновление информации пользователя
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.save()

        # Обновление информации читателя
        if reader:
            reader.first_name = user.first_name
            reader.last_name = user.last_name
            reader.email = user.email
            reader.phone = request.POST.get("phone", reader.phone)
            reader.address = request.POST.get("address", reader.address)
            reader.save()

        messages.success(request, "Профиль успешно обновлен!")
        return redirect("user_profile")

    context = {
        "reader": reader,
    }
    return render(request, "library/profile.html", context)


@login_required
def change_password(request):
    """Представление изменения пароля"""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Важно!
            messages.success(request, "Ваш пароль был успешно обновлен!")
            return redirect("user_profile")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибку ниже.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "library/change_password.html", {"form": form})


# Представления читателя
@login_required
def reader_list(request):
    """Список всех читателей"""
    # Только администраторы могут просматривать всех читателей
    if not request.user.is_staff:
        messages.error(request, "У вас нет разрешения на просмотр этой страницы.")
        return redirect("home")

    readers = Reader.objects.all()
    return render(request, "library/reader_list.html", {"readers": readers})


@login_required
def reader_detail(request, pk):
    """Просмотр деталей читателя"""
    # Только администраторы могут просматривать детали читателя
    if not request.user.is_staff:
        messages.error(request, "У вас нет разрешения на просмотр этой страницы.")
        return redirect("home")

    reader = get_object_or_404(Reader, pk=pk)
    loans = Loan.objects.filter(reader=reader)
    return render(
        request, "library/reader_detail.html", {"reader": reader, "loans": loans}
    )


@login_required
def reader_add(request):
    """Добавление нового читателя"""
    # Только администраторы могут добавлять читателей
    if not request.user.is_staff:
        messages.error(request, "У вас нет разрешения на выполнение этого действия.")
        return redirect("home")

    if request.method == "POST":
        form = ReaderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Читатель успешно добавлен!")
            return redirect("reader_list")
    else:
        form = ReaderForm()
    return render(
        request,
        "library/reader_form.html",
        {"form": form, "title": "Добавить читателя"},
    )


@login_required
def reader_edit(request, pk):
    """Редактирование информации читателя"""
    # Только администраторы могут редактировать читателей
    if not request.user.is_staff:
        messages.error(request, "У вас нет разрешения на выполнение этого действия.")
        return redirect("home")

    reader = get_object_or_404(Reader, pk=pk)
    if request.method == "POST":
        form = ReaderForm(request.POST, instance=reader)
        if form.is_valid():
            form.save()
            messages.success(request, "Информация о читателе успешно обновлена!")
            return redirect("reader_detail", pk=reader.pk)
    else:
        form = ReaderForm(instance=reader)
    return render(
        request,
        "library/reader_form.html",
        {"form": form, "title": "Редактировать читателя", "reader": reader},
    )


@login_required
def reader_delete(request, pk):
    """Удаление читателя"""
    # Только администраторы могут удалять читателей
    if not request.user.is_staff:
        messages.error(request, "У вас нет разрешения на выполнение этого действия.")
        return redirect("home")

    reader = get_object_or_404(Reader, pk=pk)
    if request.method == "POST":
        reader.delete()
        messages.success(request, "Читатель успешно удален!")
        return redirect("reader_list")
    return render(request, "library/reader_confirm_delete.html", {"reader": reader})


# Представления книги
@login_required
def book_list(request):
    """Список всех книг"""
    books = Book.objects.all()
    return render(request, "library/book_list.html", {"books": books})


@login_required
def book_detail(request, pk):
    """Просмотр деталей книги"""
    book = get_object_or_404(Book, pk=pk)
    loans = Loan.objects.filter(book=book)
    return render(request, "library/book_detail.html", {"book": book, "loans": loans})


@login_required
def book_add(request):
    """Добавление новой книги"""
    # Только администраторы могут добавлять книги
    if not request.user.is_staff:
        messages.error(request, "У вас нет разрешения на выполнение этого действия.")
        return redirect("home")

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Книга успешно добавлена!")
            return redirect("book_list")
    else:
        form = BookForm()
    return render(
        request, "library/book_form.html", {"form": form, "title": "Добавить книгу"}
    )


@login_required
def book_edit(request, pk):
    """Редактирование информации книги"""
    # Только администраторы могут редактировать книги
    if not request.user.is_staff:
        messages.error(request, "У вас нет разрешения на выполнение этого действия.")
        return redirect("home")

    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Информация о книге успешно обновлена!")
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(
        request,
        "library/book_form.html",
        {"form": form, "title": "Редактировать книгу", "book": book},
    )


@login_required
def book_delete(request, pk):
    """Удаление книги"""
    # Только администраторы могут удалять книги
    if not request.user.is_staff:
        messages.error(request, "У вас нет разрешения на выполнение этого действия.")
        return redirect("home")

    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Книга успешно удалена!")
        return redirect("book_list")
    return render(request, "library/book_confirm_delete.html", {"book": book})


# Представления выдачи
@login_required
def loan_list(request):
    """Список всех выдач"""
    # Обычные пользователи могут видеть только свои собственные выдачи
    if request.user.is_staff:
        loans = Loan.objects.all()
    else:
        reader = Reader.objects.filter(user=request.user).first()
        if reader:
            loans = Loan.objects.filter(reader=reader)
        else:
            loans = Loan.objects.none()
    return render(request, "library/loan_list.html", {"loans": loans})


@login_required
def loan_active(request):
    """Просмотр активных выдач"""
    # Обычные пользователи могут видеть только свои собственные активные выдачи
    if request.user.is_staff:
        loans = Loan.objects.filter(status="active")
    else:
        reader = Reader.objects.filter(user=request.user).first()
        if reader:
            loans = Loan.objects.filter(reader=reader, status="active")
        else:
            loans = Loan.objects.none()
    return render(
        request, "library/loan_list.html", {"loans": loans, "title": "Активные выдачи"}
    )


@login_required
def loan_history(request):
    """Просмотр истории выдач"""
    # Обычные пользователи могут видеть только свою собственную историю выдач
    if request.user.is_staff:
        loans = Loan.objects.exclude(status="active")
    else:
        reader = Reader.objects.filter(user=request.user).first()
        if reader:
            loans = Loan.objects.filter(reader=reader).exclude(status="active")
        else:
            loans = Loan.objects.none()
    return render(
        request, "library/loan_list.html", {"loans": loans, "title": "История выдач"}
    )


@login_required
def loan_add(request):
    """Выдача книги читателю"""
    # Обычные пользователи могут выдавать книги только себе
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)

            # Если обычный пользователь, установить читателя на себя
            if not request.user.is_staff:
                reader = Reader.objects.filter(user=request.user).first()
                if not reader:
                    messages.error(request, "Профиль читателя не найден.")
                    return redirect("loan_list")
                loan.reader = reader

            # Проверка наличия доступных копий книги
            if loan.book.available_copies > 0:
                # Уменьшение доступных копий
                loan.book.available_copies -= 1
                loan.book.save()
                loan.save()
                messages.success(request, "Книга успешно выдана!")
                return redirect("loan_list")
            else:
                messages.error(request, "Нет доступных копий этой книги.")
    else:
        form = LoanForm()
        # Если обычный пользователь, ограничить выбор читателя только собой
        if not request.user.is_staff:
            reader = Reader.objects.filter(user=request.user).first()
            if reader:
                form.fields["reader"].choices = [(reader.id, str(reader))]
                form.fields["reader"].initial = reader.id
    return render(
        request, "library/loan_form.html", {"form": form, "title": "Выдать книгу"}
    )


@login_required
def loan_return(request, pk):
    """Возврат книги от читателя"""
    loan = get_object_or_404(Loan, pk=pk)

    # Обычные пользователи могут возвращать только свои собственные книги
    if not request.user.is_staff:
        reader = Reader.objects.filter(user=request.user).first()
        if not reader or loan.reader != reader:
            messages.error(request, "У вас нет разрешения на возврат этой книги.")
            return redirect("loan_list")

    if request.method == "POST":
        # Установка даты возврата и статуса
        loan.return_date = timezone.now().date()
        loan.status = "returned"
        # Увеличение доступных копий
        loan.book.available_copies += 1
        loan.book.save()
        loan.save()
        messages.success(request, "Книга успешно возвращена!")
        return redirect("loan_list")
    return render(request, "library/loan_confirm_return.html", {"loan": loan})
