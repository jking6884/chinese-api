from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('app.urls')),
]

urlpatterns += [
    url(r'^api-path/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
