from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path

from apps.views import RegisterView, ActivateUserView, index, CustomLoginView
from root.settings import STATIC_URL, STATIC_ROOT

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('activate/<str:uid64>/<str:token>', ActivateUserView.as_view(), name='activate_user'),
    path('', index, name='index'),
    path('admin/', admin.site.urls),
] + static(STATIC_URL, document_root=STATIC_ROOT)
