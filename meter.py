import re

# pip install more-itertools
from more_itertools import peekable

TEST_PADAS = [
    # 1.1.1a
    {
        "text": "agním īḷe puróhitaṁ",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["ag", "ní", "m ī", "ḷe", " ", "pu", "ró", "hi", "taṁ"],
            # HS HH LHLH
            "scansion": "HS_HH | LHLH",
        }
    },
    # 1.1.1b
    {
        "text": "yajñásya devám r̥tvíjam",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["yaj", "ñás", "ya", " ", "de", "vá", "m r̥t", "ví", "jam"],
            # HHL HL HLH
            "scansion": "HHL H|L_HLH",
        }
    },
    # 1.1.1c
    {
        "text": "hótāraṁ  ratnadhā́tamam",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["hó", "tā", "raṁ", " ", "rat", "na", "dhā́", "ta", "mam"],
            # HHH HLHLH
            "scansion": "HHH H|LHLH",
        }
    },
    # 10.144.04c
    {
        "text": "śatácakraṁ yo\ 'hyo\ vartaníḥ",
        "stanza_meter": "",
        "analysis": {
            "parts": ["śa", "tá", "cak", "raṁ", " ", "yo h", "yo", " ", "var", "ta", "níḥ"],
            "scansion": "LLHH H_H HLH",
        }
    },
    # 10.166.02b
    {
        "text": "índra 'vā́riṣṭo@ ákṣataḥ",
        "stanza_meter": "Aṇuṣṭubh",
        "analysis": {
            "parts": ["ín", "dra", " ", "vā́", "riṣ", "ṭo", " ", "ák", "ṣa", "taḥ"],
            "scansion": "HL HH|H HLH",
        }
    },
    # faked
    {
        "text": "hótāra  pratnadhā́tama",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["hó", "tā", "ra p", "rat", "na", "dhā́", "ta", "ma"],
            "scansion": "HHH_H|LHLL",
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

# FIXME avagraha marker shouldn't be here? should use it to mark preceding vowel as short?
# also figure out what the other special chars are doing here
# FIXME any other special chars?
SPECIAL_CHARACTERS = ['\\', '\'', '@']

def clean_string(string):
    # remove multiple spaces with single word boundary char
    string_normalized = re.sub(" +", WORD_BOUNDARY, string)
    return ''.join(c for c in string_normalized if c not in SPECIAL_CHARACTERS)

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
        elif is_sanskrit_char(c) or is_word_boundary(c):
            sanskrit_char = c
        else:
            raise Exception(f"Unidentifiable character '{c}' in text: \"{text}\"")

        chars.append(sanskrit_char)

    return chars


# divide pada into syllables and word boundaries
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
        if is_word_boundary(c_next) or is_word_boundary(c_next_peeked):
            # don't count word boundary char, just append it to the previous
            c_next += next(chars_iterator, '')
            c_next_peeked = chars_iterator.peek('')

        # useful while debugging
        print(f"current part: '{current_part}' next char: '{c_next}' next peeked char: '{c_next_peeked}'")

        if is_sanskrit_consonant(c_next.strip(WORD_BOUNDARY)) and (
                # -CC-: ratn -> 'rat', 'n' (ra as current_part)
                is_sanskrit_consonant(c_next_peeked.strip(WORD_BOUNDARY)) or
                # C# (pada end position): mam# -> 'mam' (ma as current_part)
                c_next_peeked == ''
            ):

            # account for space being present
            if c_next and c_next[-1] == WORD_BOUNDARY:
                parts.append(current_part + c_next[:-1])
                parts.append(WORD_BOUNDARY)
            else:
                parts.append(current_part + c_next)

            current_part = '' # reset
        else:
            parts.append(current_part)
            # FIXME need to handle this elsewhere too?
            if c_next and c_next[0] == WORD_BOUNDARY:
                parts.append(WORD_BOUNDARY)
                current_part = c_next[1:]
            else:
                current_part = c_next # save for next iteration

    return parts


def analyze(pada_text, stanza_meter=""):
    #"Triṣṭubh"
    #"Aṇuṣṭubh"
    #"Gāyatrī"

    parts = get_pada_parts(clean_string(pada_text))

    return {
        "parts": parts,
        "scansion": "",
    }


if __name__ == '__main__':
    for pada in TEST_PADAS:
        # tests
        #print(" ".join(VOWELS))
        #print(" ".join(CONSONANTS))

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
