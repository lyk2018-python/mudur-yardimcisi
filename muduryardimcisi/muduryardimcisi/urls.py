from django.contrib import admin
from django.urls import path
from muduryardimci import views as muduryardimci_views
from django.contrib.auth import views as auth_views
from accounts import views as account_views

urlpatterns = [
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('admin/', admin.site.urls),
    path('superauth/', muduryardimci_views.superuser_token, name="supertoken"),
    path('auth/',  muduryardimci_views.generate_token, name="auth"),
    path('accounts/', muduryardimci_views.dashboard, name='dashboard'),
    path('', account_views.home),
    path('profile/', account_views.profile),
    path('accounts/', muduryardimci_views.dashboard, name='dashboard'),
    path('checkstundent/', muduryardimci_views.stundent_check, name="Stundent_check"),
    path('authlogin/', muduryardimci_views.AuthToken, name="Authlogin"),
]
