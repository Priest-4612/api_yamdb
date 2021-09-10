from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, filters, serializers, generics
from rest_framework.pagination import PageNumberPagination

from reviews.models import Title, Genre, Category
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from .permissions import IsAdminOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    rating = serializers.SerializerMethodField()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_rating(self, obj):
        rating = 9 #Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        return rating

    def perform_create(self, serializer):
        category = serializer.instance.category
        get_object_or_404(Category, slug=category)
        for g in serializer.instance.genre:
            get_object_or_404(Genre, slug=g)
        serializer.save()


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)


class GenreDestroy(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)


class CategoryDestroy(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
