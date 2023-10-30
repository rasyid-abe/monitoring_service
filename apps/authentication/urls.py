from django.urls import path
from .views import login_view, inactive_page
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    # path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("accounts/inactive/", inactive_page),
    path("accounts/social/signup/", inactive_page)
]
