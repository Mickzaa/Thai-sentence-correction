import numpy as np
from pythainlp.tokenize import word_tokenize, sent_tokenize



def word_correction_choice(input_words, unigrame, bigrame, trigrame, unigrame_obj):
    # Find possible word for each word
    record_possible_word = []
    for word in input_words:
        # Corrosion set of a word
        each_word_list = unigrame_obj.candidate(word)
        record_possible_word.append(each_word_list)

    # Combine each possible words to trigram word
    if len(record_possible_word) != 0:
        all_edit_words = list()
        for i in range(len(input_words)):
            for item in record_possible_word[i]:
                if i == 0:
                    new_word = item + input_words[1] + input_words[2]
                elif i == 1:
                    new_word = input_words[0] + item + input_words[2]
                else:
                    new_word = input_words[0] + input_words[1] + item
                all_edit_words.append(new_word)

    # Loop edit word in dict again to find most freq(prob)
    selected_words = []
    freq_words = []
    # after augment may be reduce to 1 words (unigrame dict)
    for item in all_edit_words:
        if item in unigrame.corpus_dict.keys():
            freq_word = unigrame.corpus_dict[item]
            selected_words.append(item)
            freq_words.append(int(freq_word))
        if item in bigrame.corpus_dict.keys():
            freq_word = bigrame.corpus_dict[item]
            selected_words.append(item)
            freq_words.append(int(freq_word))
        if item in trigrame.corpus_dict.keys():
            freq_word = trigrame.corpus_dict[item]
            selected_words.append(item)
            freq_words.append(int(freq_word))

    try:
        highest_freq_word = selected_words[np.argmax(freq_words)]
        return highest_freq_word
    except:
        return "".join(input_words)


def is_overlapped(a, b):
    if a[0] > b[0]:
        a, b = b, a
    if a[1] > b[0]:
        return True
    return False


def add_prop(sentence, candidates, trigrame, engine):
    sentence = list(sentence)
    window_size = 3
    result = []
    for candidate in candidates:
        start, end = candidate["start"], candidate["end"]
        sen = sentence[:]
        sen[start:end] = list(candidate["new_word"])
        segs = word_tokenize(''.join(sen), engine=engine)
        prod = 1
        for i in range(len(segs) - window_size+1):
            gram = segs[i:i+window_size]
            gram = ''.join(gram)
            if gram in trigrame.corpus_dict:
                ele = trigrame.corpus_dict[gram]
            else:
                ele = 0
            prod += int(ele)
        candidate.update({"prop": prod})
        result.append(candidate)
    return result


def remove_overlap(sentence, candidates, trigrame, engine="attacut"):
    candidates_prop = add_prop(sentence, candidates, trigrame, engine)
    candi = candidates_prop
    i = 0
    list_candidate = []
    while i < len(candi):
        a, b, c = None, None, None
        a = [candi[i]["start"], candi[i]["end"]]
        if i + 1 < len(candi):
            b = [candi[i+1]["start"], candi[i+1]["end"]]
        if i + 2 < len(candi):
            c = [candi[i+2]["start"], candi[i+2]["end"]]
        if b is None and c is None:
            list_candidate.append(candi[i])
            break
        if b is not None and c is None:
            if is_overlapped(a, b):
                if candi[i]['prop'] >= candi[i+1]['prop']:
                    list_candidate.append(candi[i])
                else:
                    list_candidate.append(candi[i+1])
            else:
                list_candidate.append(candi[i])
                list_candidate.append(candi[i+1])
            break
        else:
            if is_overlapped(a, b):
                if is_overlapped(a, c):
                    agmax = np.argmax(
                        [candi[i]['prop'], candi[i+1]['prop'], candi[i+2]['prop']])
                    list_candidate.append(candi[agmax])
                    i += 3
                else:
                    if candi[i]['prop'] >= candi[i+1]['prop']:
                        list_candidate.append(candi[i])
                    else:
                        list_candidate.append(candi[i+1])
                    i += 2
            else:
                list_candidate.append(candi[i])
                list_candidate.append(candi[i+1])
                list_candidate.append(candi[i+2])
                i += 3

    list_candidate.sort(reverse=True, key=lambda x: x['prop'])
    return list_candidate


