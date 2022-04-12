from pythainlp.spell import NorvigSpellChecker
from pythainlp.corpus import download , get_corpus_path , get_corpus

class Corpus():
    """Corpus attribute of word, frequency in a corpus"""
    def __init__(self, corpus_dict):
        self.corpus_dict = corpus_dict
        self.words = list(self.corpus_dict.keys())
        self.freqs = list(self.corpus_dict.values())

    def __len__(self):
        return len(self.dict_corpus)

    def __getitem__(self, word):
        return self.dict_corpus[word]


class CorpusDownload(Corpus):
    """CorpusDownload is a child class of Copus 
        Download bigrame, trigrame from pythainlp

    Args:
        corpus_name (str): Name of the corpus provided by pythainlp library
                            https://pythainlp.github.io/pythainlp-corpus/tnc_bigram_word_freqs.html
    Return:
        dictionary: key will be word, value will be frequency
    """
    def __init__(self, corpus_name):
        self.corpus_name = corpus_name
        dict_corpus = self.download_corpus(self.corpus_name)
        Corpus.__init__(self, dict_corpus)

    def download_corpus(self, name):
        download(name)
        path = get_corpus_path(name)
        data = get_corpus(path)
        word = ["".join(x.split("\t")[:-1]) for x in data]
        freq = ["".join(x.split("\t")[-1]) for x in data]
        dict_corpus = dict(zip(word, freq))
        return dict_corpus
