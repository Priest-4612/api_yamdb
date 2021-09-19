from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


USER_ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
)

FORBIDDEN_USERNAME = [
    'me', 'Me',
    'admin', 'Admin'
]

ERROR_FORBIDDEN_USERNAME = ('Использовать имя "{username}" в качестве '
                            'username запрещено.')


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        max_length=30,
        choices=USER_ROLES,
        default='user'
    )

    class Meta:
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        if self.username in FORBIDDEN_USERNAME and not self.is_superuser:
            raise ValidationError(
                ERROR_FORBIDDEN_USERNAME.format(username=self.username)
            )
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)
