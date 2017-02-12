from rest_framework import serializers
from app.models import Season, Lesson, AudioTrack, Sentence, SentenceLine
from django.contrib.auth.models import User

class SeasonSerializer(serializers.ModelSerializer):
    lessons = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ('id','title','level','url','lessons')

class LessonSerializer(serializers.ModelSerializer):
    audio_tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ('id','url','lesson_num','lesson_title','audio_tracks')

class AudioTrackSerializer(serializers.ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AudioTrack
        fields = ('id','url','audio_track_type','lesson')

class SentenceSerializer(serializers.ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Sentence
        fields = ('id','lang_version','lesson')

class SentenceLineSerializer(serializers.ModelSerializer):
    sentence = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SentenceLine
        fields = ('id','order','text','audio_url','sentence')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username')