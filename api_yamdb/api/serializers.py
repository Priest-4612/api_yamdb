from rest_framework import serializers

import datetime as dt

from reviews.models import Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', read_only=True, many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', read_only=True, many=True
    )

    class Meta:
        model = Title
        fields = ('__all__') #('id', 'genre', 'category', 'name', 'year', 'description')

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год издания произведения!')
        return value

    def create(self, validated_data):
        title = Title.objects.create(**validated_data)
        return title 


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug', 'titles')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
