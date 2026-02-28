import json
import psycopg
from datetime import datetime
import time

def wait_db():
    while True:
        try:
            conn = psycopg.connect(
                host="db",
                dbname="bot_db",
                user="appuser",
                password="pass123"
            )
            conn.close()
            break
        except Exception:
            time.sleep(2)
wait_db()



def toTime(s): 
    return datetime.fromisoformat(s)

conn = psycopg.connect(
    host="db",
    dbname="bot_db",
    user="appuser",
    password="pass123"
)
cur = conn.cursor()

with open("videos.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for video in data['videos']:
    cur.execute(
        "INSERT INTO videos (id, video_created_at, views_count, likes_count, reports_count, comments_count, creator_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            video["id"], 
            toTime(video["video_created_at"]),
            int(video["views_count"]),
            int(video["likes_count"]),
            int(video["reports_count"]),
            int(video["comments_count"]),
            video["creator_id"],
            toTime(video["created_at"]),
            toTime(video["updated_at"])
        )
    )

    for snap in video["snapshots"]:
        cur.execute(
            "INSERT INTO video_snapshots (id, video_id, views_count, likes_count, reports_count, comments_count, delta_views_count, delta_likes_count, delta_reports_count, delta_comments_count, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                snap["id"], 
                snap["video_id"],
                int(snap["views_count"]),
                int(snap["likes_count"]),
                int(snap["reports_count"]),
                int(snap["comments_count"]),
                int(snap["delta_views_count"]),
                int(snap["delta_likes_count"]),
                int(snap["delta_reports_count"]),
                int(snap["delta_comments_count"]),
                toTime(snap["created_at"]),
                toTime(snap["updated_at"])
            )
        )

conn.commit()
cur.close()
conn.close()
