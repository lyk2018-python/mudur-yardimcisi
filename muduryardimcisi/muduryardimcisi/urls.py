from django.contrib import admin
from django.urls import path
from muduryardimci import views as muduryardimci_views
from django.contrib.auth import views as auth_views

urlpatterns = [
                    path('login/', auth_views.login, name='login'),
                    path('logout/', auth_views.logout, name='logout'),
                    path('admin/', admin.site.urls),
                    path('superauth/', muduryardimci_views.superuser_token, name="supertoken"),
                    path('auth/',  muduryardimci_views.generate_token, name="auth"),
                    path('accounts/', muduryardimci_views.dashboard, name='dashboard'),
                    path('accounts/', muduryardimci_views.dashboard, name='dashboard'),
                    path('checkstundent/', muduryardimci_views.stundent_check, name="Stundent_check"),
                    path('authlogin/', muduryardimci_views.AuthToken, name="Authlogin"),
              ]
