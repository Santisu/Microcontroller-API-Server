from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework.documentation import include_docs_urls
from .views import CommandViewSet, ntp_time

router = SimpleRouter()
router.register('cmd', CommandViewSet)

urlpatterns = [
     path('', include('dj_rest_auth.urls')),
     path('time/', ntp_time, name='ntp_time'),
     path('docs/', include_docs_urls(title="Microcontroller Server API")),
]

urlpatterns += router.urls