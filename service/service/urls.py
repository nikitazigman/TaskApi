"""work_balancer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import settings

schema_view = get_schema_view(
    openapi.Info(
        title="WorkBalancer API",
        default_version="v1.1",
        description="Backend for the workbalancer service",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="zigman.nikita@gmail.com"),
        license=openapi.License(name="GPL-2.0 License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # type: ignore
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("task.urls")),
    path("api/v1/", include("day.urls")),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"  # type: ignore
    ),
]

if settings.DEBUG:
    urlpatterns.extend(
        [
            path(
                "api-auth/",
                include("rest_framework.urls"),
            ),
            path(
                "__debug__/",
                include("debug_toolbar.urls"),
            ),
        ]
    )
