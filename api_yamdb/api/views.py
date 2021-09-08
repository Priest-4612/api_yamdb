from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, permissions, filters, serializers
from rest_framework.pagination import PageNumberPagination

from reviews.models import Title, Genre, Category
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    rating = serializers.SerializerMethodField()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    pagination_class = PageNumberPagination

    def get_rating(self, obj):
        rating = 10 #Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        return rating


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
