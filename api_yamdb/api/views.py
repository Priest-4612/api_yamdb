from django_filters import rest_framework as filt

from rest_framework import viewsets, filters, generics
from rest_framework.pagination import PageNumberPagination

from reviews.models import Title, Genre, Category
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleSerializer,
    TitleSerializerRead,
)
from .permissions import IsAdminOrReadOnly


class TitlesFilter(filt.FilterSet):
    category = filt.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains',
    )
    genre = filt.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains',
    )
    name = filt.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
# ЗАГОТОВКА ДЛЯ ВЫЧИСЛЕНИЯ РЕЙТИНГА ПРОИЗВЕДЕНИЯ    
#    rating = serializers.SerializerMethodField()
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializerRead
        return TitleSerializer

# ЗАГОТОВКА ДЛЯ ВЫЧИСЛЕНИЯ РЕЙТИНГА ПРОИЗВЕДЕНИЯ
#     def get_rating(self, obj):
#         rating = 9 #Review.objects.filter(title=obj.id).aggregate(Avg('score'))
#         return rating


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
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


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
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
