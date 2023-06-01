from django.conf import settings
from django.conf.urls.static import static
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
    PostDeleteView,
    delete_user,
    delete_user_confirm,
    profile,
    post_like,
    delete_comment
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
    path('delete_user/', delete_user, name='delete_user'),
    path('delete_user/confirm/', delete_user_confirm, name='delete_confirm'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('profile/', profile, name='profile'),
    path('post_like/', post_like, name='post_like'),
    path('comment/<int:id>', delete_comment, name='delete_comment'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
