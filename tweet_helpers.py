import re
import numpy as np

def clean_text(text):
    links_removed = re.sub("http\S+", "", text)
    hex_ascii_removed = re.sub("\\\\\S+", "", links_removed)
    if hex_ascii_removed[:2] == "b'":
        hex_ascii_removed = hex_ascii_removed[2:]
    clean = re.sub("[^A-Za-z]", " ", hex_ascii_removed).lower()
    return clean

def get_word_vector(par, word_embed, ifd_weights):
    par_list = par.split()
    par_list = [elem for elem in par_list if len(elem)>0]

    sum_weights = 0.0
    sum_vector = np.zeros(300)

    for word in par_list:
        try:
            word_weights = ifd_weights.idf_[ifd_weights.vocabulary_[word]]
            sum_vector += word_embed[word] * word_weights
            sum_weights += word_weights
        except:
            pass
    return sum_vector/sum_weights