# -*- coding: utf-8 -*-

import re
import unicodedata

from collections import defaultdict


def strip_accents(text_string):
    """
    Converts the string to NFD, separates & returns only the base characters
    :param text_string:
    :return: input string without diacritic adornments on base characters
    """
    return ''.join(c for c in unicodedata.normalize('NFD', text_string)
                   if unicodedata.category(c) != 'Mn')


def strip_accents_from_file(filename, outfilename):
    """
    Reads filename containing diacritics, converts to NFC for consistency,
    then writes outfilename with diacritics removed
    :param filename:
    :param outfilename:
    :return: None
    """
    text = ''.join(c for c in unicodedata.normalize('NFC', open(filename, encoding="utf-8").read()))
    try:
        f = open(outfilename, 'w')
    except EnvironmentError:
        return False
    else:
        with f:
            f.write(strip_accents(text))
        return True


def is_text_nfc(text):
    nfc_text = ''.join(c for c in unicodedata.normalize('NFC', text))
    if nfc_text == text:
        return True
    else:
        return False


def convert_text_to_nfc(text):
    return unicodedata.normalize('NFC', text)


def convert_file_to_nfc(filename, outfilename):
    try:
        text = ''.join(c for c in unicodedata.normalize('NFC', open(filename, encoding="utf-8").read()))
        with open(outfilename, 'w', encoding="utf-8") as f:
            f.write(text)
    except EnvironmentError:
        return False
    else:
        return True


def file_info(filename):
    print("\nFilename: " + filename)
    lines = tuple(open(filename, 'r', encoding="utf-8"))
    num_utts = len(lines)

    text = ''.join(c for c in unicodedata.normalize('NFC', open(filename, encoding="utf-8").read()))
    words = re.findall('\w+', text)
    num_words = len(words)
    num_chars = len(re.findall(r'\S', text))

    unique_chars = set(text)
    num_uniq_chars = len(unique_chars)

    print(sorted(unique_chars))
    print("# utts      : " + str(num_utts))
    print("# chars     : " + str(num_chars))
    print("# uniq chars: " + str(num_uniq_chars))

    # unaccented word stats
    unaccented_words = 0
    for word in words:
        if word == strip_accents(word):
            unaccented_words += 1

    print("# total words: " + str(num_words))
    print("# unaccented words : " + str(unaccented_words))

    # ambiguous word stats
    ambiguity_map = defaultdict(set)
    for word in words:
        no_accents = strip_accents(word)
        ambiguity_map[no_accents].add(word)

    ambiguous_words = 0
    ambiguous_words_2 = 0
    ambiguous_words_3 = 0
    ambiguous_words_4 = 0
    ambiguous_words_5 = 0
    ambiguous_words_6 = 0
    ambiguous_words_7 = 0
    ambiguous_words_8 = 0
    ambiguous_words_9 = 0

    # fill ambiguity map
    for word in ambiguity_map:
        if len(ambiguity_map[word]) > 1:
            ambiguous_words += 1
        if len(ambiguity_map[word]) == 2:
            ambiguous_words_2 += 1
        elif len(ambiguity_map[word]) == 3:
            ambiguous_words_3 += 1
        elif len(ambiguity_map[word]) == 4:
            ambiguous_words_4 += 1
        elif len(ambiguity_map[word]) == 5:
            ambiguous_words_5 += 1
        elif len(ambiguity_map[word]) == 6:
            ambiguous_words_6 += 1
        elif len(ambiguity_map[word]) == 7:
            ambiguous_words_7 += 1
        elif len(ambiguity_map[word]) == 8:
            ambiguous_words_8 += 1
        elif len(ambiguity_map[word]) == 9:
            ambiguous_words_9 += 1

    # print ambiguity map
    for word in ambiguity_map:
        # if len(ambiguity_map[word]) == 2:
        # el
        if len(ambiguity_map[word]) == 3:
            print("# 3: " + str(ambiguity_map[word]))
        elif len(ambiguity_map[word]) == 4:
            print("# 4: " + str(ambiguity_map[word]))
        elif len(ambiguity_map[word]) == 5:
            print("# 5: " + str(ambiguity_map[word]))
        elif len(ambiguity_map[word]) == 6:
            print("# 6: " + str(ambiguity_map[word]))
        elif len(ambiguity_map[word]) == 7:
            print("# 7: " + str(ambiguity_map[word]))
        elif len(ambiguity_map[word]) == 8:
            print("# 8: " + str(ambiguity_map[word]))
        elif len(ambiguity_map[word]) == 9:
            print("# 9: " + str(ambiguity_map[word]))

    print("# unique ambiguous words : " + str(ambiguous_words))
    print("# total unique non-diacritized words : " + str(len(ambiguity_map)))

    unique_all_words = set()
    for word in words:
        unique_all_words.add(word)

    print("# total unique words : " + str(len(unique_all_words)))
    print("# ambiguous 2 words : " + str(ambiguous_words_2))
    print("# ambiguous 3 words : " + str(ambiguous_words_3))
    print("# ambiguous 4 words : " + str(ambiguous_words_4))
    print("# ambiguous 5 words : " + str(ambiguous_words_5))
    print("# ambiguous 6 words : " + str(ambiguous_words_6))
    print("# ambiguous 7 words : " + str(ambiguous_words_7))
    print("# ambiguous 8 words : " + str(ambiguous_words_8))
    print("# ambiguous 9 words : " + str(ambiguous_words_9))


