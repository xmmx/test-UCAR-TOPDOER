from flask import Flask, request, jsonify
from datetime import datetime
from sqlite3 import connect

app = Flask(__name__)
DB_PATH = 'reviews.db'

###########################################################################
#
# Вспомогательные функции
#
###########################################################################

def init_db():
    """init_db
    Инициализация базы данных
    """
    with connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        ''')


def analyze_sentiment(text: str) -> str:
    """analyze_sentiment
    Функция оценки настроения отзыва по его содержимому.

    Args:
        text (str): текст отзыва

    Returns:
        str: оценка натсроения
    """
    text_lower = text.lower()
    # Определим положительные ключи
    positive = ['хорош', 'люблю', 'отличн', 'супер', 'прекрасн', 'нравит', 'класс', 'нравил']
    # Определим отрицательные ключи
    negative = ['плохо', 'ненавиж', 'ужасн', 'отстой', 'раздраж', 'разочарован']

    for p in positive:
        # Для начала проверим отрицания положительных
        if f'не {p}' in text_lower:
          return 'negative'
        if p in text_lower:
            return 'positive'

    for n in negative:
        if n in text_lower:
            return 'negative'
    # Иначе нейтральный
    return 'neutral'

###########################################################################
#
# Определение роутов
#
###########################################################################

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()

    # Проверка ошибки
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400

    text = data['text']
    sentiment = analyze_sentiment(text)
    created_at = datetime.now()

    with connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
            (text, sentiment, created_at)
        )
        review_id = cursor.lastrowid

    # Вывод результата
    return jsonify({
        'id': review_id,
        'text': text,
        'sentiment': sentiment,
        'created_at': created_at
    })


@app.route('/reviews', methods=['GET'])
def get_reviews():
    sentiment = request.args.get('sentiment')

    # Проверка ошибки
    if sentiment not in ('positive', 'neutral', 'negative'):
        return jsonify({'error': 'Specify sentiment=positive|neutral|negative'}), 400

    with connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment=? ORDER BY created_at DESC',
            (sentiment,)
        )
        rows = cursor.fetchall()

    # Вывод результата
    result = [
        {'id': row[0], 'text': row[1], 'sentiment': row[2], 'created_at': row[3]}
        for row in rows
    ]
    return jsonify(result)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
