from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Главная страница
    path("", views.home, name="home"),
    # URL-адреса аутентификации пользователя
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    # URL-адреса профиля пользователя
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/change-password/", views.change_password, name="change_password"),
    # URL-адреса читателя
    path("readers/", views.reader_list, name="reader_list"),
    path("readers/add/", views.reader_add, name="reader_add"),
    path("readers/<int:pk>/", views.reader_detail, name="reader_detail"),
    path("readers/<int:pk>/edit/", views.reader_edit, name="reader_edit"),
    path("readers/<int:pk>/delete/", views.reader_delete, name="reader_delete"),
    # URL-адреса книги
    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.book_add, name="book_add"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/<int:pk>/edit/", views.book_edit, name="book_edit"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    # URL-адреса выдачи
    path("loans/", views.loan_list, name="loan_list"),
    path("loans/add/", views.loan_add, name="loan_add"),
    path("loans/<int:pk>/return/", views.loan_return, name="loan_return"),
    path("loans/active/", views.loan_active, name="loan_active"),
    path("loans/history/", views.loan_history, name="loan_history"),
]
