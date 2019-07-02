from gensim.models.ldamodel import LdaModel
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary

class Lda:
    def __init__(self):
        self.model = None
        self.common_dictionary = None
        pass

    def train(self, common_texts, num_topics):
        self.common_dictionary = Dictionary(common_texts)
        common_corpus = [self.common_dictionary.doc2bow(text) for text in common_texts]
        self.model = LdaModel(common_corpus, num_topics=num_topics, alpha='auto', eval_every=5)

    def get_topics(self, words=None):
        s = self.model.get_topics().T
        if words is not None:
            common_corpus = self.common_dictionary.doc2idx(words)
            s = s[common_corpus]
        return s

if __name__ == '__main__':
    common_texts = [
        ['a', 'b', 'c'],
        ['a', 'b', 'c'],
        ['a', 'b', 'c'],
        ['a', 'b', 'c'],
        ['a', 'b', 'c'],
    ]
    model = Lda()
    model.train(common_texts, 2)
    print(model.get_topics())
    print(model.get_topics(['c', 'b']))
