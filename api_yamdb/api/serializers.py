from rest_framework import serializers

import datetime as dt

from reviews.models import Comment, Review, Category, Genre, Title
from users.models import User # FIXIT<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='pk', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'rating', 'pub_date', 'title')
        model = Review

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context.get('title_id')
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

    class Meta:
        model = Title
        fields = ('__all__')


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
        fields = ('username', 'email')
