# -*- encoding: utf-8 -*-
"""

"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE
    path('accounts/', include('allauth.urls')),

    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls"))
]


admin.site.site_header = "DE Dashboard - Admin Panel"
admin.site.site_title = "DE Dashboard - Admin Panel"
admin.site.index_title = ""