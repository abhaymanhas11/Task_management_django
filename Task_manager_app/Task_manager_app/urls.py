"""
URL configuration for Task_manager_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ck_views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.user.urls")),
    path("todo/", include("apps.todo.urls")),
    path("api-auth/", include("rest_framework.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

ckEditor_urls = [
    re_path(r"^upload/", (ck_views.upload), name="ckeditor_upload"),
    re_path(
        r"^browse/",
        never_cache(ck_views.browse),
        name="ckeditor_browse",
    ),
]

urlpatterns += ckEditor_urls


urlpatterns +=  staticfiles_urlpatterns()
