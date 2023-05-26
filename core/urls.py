from django.urls import path
from django.contrib.auth.views import LogoutView
from core.views import (
    PostListView,
    NewsList,
    NewsDetail,
    NewsCreate,
    NewsUpdate,
    NewsDelete,
    LoginUser,
    RegisterView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

app_name = 'core'

urlpatterns = [
    path('home_page/', NewsList.as_view(), name='home_page'),
    path('news_detail/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news_create/', NewsCreate.as_view(), name='news_create'),
    path('news_update/<int:pk>', NewsUpdate.as_view(), name='news_update'),
    path('news_delete/<int:pk>', NewsDelete.as_view(), name='news_delete'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='core:home_page'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]
