from app.models import Season, Lesson, AudioTrack, Sentence, SentenceLine
from app.serializers import SeasonSerializer, LessonSerializer, AudioTrackSerializer, SentenceSerializer, SentenceLineSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class AudioTrackViewSet(viewsets.ModelViewSet):
    queryset = AudioTrack.objects.all()
    serializer_class = AudioTrackSerializer

class SentenceViewSet(viewsets.ModelViewSet):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer

class SentenceLineViewSet(viewsets.ModelViewSet):
    queryset = SentenceLine.objects.all()
    serializer_class = SentenceLineSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer