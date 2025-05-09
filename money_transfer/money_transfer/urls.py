from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('homepage.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns = [
        *urlpatterns,
        path(
            '__debug__/',
            include('debug_toolbar.urls'),
        ),
    ]
