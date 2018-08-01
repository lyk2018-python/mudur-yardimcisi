from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from accounts import views as account_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('django.contrib.auth.urls'), name="Account"),
    ]
