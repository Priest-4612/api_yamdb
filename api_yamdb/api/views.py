from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.db.models import Avg
from django.shortcuts import get_object_or_404

from reviews.models import Review, Title
from .permissions import IsAdminOrMod
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrMod, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def rating_calculation(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, title=title)
        title.rating = (Review.objects.filter(title=title).aggregate(Avg(
            'score'))['score__avg'])
        title.save(update_fields=['rating'])

    def perform_create(self, serializer):
        self.rating_calculation(serializer)

    def perform_update(self, serializer):
        self.rating_calculation(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrMod, IsAuthenticatedOrReadOnly]

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
