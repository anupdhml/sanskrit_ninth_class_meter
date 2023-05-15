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
            # HL HH LHLH
            "scansion": "HL_HH |LHLH",
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
        "text": "hótāraṁ  ratnadhā́tamam ",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["hó", "tā", "raṁ", " ", "rat", "na", "dhā́", "ta", "mam"],
            # HHH HLHLH
            "scansion": "HHH H|LHLH",
        }
    },
    # 1.3.8a
    # avagraha (o_a, a restored for o_') from -aḥ + a-: 'o' as short and 'a' counting towards the meter
    {
        "text": "víśve devā́so aptúraḥ",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["víś", "ve", " ", "de", "vā́", "so", " ", "ap", "tú", "raḥ"],
            # FIXME "so" before 'a' should be short here (devā́saḥ aptúraḥ,
            # with a- restored instaed of the expected avagraha 'ptúraḥ)
            # HH HHH HLH
            "scansion": "HH HH|H HLH",
        }
    },
    # 1.33.13b
    # avagraha (o_') from -aḥ + a-: 'o' as short? metrically long makes sense here
    {
        "text": "ví tigména vr̥ṣabhéṇā púro 'bhet",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["ví", " ", "tig", "mé", "na", " ", "vr̥", "ṣa", "bhé", "ṇā", " ", "pú", "ro", " ", "'bhet"],
            # FIXME "ro" before avagraha should be short here (from "púraḥ abhet")
            # but then it wouldn't follow the meter...
            # L HHL LLHH LH H"
            "scansion": "L HHL ,LLH|H LH H",
        }
    },
    # 10.72.4c
    # avagraha (o_') from -aḥ + a-: 'o' as short
    {
        "text": "áditer dákṣo 'jāyata@",
        "stanza_meter": "Aṇuṣṭubh",
        "analysis": {
            "parts": ["á", "di", "ter", " ", "dák", "ṣo", " ", "'jā", "ya", "ta"],
            # FIXME "ṣo" before avagraha should be short here (from "dákṣaḥ ajāyata")
            # LLH HH HLL"
            "scansion": "LLH H|H HLL",
        }
    },
    # 10.161.5d
    # avagraha (e_') from -e + a-: 'e' as long
    {
        "text": "sárvam ā́yuś ca te 'vidam ",
        "stanza_meter": "Aṇuṣṭubh",
        "analysis": {
            "parts": ["sár", "va", "m ā́", "yuś", " ", "ca", " ", "te", " ", "'vi", "dam"],
            # HL HH L H LH
            "scansion": "HL_HH |L H LH",
        }
    },
    # 1.35.5b
    {
        "text": "ráthaṁ híraṇyapra~ugaṁ váhantaḥ",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["rá", "thaṁ", " ", "hí", "raṇ", "yap", "ra", "~u", "gaṁ", " ", "vá", "han", "taḥ"],
            # LH LHHLLH LHH
            # FIXME no good way to mark caesura here since it's inside a compound
            "scansion": "LH LHH,LL|H LHH",
        }
    },
    # 1.121.1a
    {
        "text": "kád itthā́ nr̥ŕ̥m̐ḥ pā́taraṁ+ devayatā́ṁ",
        "stanza_meter": "",
        "analysis": {
            "parts": ["ká", "d it", "thā́", " ", "nr̥", "ŕ̥m̐", "ḥ pā́", "ta", "raṁ", " ", "de", "va", "ya", "tā́ṁ"],
            # L HH LH HLH HLLH
            "scansion": "L_HH LH_HLH HLLH",
        }
    },
    # 10.129.5b
    {
        "text": "adháḥ svid āsī́3d upári svid āsī3t",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["a", "dháḥ", " ", "svi", "d ā", "sī́3", "d u", "pá", "ri s", "vi", "d ā", "sī3t"],
            # LH L HH LLH L HH
            # FIXME no good way to mark caesura here since it crosses word boundary (du)
            # can check 5th and 6th syllable and see if it has space?
            "scansion": "LH L_HH,L_L|H_L_HH",
        }
    },
    # 10.144.4c
    {
        "text": "śatácakraṁ yo\ 'hyo\ vartaníḥ",
        "stanza_meter": "",
        "analysis": {
            "parts": ["śa", "tá", "cak", "raṁ", " ", "yo 'h", "yo", " ", "var", "ta", "níḥ"],
            # FIXME o before ' should be short? (avagraha)
            # FIXME should mark it _HH?
            "scansion": "LLHH H_H HLH",
        }
    },
    # 10.166.2b
    {
        "text": "índra 'vā́riṣṭo@ ákṣataḥ",
        "stanza_meter": "Aṇuṣṭubh",
        "analysis": {
            "parts": ["ín", "dra", " ", "'vā́", "riṣ", "ṭo", " ", "ák", "ṣa", "taḥ"],
            # FIXME o before a should be short? (avagraha restored)
            "scansion": "HL HH|H HLH",
        }
    },
    # 4.1.1a
    {
        "text": "tuvā́ṁ hí agne sádam ít samanyávo",
        "stanza_meter": "",
        "analysis": {
            "parts": ["tu", "vā́ṁ", " ", "hí", " ", "ag", "ne", " ", "sá", "da", "m ít", " ", "sa", "man", "yá", "vo"],
            # LH L HH LL H LHLH
            "scansion": "LH L HH LL_H LHLH",
        }
    },
    # 4.1.1a (not metrically restored)
    {
        "text": "tvā́ṁ hy àgne sádam ít samanyávo",
        "stanza_meter": "",
        "analysis": {
            "parts": ["tvā́ṁ", " ", "hy àg", "ne", " ", "sá", "da", "m ít", " ", "sa", "man", "yá", "vo"],
            # H HH LL H LHLH
            "scansion": "H _HH LL_H LHLH",
        }
    },
    # faked
    {
        "text": "hótāra  pratnadhā́tama avr̥̄",
        "stanza_meter": "",
        "analysis": {
            "parts": ["hó", "tā", "ra p", "rat", "na", "dhā́", "ta", "ma", " ", "a", "vr̥̄"],
            # FIXME use HH_?
            "scansion": "HHH_HLHLL LH",
        }
    },
]

