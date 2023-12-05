from django.urls import path
from posts.views import list_posts, post_detail, create_post, update_post, delete_post, get_post_for_current_user
from posts.api_views import PostListCreateView, PostRetrieveUpdateDeleteView
from posts.generic_views import PostListCreateGenericView, PostRetrieveUpdateDeleteGenericView, ListPostsForAuthorGenericView, ListPostsForUserGenericView

urlpatterns = [
    path("", list_posts, name="list_posts"),
    path("<int:pk>/", post_detail, name="post_detail"),
    path("create-post/", create_post, name="create_post"),
    path("update_post/<int:pk>/", update_post, name="update_post"),
    path("delete_post/<int:pk>/", delete_post, name="delete_post"),
    path("current_user/", get_post_for_current_user, name="current_user"),
    
    path("api_view/", PostListCreateView.as_view(), name="api_view"),
    path("api_view/<int:pk>/", PostRetrieveUpdateDeleteView.as_view(), name="api_view_rud"),
    
    path("api_generic_view/", PostListCreateGenericView.as_view(), name="api_generic_view"),
    path("api_generic_view/<int:pk>/", PostRetrieveUpdateDeleteGenericView.as_view(), name="api_generic_view_rud"),
    path("api_generic_view/current_user_posts/", ListPostsForAuthorGenericView.as_view(), name="current_user_posts"),
    path("api_generic_view/posts_for/<str:username>/", ListPostsForUserGenericView.as_view(), name="posts_for"),
]
