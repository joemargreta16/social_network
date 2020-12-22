from django.urls import path
from .views import post_comment_views, like_unlike_post, PostUpdateView, PostDeleteView

app_name = 'posts'

urlpatterns = [
    path('', post_comment_views, name='post-comment-views'),
    path('liked-unliked/', like_unlike_post, name='like-unlike-post'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
