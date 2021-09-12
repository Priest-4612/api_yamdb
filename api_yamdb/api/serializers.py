from rest_framework import serializers

import datetime as dt

from reviews.models import Category, Genre, Title


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
#    genre = serializers.SlugRelatedField(
#        slug_field='slug', read_only=True, many=True
#        queryset=Genre.objects.all(), many=True, required=False, slug_field='slug'
#    )
    category = CategorySerializer()
#    category = serializers.SlugRelatedField(
#        slug_field='slug', read_only=True
#        queryset=Category.objects.all(), required=False, slug_field='slug'
#    )

    class Meta:
        model = Title
        fields = ('__all__')



class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
#        slug_field='slug', read_only=True, many=True
        queryset=Genre.objects.all(), many=True, required=False, slug_field='slug'
    )
    category = serializers.SlugRelatedField(
#        slug_field='slug', read_only=True
        queryset=Category.objects.all(), required=False, slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('__all__')

#    def perform_create(self, serializer):
#        print('11111111111111111111111111 ->', serializer)
#        serializer.save(category='jazz')

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год издания произведения!')
        return value
# FIXIT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#    def create(self, validated_data):
#        category = Category.objects.get(slug=validated_data['category'].slug
#        print('111111111111111111111111111111111111111111', type(validated_data['category']))
#        validated_data['category'] = category
#        print('22222222222222222222222222', type(validated_data['category']))
#        validated_data['category'] == validated_data['category'].slug
#        title = Title.objects.create()
#        return validated_data


