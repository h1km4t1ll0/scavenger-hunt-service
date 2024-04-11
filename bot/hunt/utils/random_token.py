import random

from english_words import english_words_alpha_set


def random_token(length: int):
    english_words_alpha = list(english_words_alpha_set)
    return "_".join([random.choice(english_words_alpha).upper() for i in range(length)])
