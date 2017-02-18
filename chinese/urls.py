from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('app.urls')),
]

urlpatterns += [
    url(r'^api-path/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api-auth-token/', obtain_auth_token),
]
