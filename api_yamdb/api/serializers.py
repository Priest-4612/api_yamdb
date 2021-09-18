from rest_framework import serializers

from django.db.models import Avg
from django.shortcuts import get_object_or_404

import datetime as dt

from reviews.models import Comment, Review, Category, Genre, Title
from users.models import User # FIXIT<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='pk', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context.get('view').kwargs.get('title_id')
        if (Review.objects.filter(author=author, title=title_id).exists()
                and self.context['request'].method != 'PATCH'):
            raise serializers.ValidationError('Вы уже оставляли отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True,)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment

        
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('slug', 'name')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('slug', 'name')


class TitleSerializerRead(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    # ЗАГОТОВКА ДЛЯ ВЫЧИСЛЕНИЯ РЕЙТИНГА ПРОИЗВЕДЕНИЯ    
#    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('__all__')

    # ЗАГОТОВКА ДЛЯ ВЫЧИСЛЕНИЯ РЕЙТИНГА ПРОИЗВЕДЕНИЯ
#    def get_rating(self, obj):
#        title = get_object_or_404(Title, id=obj.id)
#        rating = round(title.reviews.all().aggregate(Avg('score'))['score__avg'])
#        return rating


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), required=False, slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), required=False, slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('__all__')

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Проверьте год издания произведения!'
            )
        return value

# FIXITvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'role')

