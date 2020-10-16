from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),

# ****************************** Blog Urls **********************************************

    path('', include('blog.urls')),

# ****************************** Expenses Urls ******************************************

    path('', include('expenses.urls')),

    path('', include('projects.urls')),

# ********************************* Users Urls **********************************************

    path('', include('users.urls')),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)