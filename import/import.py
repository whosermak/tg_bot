import json
import psycopg
from datetime import datetime

def time(s): 
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
            time(video["video_created_at"]),
            int(video["views_count"]),
            int(video["likes_count"]),
            int(video["reports_count"]),
            int(video["comments_count"]),
            video["creator_id"],
            time(video["created_at"]),
            time(video["updated_at"])
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
                time(snap["created_at"]),
                time(snap["updated_at"])
            )
        )

conn.commit()
cur.close()
conn.close()
