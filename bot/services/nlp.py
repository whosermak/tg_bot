from gigachat import GigaChat
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY=os.getenv("GIGACHAT_API_KEY")


sys_promt = """
Ты генерируешь SQL для PostgreSQL.

На входе — вопрос на русском языке в естественной форме.
На выходе — ОДИН корректный SQL-запрос, который возвращает РОВНО ОДНО ЧИСЛО.

ОБЩИЕ ПРАВИЛА:
Только SQL.
Без комментариев.
Без пояснений.
Без markdown.

Ровно один SELECT.
ДОБАВЛЯЙ SELECT в начало sql запроса ЕСЛИ ОН НУЖЕН

Ты ошибаешься в слове timestamptz (НЕ СМЕЙ ПИСАТЬ timestamtz НАДО ПИСАТЬ: timestamptz)

Ровно одна строка результата.
Ровно один столбец результата.
Используй только таблицы и поля ниже.
Если результат может быть NULL — обязательно используй COALESCE(..., 0).
Если используются агрегатные функции (COUNT, SUM, MAX, MIN) — не используй ORDER BY или LIMIT.
Если используется ORDER BY — не используй агрегатные функции.
Никогда не добавляй GROUP BY, если вопрос не требует группировки.


Интерпретация естественного языка
Правила преобразования:
"Сколько всего видео" → COUNT(*) из videos
"Сколько видео" → COUNT(*) из videos
"Сколько видео у креатора с id X" → COUNT(*) из videos WHERE creator_id = 'X'
"Больше N просмотров" → WHERE views_count > N
"Рост за период" → SUM(delta_views_count) из video_snapshots
"Сколько разных видео получали новые просмотры" →
COUNT(DISTINCT video_id)
WHERE delta_views_count > 0

Если говорится о росте за дату или период — использовать таблицу video_snapshots.
Если говорится о текущем количестве просмотров — использовать videos.views_count.
Работа с датами
Все даты в UTC.

Дата без времени означает:
= YYYY-MM-DD 00:00:00
AND
<= YYYY-MM-DD 23:59:59

Период "с X по Y включительно":
= X 00:00:00
AND
<= Y 23:59:59

Если указана одна дата — фильтровать за эту дату целиком.
Для video_snapshots использовать поле created_at.
Для videos при фильтрации по дате публикации использовать video_created_at.


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
video_id UUID,
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

Самопроверка перед выводом

Перед тем как вывести SQL, проверь:
Нет ли одновременного использования агрегатных функций и ORDER BY.
Запрос возвращает ровно одну строку и один столбец.

Используется корректный синтаксис PostgreSQL.
Все поля существуют в схеме.
Даты приведены к границам суток UTC.
Если есть ошибка — исправь и выведи корректный SQL.

Формат вывода:
Выведи только SQL-запрос.

ЗАПРОС ПОЛЬЗОВАТЕЛЯ:
"""


async def parse_text(q):
    async with GigaChat(credentials=API_KEY, verify_ssl_certs=False) as client:
        r = await client.achat(sys_promt + q)

        sql = r.choices[0].message.content.strip()
        return sql.replace("```sql", "").replace("```", "").strip()