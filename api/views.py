from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer

# Create your views here.


class PostList(generics.ListCreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class PostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], posted_by=self.request.user)
        if post.exists():
            self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('You cannot delete this post.')


class VotePost(generics.CreateAPIView,
               mixins.DestroyModelMixin):

    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])

        return Vote.objects.filter(voted_by=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post.')
        serializer.save(voted_by=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):

        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(stastus=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You cannot delete this Vote.')



