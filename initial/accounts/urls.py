from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name ='signup'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('<username>/', views.profile, name='profile'),  
    path('<username>/profile_edit/', views.profile_edit, name='profile_edit'),  
    path('<username>/follow/', views.follow, name='follow'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)