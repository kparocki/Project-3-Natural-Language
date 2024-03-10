import re

import pandas as pd
from nltk import sent_tokenize, word_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline


def tokenizeLine(line, sent_Tokenize=True, removespecial=False):
    """Tokenizes line using nltk sentence and word tokenizer

    Args:
        line (string): Input string
        removespecial (bool, optional): Remove special characters if true
        sent_Tokenize (bool, optional): recognize sentence default is true

    Returns:
        list: of tokenized sentences
    """
    line = line.lower()
    if removespecial:
        line = re.sub(r"[^a-zA-Z]+", " ", line)

    return (
        [word_tokenize(t) for t in sent_tokenize(line)]
        if sent_Tokenize
        else word_tokenize(line)
    )


def load_to_pd(_type, dataset_name):
    """Load the data into and labels into dataframe, handling weird line endings

    Args:
        _type (string): train, test, or val - specifies what split of data to use
        dataset_name (string): describe wich dataset to use

    Returns:
        DataFrame: resulting dataframe containing text and labels
    """
    x = list()
    with open(f"data/{dataset_name}/{_type}_text.txt", "r", encoding="utf-8") as text:
        for line in text:
            x.append(line.strip("\n"))
    line_df = pd.DataFrame(x), x

    # train_text_df = pd.read_csv(f'data/{dataset}/train_text.txt',sep='\n', header=None)
    text_df, _list = line_df
    labels_df = pd.read_csv(f"data/{dataset_name}/{_type}_labels.txt", header=None)
    df = pd.concat([text_df, labels_df], axis=1)
    df.columns = ["text", "label"]
    return df

def load_augmented_df(_type, dataset_name):
    x = list()
    with open(f"data/{dataset_name}/{_type}_text.txt", "r", encoding="utf-8") as text:
        for line in text:
            x.append(line.strip("\n"))
    line_df = pd.DataFrame(x)
    line_df.columns = ["text"]

    return line_df