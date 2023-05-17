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
            # LS LL SLSL
            "scansion": "LS_LL |SLSL",
            "caesura_position": -1,
        }
    },
    # 1.1.1b
    {
        "text": "yajñásya devám r̥tvíjam",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["yaj", "ñás", "ya", " ", "de", "vá", "m r̥t", "ví", "jam"],
            # LLS LS LSL
            "scansion": "LLS L|S_LSL",
            "caesura_position": -1,
        }
    },
    # 1.1.1c
    {
        "text": "hótāraṁ  ratnadhā́tamam ",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["hó", "tā", "raṁ", " ", "rat", "na", "dhā́", "ta", "mam"],
            # LLL LSLSL
            "scansion": "LLL L|SLSL",
            "caesura_position": -1,
        }
    },
    # 1.1.4c
    # treating ch as long for meter
    {
        "text": "sá íd devéṣu gachati",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["sá", " ", "íd", " ", "de", "vé", "ṣu", " ", "gac", "cha", "ti"],
            # S L LLS LSS
            "scansion": "S L LL|S LSS",
            "caesura_position": -1,
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
            # LL LLL LSL
            "scansion": "LL LL|L LSL",
            "caesura_position": -1,
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
            # S LLS SSLL SL L"
            "scansion": "S LLS ,SSL|L SL L",
            "caesura_position": 4,
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
            # SSL LL LSS"
            "scansion": "SSL L|L LSS",
            "caesura_position": -1,
        }
    },
    # 10.161.5d
    # avagraha (e_') from -e + a-: 'e' as long
    {
        "text": "sárvam ā́yuś ca te 'vidam",
        "stanza_meter": "Aṇuṣṭubh",
        "analysis": {
            "parts": ["sár", "va", "m ā́", "yuś", " ", "ca", " ", "te", " ", "'vi", "dam"],
            # LS LL S L SL
            "scansion": "LS_LL |S L SL",
            "caesura_position": -1,
        }
    },
    # 5.5.5c
    {
        "text": "prá-pra yajñám pr̥ṇītana",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            # FIXME because of -, syllabfication should be pra, pra yielding SS for the meter?
            "parts": ["práp", "ra", " ", "yaj", "ñám", " ", "pr̥", "ṇī", "ta", "na"],
            # LS LL SLSS
            "scansion": "LS LL |SLSS",
            "caesura_position": -1,
        }
    },
    # 5.41.10d
    # metrical pauses
    {
        "text": "śocíṣkeśo ̀ ní riṇāti vánā",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["śo", "cíṣ", "ke", "śo", " \u0300", " ", "ní", " ", "ri", "ṇā", "ti", " ", "vá", "nā"],
            # LLLL · S SLS SL
            "scansion": "LLLL · ,S S|LS SL",
            "caesura_position": 5,
        }
    },
    # 4.19.4c
    {
        "text": "dr̥r̥ḷhā́ni+ aubhnād uśámāna ójo",
        "stanza_meter": "",
        "analysis": {
            "parts": ["dr̥", "r̥", "ḷhā́", "ni", " ", "aubh", "nā", "d u", "śá", "mā", "na", " ", "ó", "jo"],
            # SSLS LL SSLS LL (vedaweb treats ḷh as 2 chars yielding different results here)
            "scansion": "SSLS LL_SSLS LL",
            "caesura_position": -1,
        }
    },
    # 1.51.8a
    {
        "text": "ví jānīhi ā́riyān yé ca dásyavo",
        "stanza_meter": "Jagatī",
        "analysis": {
            "parts": ["ví", " ", "jā", "nī", "hi", " ", "ā́", "ri", "yān", " ", "yé", " ", "ca", " ", "dás", "ya", "vo"],
            # S LLS LSL L S LSL
            "scansion": "S LLS ,LSL |L S LSL",
            "caesura_position": 4,
        }
    },
    # 1.35.5b
    {
        "text": "ráthaṁ híraṇyapra~ugaṁ váhantaḥ",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["rá", "thaṁ", " ", "hí", "raṇ", "yap", "ra", "~u", "gaṁ", " ", "vá", "han", "taḥ"],
            # SL SLLSSL SLL
            # FIXME no good way to mark caesura here since it's inside a compound
            "scansion": "SL SLL,SS|L SLL",
            #"caesura_position": 5,
            "caesura_position": 0,
        }
    },
    # 1.121.1a
    {
        "text": "kád itthā́ nr̥ŕ̥m̐ḥ pā́taraṁ+ devayatā́ṁ",
        "stanza_meter": "",
        "analysis": {
            "parts": ["ká", "d it", "thā́", " ", "nr̥", "ŕ̥m̐", "ḥ pā́", "ta", "raṁ", " ", "de", "va", "ya", "tā́ṁ"],
            # S LL SL LSL LSSL
            "scansion": "S_LL SL_LSL LSSL",
            "caesura_position": -1,
        }
    },
    # 10.129.5b
    {
        "text": "adháḥ svid āsī́3d upári svid āsī3t",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["a", "dháḥ", " ", "svi", "d ā", "sī́3", "d u", "pá", "ri s", "vi", "d ā", "sī3t"],
            # SL S LL SSL S LL
            # FIXME no good way to mark caesura here since it crosses word boundary (du)
            # FIXME! can check 5th and 6th syllable and see if it has space?
            "scansion": "SL S_LL,S_S|L_S_LL",
            #"caesura_position": 5,
            "caesura_position": 0,
        }
    },
    # 10.144.4c
    {
        "text": "śatácakraṁ yo\ 'hyo\ vartaníḥ",
        "stanza_meter": "",
        "analysis": {
            "parts": ["śa", "tá", "cak", "raṁ", " ", "yo 'h", "yo", " ", "var", "ta", "níḥ"],
            # FIXME o before ' should be short? (avagraha)
            # FIXME should mark it _LL?
            "scansion": "SSLL L_L LSL",
            "caesura_position": -1,
        }
    },
    # 10.166.2b
    {
        "text": "índra 'vā́riṣṭo@ ákṣataḥ",
        "stanza_meter": "Aṇuṣṭubh",
        "analysis": {
            "parts": ["ín", "dra", " ", "'vā́", "riṣ", "ṭo", " ", "ák", "ṣa", "taḥ"],
            # FIXME o before a should be short? (avagraha restored)
            "scansion": "LS LL|L LSL",
            "caesura_position": -1,
        }
    },
    # 4.1.1a
    {
        "text": "tuvā́ṁ hí agne sádam ít samanyávo",
        "stanza_meter": "",
        "analysis": {
            "parts": ["tu", "vā́ṁ", " ", "hí", " ", "ag", "ne", " ", "sá", "da", "m ít", " ", "sa", "man", "yá", "vo"],
            # SL S LL SS L SLSL
            "scansion": "SL S LL SS_L SLSL",
            "caesura_position": -1,
        }
    },
    # 4.1.1a (not metrically restored)
    {
        "text": "tvā́ṁ hy àgne sádam ít samanyávo",
        "stanza_meter": "",
        "analysis": {
            "parts": ["tvā́ṁ", " ", "hy àg", "ne", " ", "sá", "da", "m ít", " ", "sa", "man", "yá", "vo"],
            # L LL SS L SLSL
            "scansion": "L _LL SS_L SLSL",
            "caesura_position": -1,
        }
    },
    # faked
    {
        "text": "hótāra  pratnadhā́tama avr̥̄",
        "stanza_meter": "",
        "analysis": {
            "parts": ["hó", "tā", "ra p", "rat", "na", "dhā́", "ta", "ma", " ", "a", "vr̥̄"],
            # FIXME use LL_?
            "scansion": "LLL_LSLSS SL",
            "caesura_position": -1,
        }
    },
    # faked
    # multiple caesura positions eligible (first one wins)
    # FIXME decide win strategy on multiple caesura (first or last)
    {
        "text": "śocíṣkeśo va ní riṇāti vánā",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["śo", "cíṣ", "ke", "śo", " ", "va", " ", "ní", " ", "ri", "ṇā", "ti", " ", "vá", "nā"],
            # LLLL S S SLS SL
            "scansion": "LLLL S ,S S|LS SL",
            # 4 wins over possible 5
            "caesura_position": 4,
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

# space followed by gravis, used in vnh text to mark metrical pauses
PAUSE = ' \u0300'

MARKER_SYLLABLE_SHORT = 'S' # light syllable, alt marker: ◡
MARKER_SYLLABLE_LONG = 'L' # heavy syllable, alt marker: —
MARKER_SYLLABLE_SHORT_OR_LONG = 'X' # light/heavy syllable
#MARKER_PAUSE = 'P' # metrical pause, alt marker: ·
MARKER_PAUSE = '·' # metrical pause, alt marker: P
MARKER_CADENCE = '|'
MARKER_CAESURA = ','
MARKER_WORD_BOUNDARY_IN_SYLLABLE = '_'

METER_GAYATRI = "Gāyatrī"
METER_ANUSTUBH = "Aṇuṣṭubh"
METER_TRISTUBH = "Triṣṭubh"
METER_JAGATI = "Jagatī"

# cadence pattern for our meters
PATTERN_IAMBIC = f"{MARKER_SYLLABLE_SHORT}{MARKER_SYLLABLE_LONG}{MARKER_SYLLABLE_SHORT}"
PATTERN_TROCHAIC = f"{MARKER_SYLLABLE_LONG}{MARKER_SYLLABLE_SHORT}{MARKER_SYLLABLE_LONG}"
PATTERN_TROCHAIC_IAMBIC = f"{MARKER_SYLLABLE_LONG}{MARKER_SYLLABLE_SHORT}{MARKER_SYLLABLE_LONG}{MARKER_SYLLABLE_SHORT}"

METER_SPECS = {
    METER_GAYATRI: {
        "no_of_syllables": 8,
        "cadence_position": 4,
        "scansion_cadence_main": PATTERN_IAMBIC, # positions 5,6,7
    },
    METER_ANUSTUBH: {
        "no_of_syllables": 8,
        "cadence_position": 4,
        "scansion_cadence_main": PATTERN_IAMBIC, # positions 5,6,7
    },
    METER_TRISTUBH: {
        "no_of_syllables": 11,
        "cadence_position": 7,
        "scansion_cadence_main": PATTERN_TROCHAIC, # positions 8,9,10
        "caesura_possible_positions": [4, 5],
        "short_after_caesura_relative_position": 2,
    },
    METER_JAGATI: {
        "no_of_syllables": 12,
        "cadence_position": 7,
        "scansion_cadence_main": PATTERN_TROCHAIC_IAMBIC, # positions 8,9,10
        "caesura_possible_positions": [4, 5],
        "short_after_caesura_relative_position": 2,
    },
}

SPECIAL_CHARACTERS_METER = [
    # MARKER_PAUSE is intentionally not here since it counts towards the meter syllables
    MARKER_CADENCE, MARKER_CAESURA,
    MARKER_WORD_BOUNDARY_IN_SYLLABLE,
    WORD_BOUNDARY
]

# special chars used in the Van Nooten & Holland (vnh) text
# https://lrc.la.utexas.edu/books/rigveda/RV00
SPECIAL_CHARACTERS_SAMHITAPTHA_VNH = [
    '@', '+', # marks explicit restorations: https://lrc.la.utexas.edu/books/rigveda/RV00#bolle
    '-',      # marks internal boundary of amredita (iterative) compounds
    '\\',     # marks independent svarita on the preceding vowel
    '*',      # FIXME figure out what this means, eg: https://vedaweb.uni-koeln.de/rigveda/view/id/9.67.27
]

def clean_vnh_samhitapatha(string):
    return ''.join(c for c in string if c not in SPECIAL_CHARACTERS_SAMHITAPTHA_VNH)

def clean_meter_scansion(string):
    return ''.join(c for c in string if c not in SPECIAL_CHARACTERS_METER)

def is_sanskrit_vowel(str):
    return str in VOWELS

def is_sanskrit_consonant(str):
    # we can mark consonant character with avagraha so strip it off first
    return str.strip(AVAGRAHA) in CONSONANTS

def is_metrical_pause(str):
    return str == PAUSE

def is_sanskrit_char(str):
    # we count metrical pauses as a char since it has a metrical value
    return is_sanskrit_vowel(str) or is_sanskrit_consonant(str) or is_metrical_pause(str)

def is_word_boundary(str):
    return str == WORD_BOUNDARY

def is_avagraha(str):
    return str == AVAGRAHA

def is_metrically_short(syllable):
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

def is_metrically_long(syllable):
    return not is_metrically_short(syllable)

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
            # treat 'ch' spelling as what it actually is: a cluster
            # our input text does not use cch variant so this is safe to do
            if c == "ch":
                c = "c,ch" # comma used temporarily to separate multiple chars
            # if previous marking was that of avagraha, include it as part of the char
            if has_avagraha:
                c = AVAGRAHA + c
                has_avagraha = False # reset
            for sankrit_char in c.split(','):
                chars.append(sankrit_char)
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
        if is_word_boundary(c_next) and is_sanskrit_vowel(c_next_next_peeked):
            parts.append(current_part)
            parts.append(WORD_BOUNDARY)
            current_part = '' # reset
            continue

        # handle metrical pause
        if c_next == PAUSE and is_word_boundary(c_next_next_peeked):
            parts.append(current_part)
            parts.append(PAUSE)
            parts.append(next(chars_iterator, '')) # adds the word boundary
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
            if c_next and is_word_boundary(c_next[-1]):
                parts.append(current_part + c_next[:-1])
                parts.append(WORD_BOUNDARY)
            else:
                parts.append(current_part + c_next)

            current_part = '' # reset
        else:
            parts.append(current_part)
            if c_next and is_word_boundary(c_next[0]):
                parts.append(WORD_BOUNDARY)
                current_part = c_next[1:]
            else:
                current_part = c_next # save for next iteration

    return parts


def generate_scansion(pada_text, meter=""):
    # remove multiple spaces with single word boundary char
    pada_text_normalized = re.sub(" +", WORD_BOUNDARY, pada_text.strip())
    # clean special characters in the text
    pada_text_cleaned = clean_vnh_samhitapatha(pada_text_normalized)

    meter_spec = METER_SPECS.get(meter, {})

    # means there were special characters which indicates restorations:
    # see https://lrc.la.utexas.edu/books/rigveda/RV00#bolle
    has_restorations = len(pada_text_cleaned) != len(pada_text_normalized)

    caesura_possible_positions = meter_spec.get('caesura_possible_positions', [])

    parts = get_pada_parts(pada_text_cleaned)
    scansion = ""
    all_caesura_positions = []
    # 0 for invalid, -1 when not applicable (eg: for meters like anustubh and gayatri)
    caesura_position = 0 if caesura_possible_positions else -1
    no_of_syllables = 0
    syllables = []
    notes = ""

    for part in parts:
        # FIXME! add caesura marker if the syllable has the word boundary too?
        if is_word_boundary(part):
            scansion += WORD_BOUNDARY

            # mark the caesura if applicable
            if no_of_syllables in caesura_possible_positions:
                # we want to track both positions when they are possible
                all_caesura_positions.append(no_of_syllables)
                # FIXME decide win strategy on multiple caesura (first or last)
                # in case of eligible caesura on both positions, 4 wins for example, for tristubh
                # without this check, 5 would win (make sure not to put double mark in this case)
                if not caesura_position:
                    caesura_position = no_of_syllables
                    scansion += MARKER_CAESURA

            continue

        # add the cadence marker
        if no_of_syllables == meter_spec.get('cadence_position', -1):
            scansion += MARKER_CADENCE

        no_of_syllables += 1
        syllables.append(part)

        if WORD_BOUNDARY in part.strip():
            scansion += MARKER_WORD_BOUNDARY_IN_SYLLABLE

        if part == PAUSE:
            scansion += WORD_BOUNDARY + MARKER_PAUSE
        elif is_metrically_short(part):
            # FIXME handle o vowel as short before avagraha / a
            scansion += MARKER_SYLLABLE_SHORT
        else:
            scansion += MARKER_SYLLABLE_LONG

    scansion_syllables = clean_meter_scansion(scansion)
    # should never happen in our case but put this just for validation
    # TODO prefer to write these as asserts?
    #assert len(syllables) == len(scansion_syllables), f"Length of syllables {syllables} does not match that of the scansion '{scansion_syllables}'"
    if len(syllables) != len(scansion_syllables):
        raise Exception(f"Length of syllables {syllables} does not match the scansion {scansion_syllables}")

    # include info on other eligible caesura positions
    if len(all_caesura_positions) > 1:
        all_caesura_positions.remove(caesura_position)
        alt_caesura_position = ",".join([str(n) for n in all_caesura_positions])
    else:
        alt_caesura_position = ""
    if alt_caesura_position:
        notes += f"alt_caesura_position:{alt_caesura_position} "

    return {
        "parts": parts,
        "scansion": scansion,
        "no_of_syllables": no_of_syllables,
        "caesura_position": caesura_position,
        "has_restorations": has_restorations,
        "notes": notes,
        # simpler info
        "syllables": syllables,
        "scansion_syllables": scansion_syllables,
    }


def check_meter_faults(scansion, no_of_syllables, caesura_position, meter):
    if meter not in METER_SPECS:
        raise Exception(f"Unsupported meter: {meter}")

    faults = {}

    meter_spec = METER_SPECS[meter]

    # TODO we can just take last n chars as cadence too
    scansion_cadence_main = clean_meter_scansion(
        scansion.split(MARKER_CADENCE)[1]
    )[:-1] if MARKER_CADENCE in scansion else ""

    if no_of_syllables != meter_spec["no_of_syllables"]:
        faults["no_of_syllables"] = no_of_syllables
    elif scansion_cadence_main != meter_spec["scansion_cadence_main"]:
        faults["scansion_cadence"] = scansion_cadence_main + MARKER_SYLLABLE_SHORT_OR_LONG

    if caesura_position == 0: # for meters where caesura is unapplicable, this is -1
        faults["caesura_position"] = caesura_position
    elif caesura_position > 0 and "short_after_caesura_relative_position" in meter_spec:
        # TODO if alt_caesura_position is there, explore using it too
        scansion_post_caesura = clean_meter_scansion(
            scansion.split(MARKER_CAESURA)[1]
        )[:meter_spec["short_after_caesura_relative_position"]]
        if (
            len(scansion_post_caesura) != meter_spec['short_after_caesura_relative_position']
            or scansion_post_caesura[-1] != MARKER_SYLLABLE_SHORT
        ):
            faults['scansion_post_caesura'] = scansion_post_caesura

    return faults

###############################################################################

def analyze(pada_text, stanza_meter=""):
    results = generate_scansion(pada_text, stanza_meter)

    # if stanza meter is specified, check the correctness of the pada meter too
    results["is_correct"] = -1 # not applicable
    results["faults"] = ""
    if stanza_meter:
        faults = check_meter_faults(
            results["scansion"], results["no_of_syllables"], results["caesura_position"],
            stanza_meter
        )
        results["is_correct"] = 0 if faults else 1
        results['faults'] = " ".join([f"{k}={v}" for (k, v) in faults.items()])

    return results


# TODO take in arg here for custom analysis
if __name__ == '__main__':
    for pada in TEST_PADAS:
        # tests
        #print(" ".join(VOWELS))
        #print(" ".join(CONSONANTS))

        # input
        print(f'\n{pada["text"]} ({pada["stanza_meter"]})')

        # output
        analysis = analyze(pada["text"], pada["stanza_meter"])
        #print(analysis)
        print(f'{analysis["parts"]} {analysis["scansion"]} ({analysis["no_of_syllables"]}, {analysis["caesura_position"]})')
        #print(f'{analysis["syllables"]} {analysis["scansion_syllables"]} ({analysis["no_of_syllables"]})')

        # check meter correctness
        # TODO validate this too against the expected
        if analysis["faults"]:
            print("Faults:", analysis["faults"])

        # check output against expected
        # TODO save the test output in a file too?
        analysis_expected = pada["analysis"]
        #if analysis != analysis_expected:
        if (
            analysis["parts"] != analysis_expected["parts"]
            or analysis["scansion_syllables"] != clean_meter_scansion(analysis_expected["scansion"])
            or analysis["caesura_position"] != analysis_expected["caesura_position"]
        ):
            # TODO add no of syllables info?
            print(f'Not as expected: \n{analysis_expected["parts"]} {analysis_expected["scansion"]} (,{analysis_expected["caesura_position"]})\n')
