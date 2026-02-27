from groq import AsyncGroq
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

sys_promt = """
Ты генерируешь SQL для PostgreSQL.
На входе — вопрос на русском.
На выходе — ОДИН SQL-запрос, возвращающий ОДНО число.

Правила:

Только SQL.

Без комментариев.

Без пояснений.

Без markdown.

Используй только таблицы и поля ниже.

Если результат может быть NULL — используй COALESCE(..., 0).

Таблицы

videos(
id UUID PK,
video_created_at TIMESTAMPTZ,
views_count INT,
likes_count INT,
reports_count INT,
comments_count INT,
creator_id TEXT,
created_at TIMESTAMPTZ,
updated_at TIMESTAMPTZ
)

video_snapshots(
id TEXT PK,
video_id UUID → videos.id,
views_count INT,
likes_count INT,
reports_count INT,
comments_count INT,
delta_views_count INT,
delta_likes_count INT,
delta_reports_count INT,
delta_comments_count INT,
created_at TIMESTAMPTZ,
updated_at TIMESTAMPTZ
)

Логика:

Общее количество видео → videos

Текущие просмотры → videos.views_count

Рост за период → SUM(delta_views_count) из video_snapshots

Количество видео с ростом → COUNT(DISTINCT video_id) где delta_views_count > 0

Даты без времени = границы суток UTC

Период "с X по Y включительно" = >= X 00:00:00 и <= Y 23:59:59

Всегда возвращай ровно одну строку и один столбец.
"""

async def parse_text(q):
    r = await client.chat.completions.create(
        messages=[
            { "role": "system", "content": sys_promt },
            { "role": "user", "content": q }
        ],

        model="llama-3.3-70b-versatile"
    )

    sql = r.choices[0].message.content.strip()
    return sql.replace("```sql", "").replace("```", "").strip()