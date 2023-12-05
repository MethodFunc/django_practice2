from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),  #/accounts/login/ => settings.LOGIN_URL
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path("password_change/", views.password_change, name="password_change"),

    # path("password_chage", auth_views.PasswordChangeView.as_view(success_url=reverse_lazy("/")), name="password_change"),
    # path("password_change/done", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
]

