from django.urls import path
from social.views import CreateAndPublishPostView, DeletePostView, EditPostView, FetchAllPostsView

urlpatterns = [
    path('create/<str:platform>/', CreateAndPublishPostView.as_view(), name='create_post'),
    path('delete/<str:platform>/<int:post_id>/', DeletePostView.as_view(), name='delete_post'),
    path('edit/<str:platform>/<int:post_id>/', EditPostView.as_view(), name='edit_post'),
    path('fetch/<str:platform>/', FetchAllPostsView.as_view(), name='fetch_posts'),
]
