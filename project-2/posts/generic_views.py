from django.shortcuts import get_object_or_404

from rest_framework.decorators import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from posts.serializers import PostSerializer
from posts.pagination import CustomPagination

class PostListCreateGenericView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes=[IsAuthenticated]

    # assign the user who created the post
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class PostRetrieveUpdateDeleteGenericView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes=[IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ListPostsForAuthorGenericView(
    generics.GenericAPIView,
    mixins.ListModelMixin
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ListPostsForUserGenericView(
    generics.GenericAPIView,
    mixins.ListModelMixin
):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Post.objects.all()
    
    def get_queryset(self):
        username = self.kwargs.get("username")  # or you can also write -> self.request.query_params.get("username")
        queryset = Post.objects.all()
        if username is not None:
            return Post.objects.filter(author__username=username)
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)