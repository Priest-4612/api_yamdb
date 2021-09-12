from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filt

from rest_framework import viewsets, permissions, filters, serializers, generics
from rest_framework.pagination import PageNumberPagination

from reviews.models import Title, Genre, Category
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer, TitleSerializerRead
from .permissions import IsAdminOrReadOnly


class TitlesFilter(filt.FilterSet):
    category = filt.CharFilter(field_name='category__slug', lookup_expr='icontains')
    genre = filt.CharFilter(field_name='genre__slug', lookup_expr='icontains')
    name = filt.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
#    rating = serializers.SerializerMethodField()
    filter_backends = (DjangoFilterBackend,)
#    filterset_fields = ['genre__slug']#, 'name', 'year','category__slug',)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        # Если запрошенное действие (action) — получение списка объектов ('list')
#        print('11111111111111111', self.action)
        if self.action in ['list', 'retrieve']:
            # ...то применяем CatListSerializer
            return TitleSerializerRead
        # А если запрошенное действие — не 'list', применяем CatSerializer
        return TitleSerializer

    #    def get_rating(self, obj):
#        rating = 9 #Review.objects.filter(title=obj.id).aggregate(Avg('score'))
#        return rating

#    def perform_create(self, serializer):
#        category = serializer.instance.category
#        get_object_or_404(Category, slug=category)
#        for g in serializer.instance.genre:
#            get_object_or_404(Genre, slug=g)
#        serializer.save()


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_fields = ('slug',)


class GenreDestroy(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CategoryDestroy(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