#TEST_PADAS = [ TEST_PADAS[2] ]

###############################################################################

VOWELS_SHORT = [
    'a',
    'i', 'ï', '~i', # ~i can stand for ï
    'u', 'ü', '~u', # ~u can stand for ü
    'r̥',
    'l̥',
    # accented varieties
    'á', 'à',
    'í', 'ì',
    'ú', 'ù',
    'ŕ̥', 'r̥̀',
    # accented l̥ is not attested
]

VOWELS_LONG = [
    'ā',
    'ī', 'ī3',
    'ū', 'ū3', # the latter is not really attested
    'r̥̄',
    'e', 'ai',
    'o', 'au',
    # accented varieties
    'ā́', 'ā̀',
    'ī́', 'ī̀', 'ī́3',
    'ū́', 'ū̀', 'ū́3',
    # TODO add accented r̥̄, not attested?
    'é', 'è', 'aí', 'aì',
    'ó', 'ò', 'aú', 'aù',
]

VOWELS = VOWELS_SHORT + VOWELS_LONG

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
    'ṁ', 'ḥ', 'm̐',
]

WORD_BOUNDARY = ' '

AVAGRAHA = '\''

MARKER_SYLLABLE_LIGHT = 'L' # alt: ◡
MARKER_SYLLABLE_HEAVY = 'H' # alt: —
MARKER_CADENCE = '|'
MARKER_CAESURA = ','
MARKER_WORD_BOUNDARY_IN_SYLLABLE = '_'

METER_GAYATRI = "Gāyatrī"
METER_ANUSTUBH = "Aṇuṣṭubh"
METER_TRISTUBH = "Triṣṭubh"
# FIXME add tests for this too
METER_JAGATI = "Jagatī"

# TODO figure out what each of these special chars indicate in the vnh text
SPECIAL_CHARACTERS = ['\\', '@', '+']

def clean_string(string):
    # remove multiple spaces with single word boundary char
    string_normalized = re.sub(" +", WORD_BOUNDARY, string.strip())
    return ''.join(c for c in string_normalized if c not in SPECIAL_CHARACTERS)

def is_sanskrit_vowel(str):
    return str in VOWELS

def is_sanskrit_consonant(str):
    # we can mark consonant character with avagraha so strip it off first
    return str.strip(AVAGRAHA) in CONSONANTS

def is_sanskrit_char(str):
    return is_sanskrit_vowel(str) or is_sanskrit_consonant(str)

def is_word_boundary(str):
    return str == WORD_BOUNDARY

def is_avagraha(str):
    return str == AVAGRAHA

