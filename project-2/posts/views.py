from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from posts.serializers import PostSerializer
from accounts.serializers import UserSerializer

# Create your views here.
@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def list_posts(request: Request):
    try:
        posts = Post.objects.all()
        serializer = PostSerializer(instance=posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(data={ "error": "Something Went Wrong" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(http_method_names=["GET"])
def post_detail(request: Request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostSerializer(post)
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)

@api_view(http_method_names=["POST"])
@permission_classes(permission_classes=[IsAuthenticated])
def create_post(request: Request):
    try:
        data = request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            # assign the user who created the post
            serializer.save(author=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={ "errors": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(data={ "error": "Something went wrong" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def get_post_by_id(request: Request, pk: int):
    pass

@api_view(http_method_names=["PUT"])
@permission_classes(permission_classes=[IsAuthenticated])
def update_post(request: Request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    data = request.data
    serializer = PostSerializer(instance=post, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=["DELETE"])
@permission_classes(permission_classes=[IsAuthenticated])
def delete_post(request: Request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return Response(data={}, status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def get_post_for_current_user(request: Request):
    user = request.user
    serializer = UserSerializer(instance=user, context={ "request": request })  # context requried, if you are using HyperlinkedRelatedField
    return Response(data=serializer.data, status=status.HTTP_200_OK)

"""
if writing a views is like building a chair, then 
1. APIView is like building each component of chair yourself
2. Generic views is assembling already made components to form a chair
3. ViewSet is a framework on which you build to make sure your chairs are always consistent.
"""

"""
Concrete View Classes
If you're using generic views this is normally to level you'll be
working at unless you need heavily customized behavior.
Concrete Views are combination of Mixins and GenericAPIView. They 
abstract away most of that tasks that we need to do manually using 
APIView.

    RetrieveAPIView - used for read-only endpoints to represnt a single models instance. Provides get method handler.
    CreateAPIView - used for create-only endpoints. Provides post method handler.
    ListAPIView - used for read-only endpoints to represent a collection of model instances. Provides get method handler.
    ListCreateAPIView - used for read-write endpoints to represent a collection of model instances. Provides get and post method handler.
    UpdateAPIView - used for update-write endpoints to represent a single model instance. Provides put and patch method handler.
    DestroyAPIView - used for delete-write endpoints to represent a single model instance. Provides delete method handler.
    RetrieveUpdateAPIView - used for read or update endpoints to represent a single model instance. Provides get, put, patch method handler.
    RetrieveDestroyAPIView - used for read or delete endpoints to represent a single model instance. Provides get and delete method handler.
    RetrieveUpdateDestroyAPIView - used for read-write-delete endpoints to represent a single model instance. Provides get, put, patch, delete method handler.
"""

"""
GenericAPIView
is a base class in all Generic View classes. Extends REST  frameworks APIView 
class, adding commonly requierd behavior for stndard list and detail views.

Mixins
Mixin used to provide the basic view behavior. Note that mixin class provide
action methods rather than defining the handler methods such as .get() and
.post() directly. This allows for more flexible composition of behavior.
Mixins are not much use on their own, we need to use thm with GenericAPIView.

    ListModelMixin - provides .list(request, *args, **kwargs) method that implements listing a queryset.
    CreateModelMixin - provides .create(request, *args, **kwargs) method that implements creating and saving new model instance.
    RetrieveModelMixin - provides .retrieve(request, *args, **kwargs) method that implements returning an existing model instance.
    UpdateModelMixin - provides .update(request, *args, **kwargs) method that implements updating and saving existing model instance.
    DestroyModelMixin - provides .destroy(request, *args, **kwargs) method that implements deletion of an existing model instance.
"""