from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


USER_ROLES = (
    ('u', 'user'),
    ('m', 'moderator'),
    ('a', 'admin')
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
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=50, #FIXIT<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        default='user' #FIXIT<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    )

    def save(self, *args, **kwargs):
        if self.username in FORBIDDEN_USERNAME and not self.is_superuser:
            raise ValidationError(
                ERROR_FORBIDDEN_USERNAME.format(username=self.username)
            )
        if self.is_superuser:
            self.role = 'admin' #FIXIT<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        if self.role == USER_ROLES[2] or self.is_superuser:
            return True

    @property
    def is_moderator(self):
        if self.role == USER_ROLES[1] or self.is_superuser:
            return True

    class Meta:
        ordering = (
            '-username',
        )