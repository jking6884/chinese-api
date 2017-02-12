#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from pprint import pprint
import codecs
import json
import psycopg2

logger = codecs.open('logs/build_db', 'w', "utf-8")

encoding = "utf-8"

db = psycopg2.connect("dbname='postgres' user='postgres' host='db' password=''")

cursor = db.cursor()

filenames = ['Absolute+Beginner','Beginner','Intermediate','Advanced']

for (filename) in filenames:
    with codecs.open("chinese-class-101/" + filename + ".js", 'r', encoding="utf-8") as file_content:
        data = json.load(file_content)

        for (season) in data:
            season_title = season["season"]["title"]
            season_url = season["season"]["href"]
            level = filename.replace("+", "_")

            cursor.execute('''INSERT INTO app_season (title, level, url) VALUES (%s, %s, %s) RETURNING id''', (season_title, level.lower(), season_url))
            db.commit()

            season_id = cursor.fetchone()[0]

            lessons = season['lessons']
            for (lesson) in lessons:
                lesson_url = lesson["href"]
                lesson_num = lesson["lessonNum"]
                lesson_title = lesson["lessonTitle"]

                cursor.execute('''INSERT into app_lesson (url, lesson_num, lesson_title, season_id) VALUES (%s, %s, %s, %s) RETURNING id''', (lesson_url, lesson_num, lesson_title, season_id))
                db.commit()

                lesson_id = cursor.fetchone()[0]

                audioTracks = lesson['audioTracks']
                for (audioTrack) in audioTracks:
                    url = audioTrack["url"]
                    audio_track_type = audioTrack["name"]

                    cursor.execute('''INSERT into app_audio_track (url, audio_track_type, lesson_id) VALUES (%s, %s, %s) RETURNING id''', (url, audio_track_type, lesson_id))
                    db.commit()

                sentences = lesson["sentences"]
                for (sentence) in sentences:
                    lang_version = sentence["langVersion"]

                    cursor.execute('''INSERT into app_sentence (lang_version, lesson_id) VALUES (%s, %s) RETURNING id''', (lang_version, lesson_id))
                    db.commit()

                    sentence_id = cursor.fetchone()[0]

                    sentence_lines = sentence["textLines"]
                    for idx, sentence_line in enumerate(sentence_lines):
                        audio_url = sentence_line["audioLink"]
                        text = sentence_line["text"]
                        order = (idx + 1)

                        print '--------'
                        print(audio_url)
                        print(text)
                        print(order)
                        print(sentence_id)
                        print '--------'

                        logger.write(audio_url + "\n")
                        logger.write(text + "\n")
                        # logger.write(order)
                        # logger.write(sentence_id)

                        cursor.execute('''INSERT into app_sentence_line ("order", text, audio_url, sentence_id) VALUES (%s, %s, %s, %s) RETURNING id''', (order, text, audio_url, sentence_id))
                        db.commit()

                        pprint(cursor.fetchone()[0])