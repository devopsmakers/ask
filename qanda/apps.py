from django.apps import AppConfig
import nltk

class QandaConfig(AppConfig):
    name = 'qanda'
    def ready(self):
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
