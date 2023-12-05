from django.urls import path
from book.views import book_list, book_create, book_fetch, current_user_books, BookList, BookCreate, Books

urlpatterns = [
    path('list/', book_list),
    path('create/', book_create),
    path('<int:pk>/', book_fetch, name="book_detail"),
    path('current-user-books/', current_user_books),
    
    path('list-view/', BookList.as_view()),
    path('create-view/', BookCreate.as_view()),
    path('rest-view/<int:pk>/', Books.as_view()),
]
