from django.conf.urls import url, include
from app import views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Pastebin API')

router = DefaultRouter(trailing_slash=False)
router.register(r'seasons', views.SeasonViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'audio_tracks', views.AudioTrackViewSet)
router.register(r'sentences', views.SentenceViewSet)
router.register(r'sentence_lines', views.SentenceLineViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url('^schema/$', schema_view),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^logout/', views.Logout.as_view())
]