def is_light(syllable):
    syllable_chars = [c for c in get_sanskrit_chars(syllable.strip())]

    # some validation
    part_vowel_chars = [c for c in syllable_chars if is_sanskrit_vowel(c)]
    if len(part_vowel_chars) != 1:
        # TODO custom exception with nicer params. also should add pada text here
        raise Exception(
            f"Syllable part '{syllable}' has either zero or more than one vowel"
        )

    last_char = syllable_chars[-1]
    return last_char in VOWELS_SHORT

def is_heavy(syllable):
    return not is_light(syllable)

###############################################################################

def get_sanskrit_chars(text):
    chars = []

    text_iterator = peekable(text)
    has_avagraha = False
    while (c := next(text_iterator, '')):
        if is_avagraha(c):
            has_avagraha = True
            continue

        # support lengthy sanskrit chars like r̥̄ or ī3
        while (c_peeked := text_iterator.peek('')) and is_sanskrit_char(c + c_peeked):
            c += next(text_iterator, '')

        if len(c) > 1 or is_sanskrit_char(c) or is_word_boundary(c):
            if has_avagraha:
                c = AVAGRAHA + c
                has_avagraha = False # reset
            chars.append(c)
        else:
            raise Exception(f"Unidentifiable character '{c}' in text: \"{text}\"")

    #print(chars)
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

        # handles cases when there's a vowel hiatus, like in the case of ~u: híraṇyapra~ugaṁ
        c_next_peeked = chars_iterator.peek('')
        if is_sanskrit_vowel(c_next_peeked):
            parts.append(current_part)
            current_part = '' # reset
            continue

        c_next = next(chars_iterator, '')
        c_next_next_peeked = chars_iterator.peek('') # peeking the one after above

        # TODO consolidate this with the above logic for immediate vowel hiatus?
        if c_next == WORD_BOUNDARY and is_sanskrit_vowel(c_next_next_peeked):
            parts.append(current_part)
            parts.append(WORD_BOUNDARY)
            current_part = '' # reset
            continue

        if is_word_boundary(c_next) or is_word_boundary(c_next_next_peeked):
            # don't count word boundary char, just append it to the previous
            c_next += next(chars_iterator, '')
            c_next_next_peeked = chars_iterator.peek('')

        # useful while debugging
        # print(
        #     f"current part: '{current_part}'",
        #     f"next char: '{c_next}'",
        #     f"next peeked char: '{c_next_next_peeked}'"
        # )

        if is_sanskrit_consonant(c_next.strip(WORD_BOUNDARY)) and (
                # -CC-: ratn -> 'rat', 'n' (ra as current_part)
                is_sanskrit_consonant(c_next_next_peeked.strip(WORD_BOUNDARY)) or
                # C# (pada end position): mam# -> 'mam' (ma as current_part)
                c_next_next_peeked == ''
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
            if c_next and c_next[0] == WORD_BOUNDARY:
                parts.append(WORD_BOUNDARY)
                current_part = c_next[1:]
            else:
                current_part = c_next # save for next iteration

    return parts


def analyze(pada_text, stanza_meter=""):
    parts = get_pada_parts(clean_string(pada_text))

    scansion = ""
    no_of_syllables = 0
    for part in parts:
        if part == WORD_BOUNDARY:
            scansion += WORD_BOUNDARY

            # add the caesura marker
            # FIXME track early and late caesura. also which one wins when both satisfy?
            # also improve caesura marking when 5th or 6th syllable actually has a space
            if (stanza_meter in [METER_TRISTUBH, METER_JAGATI]) and no_of_syllables in [4, 5]:
                scansion += MARKER_CAESURA

            continue

        # add the cadence marker
        if (
            (stanza_meter in [METER_GAYATRI, METER_ANUSTUBH] and no_of_syllables == 4)
            or (stanza_meter in [METER_TRISTUBH, METER_JAGATI] and no_of_syllables == 7)
        ):
            scansion += MARKER_CADENCE

        no_of_syllables += 1

        if WORD_BOUNDARY in part.strip():
            scansion += MARKER_WORD_BOUNDARY_IN_SYLLABLE

        if is_light(part):
            # FIXME handle gachati case
            # FIXME handle o vowel as short before avagraha / a
            scansion += MARKER_SYLLABLE_LIGHT
        else:
            scansion += MARKER_SYLLABLE_HEAVY

    return {
        "parts": parts,
        "scansion": scansion,
        # TODO add this info along with actual syllables
        #"no_of_syllables": no_of_syllables,
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
        # TODO save the test output in a file too?
        analysis_expected = pada["analysis"]
        if analysis != analysis_expected:
            print(f'Not as expected: \n{analysis_expected["parts"]} {analysis_expected["scansion"]}\n')
