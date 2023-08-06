"""
Natural Language Processing functionality specific to fidescls
"""

import logging
import re
import warnings
from typing import Dict, Iterable, List, Mapping, Tuple, Union
import spacy
from spacy import tokenizer, symbols, tokens


NLP_MODEL = "en_core_web_lg"
NLP = spacy.load(NLP_MODEL)
# capture a list of special tokens that we'd want to make sure get handled as expected
SPECIAL_TOKENS = {"id": ("id",)}


def get_nlp_tokenizer(
    special_cases: Union[None, Mapping[str, Iterable[str]]] = None,
    vocab: spacy.vocab.Vocab = NLP.vocab,
) -> tokenizer.Tokenizer:
    """
    Setup custom tokenizer with special cases
    https://spacy.io/usage/linguistic-features/#special-cases
    TODO: Find a way to do this once instead of for each tokenization

    Args:
        special_cases: array of strings that need special handling to make sure they get tokenized properly
        e.g.
                {
                'gimme': (gim, me),
                'id': (id)
                }
        vocab: spacy vocab language
    """
    if not special_cases:
        special_cases = SPECIAL_TOKENS
    vocab_tokenizer = tokenizer.Tokenizer(vocab)
    for word, special_tokens in special_cases.items():
        special_case = [{symbols.ORTH: token} for token in special_tokens]
        logging.debug(f"Adding special case for tokenization: {special_case}")
        vocab_tokenizer.add_special_case(word, special_case)
    return vocab_tokenizer


def tokenize(
    text: str, special_cases: Union[None, Mapping[str, Iterable[str]]] = None
) -> spacy.tokens.doc.Doc:
    """
    Convert a string to a spacy tokenized document
    Args:
        text: the text string to be tokenized
        special_cases: special token cases used to initialize the nlp framework

    Returns:
        the input text tokens
    """
    # TODO: inspect latency with instantiating the tokenizer with every call
    vocab_tokenizer = get_nlp_tokenizer(
        special_cases=special_cases if special_cases else SPECIAL_TOKENS
    )
    return vocab_tokenizer(text)


def get_top_n_dict(
    dict_to_sort: Dict, top_n: Union[int, None] = 1, descending: bool = True
) -> List[Tuple[str, float]]:
    """
    Sort and filter dictionary by value
    Args:
        dict_to_sort: dictionary to sort by its value
        top_n: number of top results to filter down to (set to None for all values returned in sorted order)
        descending: which direction to sort the dictionary values

    Returns:
        A dictionary with the `top_n` entries, sorted by value in `descending` order
    """
    return sorted(dict_to_sort.items(), key=lambda x: x[1], reverse=descending)[:top_n]


def similarity(
    text1: Union[str, tokens.doc.Doc], text2: Union[str, tokens.doc.Doc]
) -> float:
    """
    Perform a spacy similarity (cosine) between two strings or docs
    Args:
        text1: a string or spacy doc to compare
        text2: a string or spacy doc to compare

    Returns:
        Similarity value [0,1] - 0: not similar, 1: exact same
    """
    logging.debug(f"Checking similarity between [{text1}] and [{text2}]")
    # TODO figure out how to best handle empty vectors (word not in vocabulary)
    with warnings.catch_warnings():
        warnings.filterwarnings("error")
        try:
            if isinstance(text1, str):
                text1 = tokenize(text1)
            if isinstance(text2, str):
                text2 = tokenize(text2)
            return text1.similarity(text2)
        except UserWarning as warn:
            logging.debug(
                f"Similarity is 0 due to either [{text1}] or [{text2}] not in vocab! {warn}"
            )
            return 0.0


def preprocess_text(
    text: str,
    remove_stop_words: bool = True,
    removal_pattern: str = r"_|\/|\.(?!\s|$)|\d",
    replacement_pattern: str = " ",
) -> str:
    """
    Pre-process text by removing and splitting based on a removal pattern
    Args:
        text: text to be processed
        remove_stop_words: flag to remove spacy default stop words
        removal_pattern: regex pattern of which characters to remove
        replacement_pattern:

    Returns:

    """
    # TODO: the text gets tokenized here and has to be re-tokenized after, efficiency to be gained here
    doc = tokenize(re.sub(removal_pattern, replacement_pattern, text).lower())
    if remove_stop_words:
        # TODO: research around if we may want to be a bit more particular about stop words
        return " ".join(
            [token.text for token in doc if token.text not in NLP.Defaults.stop_words]
        )
    return " ".join([token.text for token in doc])
