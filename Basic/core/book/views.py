from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from book.models import Book
from book.serializers import BookSerializers, BookModelSerializers, AuthorModelSerializer

from rest_framework.views import APIView

# Create your views here.
@api_view(['GET'])
def book_list(request):
    book = Book.objects.all();  # complex DS i.e querySet
    serializer = BookSerializers(book, many=True);  # convert querySet to JSON
    return Response(serializer.data);

@api_view(['POST'])
def book_create(request):
    serializer = BookSerializers(data=request.data);  # convert JSON to querySet
    if serializer.is_valid():
        serializer.save();
        return Response(serializer.data);
    
    return Response(serializer.errors);

@api_view(['GET', 'PUT', 'DELETE'])
def book_fetch(request, pk):
    try:
        book = Book.objects.get(pk=pk);
    except:
        return Response({}, status=status.HTTP_404_NOT_FOUND);
        
    if request.method == 'GET':
        serializer = BookSerializers(book);
        return Response(serializer.data, status=status.HTTP_200_OK);
        
    elif request.method == 'PUT':
        serializer = BookSerializers(book, data=request.data);
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_200_OK);
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST);
        
    elif request.method == 'DELETE':
        book.delete();
        return Response({}, status=status.HTTP_204_NO_CONTENT);
    
    else:
        raise Response({ 'error': 'method not sopported' })

@api_view(["GET"])
def current_user_books(request):
    user = request.user
    serializer = AuthorModelSerializer(instance=user, context={ "request": request })
    return Response(serializer.data)

# ============================================= class views =============================================
class BookList(APIView):
    def get(self, request):
        book = Book.objects.all();  # complex DS i.e querySet
        serializer = BookModelSerializers(book, many=True, context={ "request": request });  # convert querySet to JSON
        return Response(serializer.data);
    
class BookCreate(APIView):
    def post(self, request):
        serializer = BookModelSerializers(data=request.data);  # convert JSON to querySet
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data);
        
        return Response(serializer.errors);

class Books(APIView):
    
    def get_book_by_pk(self, pk):
        try:
            book = Book.objects.get(pk=pk);
            return book;
        except:
            return Response({}, status=status.HTTP_204_NO_CONTENT);
    
    def get(self, request, pk):
        if request.method == 'GET':
            book = self.get_book_by_pk(pk);
            serializer = BookModelSerializers(book);
            return Response(serializer.data, status=status.HTTP_200_OK);
    
    def put(self, request, pk):
        book = self.get_book_by_pk(pk);
        serializer = BookModelSerializers(book, data=request.data);
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_200_OK);
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST);
    
    def delete(self, request, pk):
        book = self.get_book_by_pk(pk);
        book.delete();
        return Response({}, status=status.HTTP_204_NO_CONTENT);
