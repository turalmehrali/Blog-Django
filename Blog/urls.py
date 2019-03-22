
from . import views
from django.urls import path

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/<str:slug>/', views.article_from_category, name='article_from_category'),
    path('create/', views.article_create, name='article_create'),
    path('articles/<str:slug>/', views.article_detail, name='article_detail'),
    path('articles/<str:slug>/update/', views.article_update, name='article_update'),
    path('articles/<str:slug>/delete/', views.article_delete, name='article_delete'),
    #path('article/<str:slug>/comments/<int:comment_id>', views.article_detail),
]