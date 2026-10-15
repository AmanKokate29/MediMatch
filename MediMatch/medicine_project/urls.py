"""
URL configuration for medicine_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

# Non-i18n URLs (language switcher should be accessible without language prefix)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# i18n URLs (these will have language prefix)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('recommendation.urls')),
    prefix_default_language=False
)
