import argparse
from pythainlp.spell import NorvigSpellChecker
from utils import Corpus, CorpusDownload, Preprocess
from utils import final_correction


def parse_args():
    """
    Params: 
        --file: str
                Path of text file
                Default as input_text.txt
        --engine: str
                Word segmentation engine: attacut, deepcut
                Default as attacut
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="input_text.txt")
    parser.add_argument("--engine", type=str, default="attacut")
    return parser.parse_args()


def main():
    """Main program of Thai sentence correction
    Download unigrame, bigrame, trigrame
    Read an input text file
    final_correction function will return 

    Returns:
        list of dictionary
        start: Start index of the misspell word
        end: End index is excluded (the index will be end-1) 
        old_word: Misspell word that have in corpus dataset
        new_word: Highest frequency of the correct word choices
    """
    args = parse_args()
    
    checker = NorvigSpellChecker()

    # Download Dataset
    unigrame = Corpus(dict(checker.dictionary()))
    bigrame = CorpusDownload("tnc_bigram_word_freqs")
    trigrame = CorpusDownload("tnc_trigram_word_freqs")

    # Preprocess a unigrame to be unigram corrosion object
    uni_cor_obj = Preprocess(unigrame)

    # Read text file
    if args.file:
        with open(args.file, "r", encoding="utf8") as f:
            paragraph = f.readline()

    # Word correction
    if args.engine:
        word_correct_hist = final_correction(paragraph, unigrame, bigrame, trigrame, uni_cor_obj, engine=args.engine)
        return word_correct_hist


if __name__ == "__main__":
    word_correct_hist = main()
    print(word_correct_hist)