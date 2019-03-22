
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/<username>/', views.profile_view, name='profile_view'),
    path('users/<username>/articles/', views.user_articles, name='user_articles'),
    path('editprofile/', views.profile_edit, name='profile_edit'),
]