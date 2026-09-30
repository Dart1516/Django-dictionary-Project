# Main URLs: /admin/ goes to the admin site, everything else to the dictionary app
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("dictionary.urls")),
    path('admin/', admin.site.urls),
]
