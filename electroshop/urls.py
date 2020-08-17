from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Allauth URL's
    path('accounts/', include('allauth.urls')),

    # App URL's
    path('', include('shop.urls', namespace='shop')),

]

# ERROR 404- NOT FOUND PAGE
handler404 = 'shop.views.Erro404View'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)