from django.contrib import admin

from .models import Book, Loan, Reader

admin.site.register(Reader)
admin.site.register(Book)
admin.site.register(Loan)
