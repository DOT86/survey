from django.contrib import admin
from authors.models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'patronymic_name')
    list_filter = ('user',)
    ordering = ('user',)
