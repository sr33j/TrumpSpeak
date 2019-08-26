import csv
import numpy as np
from tweet_helpers import clean_text, get_word_vector
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from scipy.spatial.distance import cosine


def find_closest_tweet(phrase, vectorizer, google_model):
    trump_tweets = []
    with open('trump_tweets.csv') as csvfile:
        trump_csv = csv.reader(csvfile, delimiter=',')
        for row in trump_csv:
            trump_tweets.append(row[2])

    clean_phrase = clean_text(phrase)
    phrase_vector = get_word_vector(clean_phrase,google_model,vectorizer)

    word_vectors = np.load("wordvectors.npy", allow_pickle=True)

    min_cos = 10
    min_cos_idx = 0
    for i in range(len(word_vectors)):
        if cosine(word_vectors[i],phrase_vector) < min_cos:
            min_cos = cosine(word_vectors[i],phrase_vector)
            min_cos_idx = i

    return trump_tweets[int(min_cos_idx)]
    # print(min_cos)
    # print(trump_tweets[min_cos_idx])