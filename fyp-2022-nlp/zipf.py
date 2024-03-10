import collections
import pickle
from os.path import exists

import matplotlib.pyplot as plt
import nltk.tokenize
import numpy
import pandas
import seaborn
from tqdm import tqdm


def pickle_tokeized_ncv16():
    tok = nltk.tokenize.TreebankWordTokenizer()

    corpus = []
    with open("data/news-commentary-v16.en", "r") as f:
        corpus.extend(t for line in f for t in tok.tokenize(line))

    with open("data/ncv16-list.pickle", "wb") as f:
        pickle.dump(corpus, f)


def load_pickled_ncv16():
    if not exists("data/ncv16-list.pickle"):
        pickle_tokeized_ncv16()
    with open("data/ncv16-list.pickle", "rb") as f:
        corpus = pickle.load(f)
    return corpus


def plot_zipf_distribution():
    corpus = load_pickled_ncv16()

    voc = collections.Counter(corpus)
    frq = pandas.DataFrame(voc.most_common(), columns=["token", "frequency"])

    # Index in the sorted list
    frq["idx"] = frq.index + 1

    # Frequency normalised by corpus size
    frq["norm_freq"] = frq.frequency / len(corpus)

    # Cumulative normalised frequency
    frq["cumul_frq"] = frq.norm_freq.cumsum()

    seaborn.set_theme(style="whitegrid")

    # Plot: Cumulative frequency by index
    seaborn.relplot(x="idx", y="cumul_frq", data=frq, edgecolor="none")
    plt.show()

    # Plot: Cumulative frequency by index, top 10000 tokens
    seaborn.relplot(x="idx", y="cumul_frq", data=frq[:10000], edgecolor="none")
    plt.show()

    # Plot: Log-log plot for Zipf's law
    frq["log_frq"] = numpy.log(frq.frequency)
    frq["log_rank"] = numpy.log(frq.frequency.rank(ascending=False))
    seaborn.relplot(x="log_rank", y="log_frq", data=frq, edgecolor="none")
    plt.show()


if __name__ == "__main__":
    plot_zipf_distribution()
