from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10, 'Рейтинг не может быть выше 10'),
            MinValueValidator(1),
        ],
        null=True,
        verbose_name="Рейтинг",
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10, 'Максимальная оценка - 10'),
            MinValueValidator(1, 'Минимальная оценка - 1'),
        ],
    )

    class Meta:
        ordering = (
            '-pub_date',
        )
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_following'),
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = (
            '-pub_date',
        )
