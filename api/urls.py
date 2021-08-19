from django.urls import path

from . import views

urlpatterns = [
    path('api/post', views.PostList.as_view()),
    path('api/post/<int:pk>', views.PostRetrieveUpdateDestroy.as_view()),
    path('api/post/<int:pk>/vote', views.VotePost.as_view()),
]