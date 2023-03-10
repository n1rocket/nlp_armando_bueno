import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


def preprocess_text(text, my_stop_words):
    # Convertir todo el texto a minúsculas
    text = text.lower()

    # Eliminar signos de puntuación
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)

    # Tokenización de palabras
    words = nltk.word_tokenize(text)

    # Lematización
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # Eliminación de stopwords
    stpwrd = stopwords.words('english')
    # Mis propias stopwords
    stpwrd.extend(my_stop_words)
    stop_words = set(stpwrd)
    words = [word for word in words if word not in stop_words]

    # Unir las palabras procesadas en un solo texto
    processed_text = ' '.join(words)

    return processed_text


def process_reviews(reviews, my_stop_words):
    processed_sentences = []
    for sent in reviews:
        if not sent != sent:  # check if sent is not nan
            sent = preprocess_text(sent, my_stop_words)
            processed_sentences.append(sent)
        else:
            processed_sentences.append('None')
    return processed_sentences


def plot_word_cloud(text):
    wordcloud = WordCloud(max_font_size=50,
                          max_words=100,
                          background_color="white").generate(' '.join(text))
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


# Read CSV file into DataFrame df
df = pd.read_csv('./project/balanced_reviews.csv', index_col=0)

# Show dataframe
print(df)

my_stop_words = [
    "game", "play", "level", "character", "one", "mouse", "got", "people",
    "gameplay", "run", "first", "will", "review", "mouse", "control", "system"
]
reviews_processed = process_reviews(df['reviewText'], my_stop_words)

all_words = ''.join(reviews_processed)
splitted_reviews = all_words.lower().split()

# plot_word_cloud(splitted_reviews)
print("game" in splitted_reviews)
