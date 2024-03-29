from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('category/<int:pk>', CategoryList.as_view(), name='category'),

    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),

    path('news/search/', PostSearch.as_view(), name='post_search'),
    #  delete
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    #  update
    path('news/<int:pk>/update', PostUpdate.as_view(), name='news_update'),
    path('article/<int:pk>/update', ArticleUpdate.as_view(), name='news_update'),
    #  create
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('article/create', ArticleCreate.as_view(), name='article_create'),

    path('index/', IndexView.as_view(), name='index'),
    #  path('login/', log_in, name='login'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    #  path('logout/', log_out, name='logout'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    #  path('signin/', sign_in, name='signin'),
    path('sign/', BaseRegisterView.as_view(template_name='sign.html'), name='sign'),

    path('upgrade/', upgrade_me, name='upgrade'),

    path('submit/<int:pk>', submit, name='submit'),

    path('translate', Index.as_view(), name='translate'),

    path('testframe/', PostListView.as_view(), name='testframe')

    ]
