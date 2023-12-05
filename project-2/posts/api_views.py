from django.shortcuts import get_object_or_404

from rest_framework.decorators import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from posts.serializers import PostSerializer

class PostListCreateView(APIView):
    serializer_class = PostSerializer
    permission_classes=[IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = self.serializer_class(instance=posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # assign the user who created the post
            serializer.save(author=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostRetrieveUpdateDeleteView(APIView):
    serializer_class = PostSerializer
    permission_classes=[IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.serializer_class(instance=post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        data = request.data
        serializer = PostSerializer(instance=post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request: Request, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)