def split_corpus_on_symbol(filename, outfilename, symbol=','):
    """ 
    For yoruba blog (and probably bibeli mimo)

    Args: filenames for I/O and symbol to split lines on
    Returns: writes outputfile
    """

    lines = tuple(open(filename, 'r', encoding="utf-8"))

    min_words_to_split = 10
    min_words_in_utt = 5

    with open(outfilename, 'w', ) as f:
        # split out heavily comma'd text :((
        for line in lines:
            if symbol in line:
                num_words = len(line.split())
                num_commas = line.count(symbol)
                curr_comma_position = line.index(symbol)
                num_words_ahead_of_curr_comma = len(line[0:curr_comma_position].split())

                curr_line = line
                while num_commas > 0:
                    if num_words < min_words_to_split:
                        # print(curr_line.strip())
                        f.write(curr_line)
                        break
                    if num_words >= min_words_to_split:
                        if num_words_ahead_of_curr_comma >= min_words_in_utt and \
                                        len((curr_line)[curr_comma_position:].split()) >= min_words_in_utt:
                            f.write((curr_line)[0:curr_comma_position] + "\n")

                            # update vars
                            curr_line = curr_line[curr_comma_position +1:]
                            num_words = len(curr_line.split())
                            num_commas = num_commas - 1
                            if num_commas > 0:
                                curr_comma_position = curr_line.index(symbol)
                                num_words_ahead_of_curr_comma = len(curr_line[0:curr_comma_position].split())
                            else:
                                f.write(curr_line)
                        else:
                            # ignore too short comma (+= vs = on current comma position)
                            num_commas = num_commas - 1
                            if num_commas > 0: # for say 3 commas
                                curr_comma_position += curr_line[curr_comma_position +1:].index(symbol) + 1
                                num_words_ahead_of_curr_comma = len(curr_line[0:curr_comma_position].split())
                            else:
                                f.write(curr_line)
                    else:
                        f.write(curr_line)
            else:
                f.write(line)

if __name__ == "__main__":

    # test
    print(is_text_nfc("Kílódé, ṣèbí àdúrà le̩ fé̩ gbà nbẹ?"))  # NFD
    print(is_text_nfc("Kílódé, ṣèbí àdúrà le̩ fé̩ gbà nbẹ?"))  # NFC