from django.urls import path
from . import views
from initial import settings

app_name = 'articles'

urlpatterns = [
 path('', views.index, name='index'),   
 path('home/', views.home, name='home' ),
 path('movie_list/', views.movie_list, name='movie_list'),
 path('last_movie_list/', views.last_movie_list, name='last_movie_list'),
 path('review_list/', views.review_list, name='review_list'),
 path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
 path('<int:movie_pk>/community', views.community, name='community'),
 path('<int:movie_pk>/review_create', views.review_create, name='review_create'),
 path('<int:movie_pk>/<int:review_pk>/', views.review_detail, name='review_detail'),
 path('<int:movie_pk>/<int:review_pk>/review_delete', views.review_delete, name='review_delete'),
 path('<int:movie_pk>/<int:review_pk>/review_update', views.review_update, name='review_update'),
 path('<int:movie_pk>/<int:review_pk>/comment_create', views.comment_create, name='comment_create'),
 path('<int:movie_pk>/<int:review_pk>/<int:comment_pk>/comment_delete/', views.comment_delete, name='comment_delete'),
 path('<int:movie_pk>/<int:review_pk>/<int:comment_pk>/comment_update/', views.comment_update, name='comment_update'),
 path('<int:movie_pk>/youtube', views.youtube, name='youtube'),
]