from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]
    FORBIDDEN_USERNAME = [
        'me', 'Me',
        'admin', 'Admin'
    ]
    ERROR_FORBIDDEN_USERNAME = ('Использовать имя "{username}" в качестве '
                                'username запрещено.')

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(

        max_length=30,
        choices=USER_ROLES_CHOICES,
        default=USER
    )

    class Meta:
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        if self.username in self.FORBIDDEN_USERNAME and not self.is_superuser:
            raise ValidationError(
                self.ERROR_FORBIDDEN_USERNAME.format(username=self.username)
            )
        if self.is_superuser:

            self.role = self.ADMIN
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_superuser

    class Meta:
        ordering = (
            '-username',
        )
