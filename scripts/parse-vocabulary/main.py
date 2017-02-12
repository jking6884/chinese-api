#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from pprint import pprint
import codecs
import json
import psycopg2
from PpcMain import PpcMain

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

logger = codecs.open('logs/parse-vocabulary', 'w', "utf-8")

encoding = "utf-8"

db = psycopg2.connect("dbname='postgres' user='postgres' host='db' password=''")

cursor = db.cursor()

cursor.execute("""SELECT *
                  FROM app_season""")

seasons = cursor.fetchall()

for season in seasons:
    season_id = str(season[0])

    cursor.execute("""SELECT *
                      FROM app_lesson
                      wHERE season_id = %s
                      ORDER BY id ASC""", (season_id,))

    lessons = cursor.fetchall()

    for lesson in lessons:

        lesson_id = str(lesson[0])

        cursor.execute("""SELECT *
                          FROM app_sentence
                          WHERE lesson_id = %s
                          AND lang_version = 'Traditional Chinese'
                          ORDER BY id ASC""", (lesson_id,))

        sentences = cursor.fetchall()

        for sentence in sentences:
            sentence_id = str(season[0])

            cursor.execute("""SELECT *
                              FROM app_sentence_line
                              WHERE sentence_id = %s
                              ORDER BY id ASC""", (sentence_id,))

            sentence_lines = cursor.fetchall()

            for sentence_line in sentence_lines:
                # pprint(sentence_line)
                #
                # # audio_url = sentence_line[3]
                # text = sentence_line[2]
                # print(text)
                #
                # # logger.write(audio_url + "\n")
                # logger.write(text + "\n")

                ppcMain = PpcMain()
                e = PpcMain.search(ppcMain, u'中文')
                print(e)

        exit()

# for (season) in data:
#     season_title = season["season"]["title"]
#     season_url = season["season"]["href"]
#     level = filename.replace("+", "_")
#
#     cursor.execute('''INSERT INTO app_season (title, level, url) VALUES (%s, %s, %s) RETURNING id''',
#                    (season_title, level.lower(), season_url))
#     db.commit()
#
#     season_id = cursor.fetchone()[0]
#
#     lessons = season['lessons']
#     for (lesson) in lessons:
#         lesson_url = lesson["href"]
#         lesson_num = lesson["lessonNum"]
#         lesson_title = lesson["lessonTitle"]
#
#         cursor.execute(
#             '''INSERT into app_lesson (url, lesson_num, lesson_title, season_id) VALUES (%s, %s, %s, %s) RETURNING id''',
#             (lesson_url, lesson_num, lesson_title, season_id))
#         db.commit()
#
#         lesson_id = cursor.fetchone()[0]
#
#         audioTracks = lesson['audioTracks']
#         for (audioTrack) in audioTracks:
#             url = audioTrack["url"]
#             audio_track_type = audioTrack["name"]
#
#             cursor.execute(
#                 '''INSERT into app_audio_track (url, audio_track_type, lesson_id) VALUES (%s, %s, %s) RETURNING id''',
#                 (url, audio_track_type, lesson_id))
#             db.commit()
#
#         sentences = lesson["sentences"]
#         for (sentence) in sentences:
#             lang_version = sentence["langVersion"]
#
#             cursor.execute('''INSERT into app_sentence (lang_version, lesson_id) VALUES (%s, %s) RETURNING id''',
#                            (lang_version, lesson_id))
#             db.commit()
#
#             sentence_id = cursor.fetchone()[0]
#
#             sentence_lines = sentence["textLines"]
#             for idx, sentence_line in enumerate(sentence_lines):
#                 audio_url = sentence_line["audioLink"]
#                 text = sentence_line["text"]
#                 order = (idx + 1)
#
#                 print '--------'
#                 print(audio_url)
#                 print(text)
#                 print(order)
#                 print(sentence_id)
#                 print '--------'
#
#                 logger.write(audio_url + "\n")
#                 logger.write(text + "\n")
#                 # logger.write(order)
#                 # logger.write(sentence_id)
#
#                 cursor.execute(
#                     '''INSERT into app_sentence_line ("order", text, audio_url, sentence_id) VALUES (%s, %s, %s, %s) RETURNING id''',
#                     (order, text, audio_url, sentence_id))
#                 db.commit()
#
#                 pprint(cursor.fetchone()[0])
