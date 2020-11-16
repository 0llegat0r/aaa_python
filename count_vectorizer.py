from typing import Iterable, Dict, List
import re


class MyCountVectorizer:
    def __init__(self, vocabulary: Dict[str, int] = None) -> None:
        if vocabulary is not None:
            self._vocabulary = {
                key: value
                for key, value in sorted(vocabulary.items(), key=lambda x: x[1])
            }
            self._validate_vocabulary_type()
        else:
            self._vocabulary = None

    def get_feature_names(self):
        return list(self._vocabulary.keys())

    def _validate_vocabulary_type(self) -> None:
        if not isinstance(self._vocabulary, Dict):
            raise TypeError("vocabulary has non-dict type")

        for key, value in self._vocabulary.items():
            if not isinstance(key, str):
                raise TypeError("vocabulary key has non-str type")

            if not isinstance(value, int):
                raise TypeError("vocabulary value has non-int type")

        count = len(self._vocabulary)
        if set(range(count)) != set(self._vocabulary.values()):
            raise ValueError(
                "vocabulary values don't from a sequence from 0 to {}".format(count)
            )

    @staticmethod
    def _validate_corpus_type(corpus: Iterable[str]) -> None:
        if not isinstance(corpus, Iterable):
            raise TypeError("corpus has non-iterable type")

        for text in corpus:
            if not isinstance(text, str):
                raise TypeError("element in corpus has non-str type")

    def _fit_vocabulary(self, corpus: Iterable[str]) -> None:
        vocabulary = {}
        i = 0
        for text in corpus:
            for word in self._split(text):
                if word not in vocabulary:
                    vocabulary[word] = i
                    i += 1

        self._vocabulary = vocabulary

    @staticmethod
    def _split(text: str) -> List[str]:
        return re.split("\\W+", text.lower())

    def fit_transform(self, corpus: Iterable[str]) -> List[List[int]]:
        self._validate_corpus_type(corpus)

        if self._vocabulary is None:
            self._fit_vocabulary(corpus)

        return self._get_counts(corpus)

    def _get_counts(self, corpus: Iterable[str]) -> List[List[int]]:
        vectors = []
        for text in corpus:
            vector = [0] * len(self._vocabulary)
            for token in self._split(text):
                if token in self._vocabulary:
                    vector[self._vocabulary[token]] += 1

            vectors.append(vector)

        return vectors


def test_default() -> None:
    corpus = [
        "Crock Pot Pasta Never boil pasta again",
        "Pasta Pomodoro Fresh ingredients Parmesan to taste",
    ]
    vectorizer = MyCountVectorizer()
    x = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    assert feature_names == [
        "crock",
        "pot",
        "pasta",
        "never",
        "boil",
        "again",
        "pomodoro",
        "fresh",
        "ingredients",
        "parmesan",
        "to",
        "taste",
    ]
    assert x == [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    ]


def test_with_custom_vocabulary() -> None:
    corpus = ["word index word", "test index test"]
    vocabulary = {"index": 1, "test": 0}
    vectorizer = MyCountVectorizer(vocabulary)
    y = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    assert feature_names == ["test", "index"]
    assert y == [[0, 1], [2, 1]]


def main():
    test_default()
    test_with_custom_vocabulary()
    v = MyCountVectorizer()
    v.fit_transform()


if __name__ == "__main__":
    main()
