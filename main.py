import random
import tomllib

import pyperclip
import requests
from unidecode import unidecode

WORD_COUNT_FINAL = 50_000
WORD_COUNT_PER_LANG = 20_000

# TODO pre-download data?

def get_data(lang_name):
    url_base = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018"
    url = f"{url_base}/{lang_name}/{lang_name}_50k.txt"
    data = requests.get(url).text
    return data

def print_dict_start(d, n):
    d = dict(list(d.items())[:n])
    for key, value in d.items():
        print(f"{key: <9}{value:.3f}")

def sorted_dictionary(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}

def get_word_data(lines):
    word_data = {}
    freq_total = 0

    for line in lines:
        word, freq = line.split()
        word = unidecode(word)
        word = "".join(filter(str.isalpha, word))
        freq = int(freq)

        word_data[word] = word_data.get(word, 0) + freq
        freq_total += freq
    
    for key in word_data:
        word_data[key] /= freq_total

    word_data = sorted_dictionary(word_data)
    return word_data

def get_corpus():
    with open("cfg.toml", "rb") as f:
        cfg = tomllib.load(f)

    randomized_words = []

    for lang_name, lang_weight in cfg["langs"].items():
        data = get_data(lang_name)
        lines = data.splitlines()[:WORD_COUNT_PER_LANG]
        word_data_per_lang = get_word_data(lines)

        print(f"----- {lang_name.upper()} -----")
        print_dict_start(word_data_per_lang, 8)
        print()

        randomized_words_per_lang = random.choices(
            list(word_data_per_lang.keys()),
            weights=word_data_per_lang.values(),
            k=int(lang_weight*WORD_COUNT_FINAL)
        )
        randomized_words.extend(randomized_words_per_lang)

    corpus = " ".join(randomized_words)
    return corpus

corpus = get_corpus()
pyperclip.copy(corpus)

print(f"{WORD_COUNT_FINAL:,} words copied to the clipboard.")
print()
