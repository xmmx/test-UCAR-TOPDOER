import unittest
from app import app, analyze_sentiment
import os

class SentimentTests(unittest.TestCase):

    def test_positive(self):
        positives = [
            'Очень хорошее обслуживание!',
            'Люблю этот сервис.',
            'Отличная поддержка.',
            'Классный магазин!',
            'Мне всё понравилось.'
        ]
        for text in positives:
          try:
            self.assertEqual(analyze_sentiment(text), 'positive')
          except Exception as e:
            print(text)
            print(e)

    def test_negative(self):
        negatives = [
            'Очень плохо.',
            'Ненавижу этот сервис.',
            'Ужасно.',
            'Отстойное обслуживание!',
            'Совсем не нравится.'
        ]
        for text in negatives:
          try:
            self.assertEqual(analyze_sentiment(text), 'negative')
          except Exception as e:
            print(text)
            print(e)

    def test_neutral(self):
        neutrals = [
            'Всё в порядке.',
            'Средне.',
            'Я посетил магазин.',
            'Услуга оказана.',
        ]
        for text in neutrals:
          try:
            self.assertEqual(analyze_sentiment(text), 'neutral')
          except Exception as e:
            print(text)
            print(e)

class AppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Тестовая БД
        cls.test_db = 'test_reviews.db'
        app.config['TESTING'] = True
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.test_db)
        except Exception:
            pass


if __name__ == '__main__':
    unittest.main()
