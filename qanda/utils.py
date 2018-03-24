from nltk.corpus import stopwords

_STOP_WORDS = set(stopwords.words("english"))

def strip_stop_words(text):
    return ' '.join(
        [w for w in text.split() if w.lower() not in _STOP_WORDS])
