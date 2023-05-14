import re

# pip install more-itertools
from more_itertools import peekable

TEST_PADAS = [
    {
        "text": "agním īḷe puróhitaṁ",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["ag", "ní", "m ī", "ḷe", " ", "pu", "ró", "hi", "taṁ"],
            # HS HH LHLH
            "scansion": "HS_HH | LHLH",
        }
    },
    {
        "text": "yajñásya devám r̥tvíjam",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["yaj", "ñás", "ya", " ", "de", "vá", "m r̥t", "ví", "jam"],
            # HHL HL HLH
            "scansion": "HHL H|L_HLH",
        }
    },
    {
        "text": "hótāraṁ  ratnadhā́tamam",
        # TODO add a test case for this too
        #"text": "hótāraṁ  ratnadhā́tama",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["hó", "tā", "raṁ", " ", "rat", "na", "dhā́", "ta", "mam"],
            # HHH HLHLH
            "scansion": "HHH H|LHLH",
        }
    },
    # {
    #     "text": "tvā́ṁ hy àgne sádam ít samanyávo",
    #     "stanza_meter": "",
    #     "analysis": {
    #         "parts": [],
    #         "scansion": "",
    #     }
    # },
]

#TEST_PADAS = [ TEST_PADAS[2] ]

###############################################################################

VOWELS = [
    'a', 'ā',
    'i', 'ï', 'ī', 'ī3',
    'u', 'ü', 'ū',
    'r̥', 'r̥̄', 'l̥',
    'e', 'ai', 'o', 'au',
    # accented varieties
    'á', 'à', 'ā́', 'ā̀',
    'í', 'ì', 'ī́', 'ī̀',
    'ú', 'ù', 'ū́', 'ū̀',
    # TODO add accented r̥̄ too?
    'ŕ̥', 'r̥̀',
    'é', 'è','ó', 'ò',
    'aí', 'aì', 'aú', 'aù',
]

CONSONANTS = [
    'k', 'kh', 'g', 'gh', 'ṅ',
    'c', 'ch', 'j', 'jh', 'ñ',
    'ṭ', 'ṭh', 'ḍ', 'ḍh', 'ṇ',
    't', 'th', 'd', 'dh', 'n',
    'p', 'ph', 'b', 'bh', 'm',
    'y', 'r', 'l', 'v',
    'ś', 'ṣ', 's', 'h',
    # extras
    'ḷ', 'ḷh',
    # FIXME anunasika as vowel?
    'ṁ', 'ḥ', 'm̐',
]

WORD_BOUNDARY = ' '

def is_sanskrit_vowel(str):
    return str in VOWELS

def is_sanskrit_consonant(str):
    return str in CONSONANTS

def is_sanskrit_char(str):
    return is_sanskrit_vowel(str) or is_sanskrit_consonant(str)

def is_word_boundary(str):
    return str == WORD_BOUNDARY

###############################################################################

def get_sanskrit_chars(text):
    chars = []

    text_iterator = peekable(text)
    while (c := next(text_iterator, '')):
        if is_sanskrit_char(c +  text_iterator.peek('')):
            sanskrit_char = c + next(text_iterator, '')
            #print(sanskrit_char)
        else:
            sanskrit_char = c

        chars.append(sanskrit_char)

    return chars


def get_pada_parts(text):
    parts = []

    current_part = ''
    chars_iterator = peekable(get_sanskrit_chars(text))

    while (c := next(chars_iterator, '')):
        # keep accumulating till we hit a vowel character
        if not is_sanskrit_vowel(c):
            current_part += c
            continue

        current_part += c

        c_next = next(chars_iterator, '')
        c_next_peeked = chars_iterator.peek('') # peeking the one after above
        if is_word_boundary(c_next_peeked):
            c_next += next(chars_iterator, '')
            # next(chars_iterator, '')
            # c_next += '_'
            # print("found word boundary")
            # print(c_next)
            c_next_peeked = chars_iterator.peek('')

        # useful while debugging
        #print(f"current part: '{current_part}' next char: '{c_next}' next peeked char: '{c_next_peeked}'")

        if is_sanskrit_consonant(c_next.strip()) and (
                # -CC-: ratn -> 'rat', 'n' (ra as current_part)
                is_sanskrit_consonant(c_next_peeked.strip()) or
                # -C : ram -> 'ram', ' ' (ra as current_part)
                #is_word_boundary(c_next_peeked) or
                # C# (pada end position): mam# -> 'mam' (ma as current_part)
                c_next_peeked == '' # pada end
            ):
            #print(current_part, c_next)

            # account for space being present
            if c_next[-1] == WORD_BOUNDARY:
                parts.append(current_part + c_next[:-1])
                parts.append(WORD_BOUNDARY)
            else:
                parts.append(current_part + c_next)

            current_part = '' # reset
        else:
            #print(current_part, c_next)
            parts.append(current_part)
            # FIXME need to handle this elsewhere too?
            if c_next == WORD_BOUNDARY:
                parts.append(c_next)
                current_part = '' # reset
            else:
                current_part = c_next # save for next iteration

    return parts


def analyze(pada_text, stanza_meter=""):
    #"Triṣṭubh"
    #"Aṇuṣṭubh"
    #"Gāyatrī"

    # remove multiple spaces with single word boundary char
    pada_text_normalized = re.sub(" +", WORD_BOUNDARY, pada_text)

    parts = get_pada_parts(pada_text_normalized)

    return {
        "parts": parts,
        "scansion": "",
    }


if __name__ == '__main__':
    for pada in TEST_PADAS:
        # input
        print(f'\n{pada["text"]} ({pada["stanza_meter"]})')

        # output
        analysis = analyze(pada["text"], pada["stanza_meter"])
        print(f'{analysis["parts"]} {analysis["scansion"]}')

        # check output against expected
        analysis_expected = pada["analysis"]
        analysis_expected["scansion"] = "" # TODO remove, for initial testing only
        if analysis != analysis_expected:
            print(f'Not as expected: \n{analysis_expected["parts"]} {analysis_expected["scansion"]}\n')

        # tests
        #print(" ".join(VOWELS))
        #print(" ".join(CONSONANTS))
