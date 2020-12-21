from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from typing import List
import numpy as np
from count_vectorizer import MyCountVectorizer


def idf_transform(matrix: List[List[int]]) -> List[int]:
    if len(matrix) == 0:
        return []

    word_count = len(matrix[0])
    doc_count = len(matrix)
    idf_matrix = [0] * word_count

    for doc in matrix:
        for word_index in range(len(doc)):
            if doc[word_index] > 0:
                idf_matrix[word_index] += 1

    for word_index in range(len(idf_matrix)):
        doc_with_word_count = idf_matrix[word_index]
        rel = (doc_count + 1) / (doc_with_word_count + 1)
        idf_matrix[word_index] = np.log(rel) + 1

    return idf_matrix


def tf_transform(matrix: List[List[int]]) -> List[List[int]]:
    tf_matrix = []

    for row in matrix:
        s = sum(row)
        tf_matrix.append([elem / s for elem in row])

    return tf_matrix


class MyTfidfTransformer:
    @staticmethod
    def fit_transform(count_matrix: List[List[int]]) -> List[List[int]]:
        tf_matrix = tf_transform(count_matrix)
        idf_matrix = tf_transform(count_matrix)

        tf_idf_matrix = idf_matrix
        for row_index in range(len(idf_matrix)):
            for column_index in range(len(idf_matrix[row_index])):
                idf_matrix[row_index][column_index] *= tf_matrix[column_index]

        return tf_idf_matrix


class TfidVectorizer2(MyCountVectorizer):
    def __init__(self):
        super().__init__()
        self.tfidf_transformer = TfidfTransformer()  # "composition"

    def fit_transform(self, corpus: Iterable[str]) -> List[List[int]]:
        x = super().fit_transform(corpus)
        matrix = self.tfidf_transformer.fit_transform(x)

        return matrix


def main():
    corpus = [
        "Crock Pot Pasta Never boil pasta again",
        "Pasta Pomodoro Fresh ingredients Parmesan to taste",
    ]
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    print(feature_names)
    matrix = count_matrix.toarray()
    temp_matrix = [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    ]
    print(matrix)
    tf_matrix = tf_transform(temp_matrix)
    print(tf_matrix)
    idf_matrix = idf_transform(temp_matrix)
    print(idf_matrix)

    transformer = TfidfTransformer()

    tfidf_matrix = transformer.fit_transform(temp_matrix)
    print("TF-IDF MATRIX")
    print(tfidf_matrix.toarray())
    transformer = MyTfidfTransformer()
    tfidf_matrix = transformer.fit_transform(temp_matrix)
    print(tfidf_matrix)


if __name__ == "__main__":
    main()
