from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('home/', include('homepage.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = [
        path(
            '__debug__/',
            include('debug_toolbar.urls'),
        ),
        *urlpatterns,
    ]
