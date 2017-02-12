from __future__ import unicode_literals

from django.db import models

class Season(models.Model):
    title = models.CharField(max_length=64, blank=False)
    level = models.CharField(max_length=64, blank=False)
    url = models.CharField(max_length=255, blank=False)

class Lesson(models.Model):
    url = models.CharField(max_length=255, blank=False)
    lesson_num = models.CharField(max_length=10, blank=False)
    lesson_title = models.CharField(max_length=255, blank=False)



    season = models.ForeignKey('app.Season', null=True, related_name='lessons', on_delete=models.CASCADE)

class AudioTrack(models.Model):
    url = models.CharField(max_length=255, blank=False)
    audio_track_type = models.CharField(max_length=64, blank=False)

    class Meta:
        db_table = 'app_audio_track'

    lesson = models.ForeignKey('app.Lesson', null=True, related_name='audio_tracks', on_delete=models.CASCADE)

class Sentence(models.Model):
    lang_version = models.CharField(max_length=64, blank=False)

    lesson = models.ForeignKey('app.Lesson', null=True, related_name='sentences', on_delete=models.CASCADE)

class SentenceLine(models.Model):
    order = models.IntegerField()
    text = models.TextField()
    audio_url = models.CharField(max_length=255, default=None, blank=True, null=True)

    class Meta:
        db_table = 'app_sentence_line'

    sentence = models.ForeignKey('app.Sentence', null=True, related_name='sentence_lines', on_delete=models.CASCADE)