def final_correction(paragraph, unigrame, bigrame, trigrame, unigrame_obj, engine="attacut"):
    """Find the correction word of a misspell word

    Args:
        paragraph (str): text paragraph
        unigrame (Corpus): Corpus object for unigrame 
        bigrame (Corpus): Corpus object for bigrame
        trigrame (Corpus): Corpus object for trigrame
        unigrame_obj (Preprocess): object created from Preprocess
        engine (str, optional): Word segmentation. Defaults to "attacut".
    Return:
        list of dictionary
        start: Start index of the misspell word
        end: End index is excluded (the index will be end-1) 
        old_word: Misspell word that have in corpus dataset
        new_word: Highest frequency of the correct word choices
    """
    def prepare_index(ans_list, length_acc_list, prop=True):
        for idx, sen in enumerate(ans_list):
            if idx != 0:
                for each in sen:
                    each['start'] += length_acc_list[idx-1]
                    each['end'] += length_acc_list[idx-1]
            if not prop:
                del sen[0]['prop']

        return ans_list

    correction_list = list()
    sentence_list = sent_tokenize(paragraph)
    length_acc_list = list()
    length_acc = 0
    for i in sentence_list:
        length_acc += len(i)
        length_acc_list.append(length_acc)

    for text in sentence_list:
        word_deepcut = word_tokenize(text, engine=engine)
        full_word = []
        start_idx_list = []
        end_idx_list = []
        count = 1

        for idx in range(len(word_deepcut)):
            if idx == 0:  # only first index to add </s> for first 2 words
                word = word_deepcut[idx:idx+2]

                start_idx_list.append(0)  # add value 0
                count_word = ''.join(word)
                end_idx_list.append(len(count_word))

                word.insert(0, '<s/>')
                full_word.append(word)

            if idx == len(word_deepcut)-2:
                word = word_deepcut[idx:idx+2]
                count_word = ''.join(word)

                start_idx_list.append(count-1)
                count += len(count_word)
                end_idx_list.append(count-1)
                word.append('<s/>')
                full_word.append(word)
                break

            else:
                word = word_deepcut[idx:idx+3]
                count_word = ''.join(word)
                start_idx_list.append(count-1)
                end_idx_list.append(count+len(count_word)-1)
                count += len(word[0])  # next start index

            full_word.append(word)
            start_idx_list[1] = 0 

        wrong_words = []
        wrong_word_combine = []
        selected_start_index = []
        selected_end_index = []

        for i in range(len(full_word)):
            tri_word = "".join(full_word[i])
            if tri_word not in trigrame.words:
                wrong_words.append(full_word[i])
                wrong_word_combine.append(tri_word)
                selected_start_index.append(start_idx_list[i])
                selected_end_index.append(end_idx_list[i])

        edit_word_list = []
        # find correct word
        for item in wrong_words:
            correct_one = word_correction_choice(item, unigrame, bigrame, trigrame, unigrame_obj)
            edit_word_list.append(correct_one)

        result = []
        for i in range(len(edit_word_list)):
            edit_word = {}
            if wrong_word_combine[i] != edit_word_list[i]:
                edit_word["start"] = selected_start_index[i]
                edit_word["end"] = selected_end_index[i]
                edit_word["old_word"] = wrong_word_combine[i]
                edit_word["new_word"] = edit_word_list[i]
                result.append(edit_word)

        correction_list.append(result)

    correction_list = [remove_overlap(sentence_list[index], correction_list[index], trigrame, engine)[:2] for index in range(len(correction_list))]
    ans_list = prepare_index(correction_list, length_acc_list, prop=False)
    return ans_list
