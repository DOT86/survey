from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class Author(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        _('First name'),
        max_length=30,
    )
    last_name = models.CharField(
        _('Last name'),
        max_length=40,
    )
    patronymic_name = models.CharField(
        _('Patronymic name'),
        max_length=50,
        blank=True,
        null = True,
    )
    email = models.EmailField(
        _('Email'),
        max_length=254,
        blank=True,
    )
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True,
        db_index=True,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        _('Updated At'),
        auto_now=True,
        db_index=True,
        null=True,
        blank=True,
    )


    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
