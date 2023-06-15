import re

# pip install more-itertools
from more_itertools import peekable, triplewise

TEST_PADAS = [
    # 1.1.1a
    {
        "pada_text": "agním īḷe puróhitaṁ",
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
        "pada_text": "yajñásya devám r̥tvíjam",
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
        "pada_text": "hótāraṁ  ratnadhā́tamam ",
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
        "pada_text": "sá íd devéṣu gachati",
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
        "pada_text": "víśve devā́so aptúraḥ",
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
        "pada_text": "ví tigména vr̥ṣabhéṇā púro 'bhet",
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
        "pada_text": "áditer dákṣo 'jāyata@",
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
        "pada_text": "sárvam ā́yuś ca te 'vidam",
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
        "pada_text": "prá-pra yajñám pr̥ṇītana",
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
        "pada_text": "śocíṣkeśo ̀ ní riṇāti vánā",
        "stanza_meter": "Triṣṭubh",
        "search_term": "riṇā",
        "analysis": {
            "parts": ["śo", "cíṣ", "ke", "śo", " \u0300", " ", "ní", " ", "ri", "ṇā", "ti", " ", "vá", "nā"],
            # LLLL · S SLS SL
            "scansion": "LLLL · ,S S|LS SL",
            "caesura_position": 5,
            "search_term_positions": [7, 8],
            "search_term_found": "riṇā",
        }
    },
    # 1.51.8a
    {
        "pada_text": "ví jānīhi ā́riyān yé ca dásyavo",
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
        "pada_text": "ráthaṁ híraṇyapra~ugaṁ váhantaḥ",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["rá", "thaṁ", " ", "hí", "raṇ", "yap", "ra", "~u", "gaṁ", " ", "vá", "han", "taḥ"],
            # SL SLLSSL SLL
            # FIXME no good way to mark caesura here since it's inside a compound
            #"scansion": "SL SLL,SS|L SLL",
            "scansion": "SL SLLSS|L SLL",
            #"caesura_position": 5,
            "caesura_position": 0,
        }
    },
    # 1.121.1a
    {
        "pada_text": "kád itthā́ nr̥ŕ̥m̐ḥ pā́taraṁ+ devayatā́ṁ",
        "stanza_meter": "",
        "analysis": {
            "parts": ["ká", "d it", "thā́", " ", "nr̥̄́m̐", "ḥ pā́", "ta", "raṁ", " ", "de", "va", "ya", "tā́ṁ"],
            # S LL L LSL LSSL
            "scansion": "S_LL L_LSL LSSL",
            "caesura_position": -1,
        }
    },
    # 10.129.5b
    {
        "pada_text": "adháḥ svid āsī́3d upári svid āsī3t",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["a", "dháḥ", " ", "svi", "d ā", "sī́3", "d u", "pá", "ri s", "vi", "d ā", "sī3t"],
            # SL S LL SSL S LL
            # TODO! _LS should be L_S
            "scansion": "SL S_LL,_SS|_LS_LL",
            "caesura_position": 5,
        }
    },
    # 10.144.4c
    {
        "pada_text": "śatácakraṁ yo\ 'hyo\ vartaníḥ",
        "stanza_meter": "",
        "analysis": {
            "parts": ["śa", "tá", "cak", "raṁ", " ", "yo\\ 'h", "yo\\", " ", "var", "ta", "níḥ"],
            # FIXME o before ' should be short? (avagraha)
            # TODO! _LL should be L_L?
            "scansion": "SSLL _LL LSL",
            "caesura_position": -1,
        }
    },
    # 10.166.2b
    {
        "pada_text": "índra 'vā́riṣṭo@ ákṣataḥ",
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
        "pada_text": "tuvā́ṁ hí agne sádam ít samanyávo",
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
        "pada_text": "tvā́ṁ hy àgne sádam ít samanyávo",
        "stanza_meter": "",
        "analysis": {
            "parts": ["tvā́ṁ", " ", "hy àg", "ne", " ", "sá", "da", "m ít", " ", "sa", "man", "yá", "vo"],
            # L LL SS L SLSL
            "scansion": "L _LL SS_L SLSL",
            "caesura_position": -1,
        }
    },
    # 1.48.4
    # r̥r̥ should be treated as r̥̄
    {
        "pada_text": "nā́ma gr̥ṇāti nr̥r̥ṇáam+",
        "stanza_meter": "",
        "analysis": {
            "parts": ["nā́", "ma", " ", "gr̥", "ṇā", "ti", " ", "nr̥̄", "ṇá", "am"],
            "scansion": "LS SLS LSL",
            "caesura_position": -1,
        }
    },
    # 1.42.5c (alt representation)
    # handling of r̥̄́ (has accent)
    {
        "pada_text": "yéna pitr̥̄́n ácodayaḥ",
        "stanza_meter": "",
        "analysis": {
            "parts": ["yé", "na", " ", "pi", "tr̥̄́", "n á", "co", "da", "yaḥ"],
            "scansion": "LS SL_SLSL",
            "caesura_position": -1,
        }
    },
    # 1.42.5c
    # r̥ŕ̥ should be treated as r̥̄́ (has accent)
    {
        "pada_text": "yéna pitr̥ŕ̥n ácodayaḥ",
        "stanza_meter": "",
        "analysis": {
            "parts": ["yé", "na", " ", "pi", "tr̥̄́", "n á", "co", "da", "yaḥ"],
            "scansion": "LS SL_SLSL",
            "caesura_position": -1,
        }
    },
    # 7.28.3b
    # ŕ̥r̥ should be treated as ŕ̥r̥ (has accent) (i.e. don't combine)
    # (represented as nr̥̃́n in the texas version):
    # https://lrc.la.utexas.edu/books/rigveda/RV07#H028
    # only other similar instance in 10.50.4c
    {
        "pada_text":  "sáṁ yán nŕ̥r̥n ná ródasī ninétha",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["sáṁ", " ", "yán", " ", "nŕ̥", "r̥n", " ", "ná", " ", "ró", "da", "sī",  " ", "ni", "né", "tha"],
            # multiple caesura positions eligible (first one wins)
            # FIXME decide win strategy on multiple caesura (first or last)
            # this is proof for win of late caesura? then only this follows meter
            #"scansion": "L L SL S ,LS|L SLS",
            #"caesura_position": 5,
            "scansion": "L L SL ,S LS|L SLS",
            "caesura_position": 4,
            # TODO! add this to all other test cases as applicable
            "fault_positions": [6],
        }
    },
    # 4.19.4c
    # ḷh should be treated as a single character (consonant)
    {
        "pada_text": "dr̥r̥ḷhā́ni+ aubhnād uśámāna ójo",
        "stanza_meter": "Triṣṭubh", # not tagged as such normally
        "analysis": {
            "parts": ["dr̥̄", "ḷhā́", "ni", " ", "aubh", "nā", "d u", "śá", "mā", "na", " ", "ó", "jo"],
            # SSLS LL SSLS LL (vedaweb treats ḷh as 2 chars yielding different results here)
            "scansion": "LLS LL,_SS|LS LL",
            "caesura_position": 5,
        }
    },
    # 10.157.2b
    # ḷ here is really the vowel l̥ (syllabic l): this is using IAST
    # which merges the consonant and the vowel. See:
    # https://en.wikipedia.org/wiki/International_Alphabet_of_Sanskrit_Transliteration#Comparison_with_ISO_15919
    # https://vedaweb.uni-koeln.de/rigveda/view/id/10.157.02
    {
        "pada_text": "ādityaír índraḥ sahá cīkḷpāti",
        "stanza_meter": "",
        "analysis": {
            # treating ḷ as consonant would yield the following which is incorrect
            #"parts": ["ā", "dit", "yaí", "r ín", "draḥ", " ", "sa", "há", " ", "cīk", "ḷpā", "ti"],
            #"scansion": "LLL_LL SS LLS",
            "parts": ["ā", "dit", "yaí", "r ín", "draḥ", " ", "sa", "há", " ", "cī", "kl̥", "pā", "ti"],
            "scansion": "LLL_LL SS LSLS",
            "caesura_position": -1,
        }
    },
    # faked
    {
        "pada_text": "hótāra  pratnadhā́tama avr̥̄",
        "stanza_meter": "",
        "analysis": {
            "parts": ["hó", "tā", "ra p", "rat", "na", "dhā́", "ta", "ma", " ", "a", "vr̥̄"],
            # TODO! _LL should be L_L
            "scansion": "LL_LLSLSS SL",
            "caesura_position": -1,
        }
    },
    # faked
    # multiple caesura positions eligible (first one wins)
    # FIXME decide win strategy on multiple caesura (first or last)
    {
        "pada_text": "śocíṣkeśo va ní riṇāti vánā",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["śo", "cíṣ", "ke", "śo", " ", "va", " ", "ní", " ", "ri", "ṇā", "ti", " ", "vá", "nā"],
            # LLLL S S SLS SL
            "scansion": "LLLL ,S S S|LS SL",
            # 4 wins over possible 5
            "caesura_position": 4,
        }
    },
    # 1.63.2
    # testing search term (without accent)
    {
        "pada_text": "púra iṣṇā́si puruhūta pūrvī́ḥ",
        "stanza_meter": "Triṣṭubh",
        "search_term": "iṣṇā",
        "analysis": {
            "parts": ['pú', 'ra', ' ', 'iṣ', 'ṇā́', 'si', ' ', 'pu', 'ru', 'hū', 'ta', ' ', 'pūr', 'vī́ḥ'],
            "scansion": "SS LLS ,SS|LS LL",
            "caesura_position": 5,
            "search_term_positions": [3, 4],
            "search_term_found": "iṣṇā",
        }
    },
    # 1.71.10
    # testing search term with stem variants
    {
        "pada_text": "nábho ná rūpáṁ jarimā́ mināti",
        "stanza_meter": "Triṣṭubh",
        "search_term": "minā mīnā",
        "analysis": {
            "parts": ['ná', 'bho', ' ', 'ná', ' ', 'rū', 'páṁ', ' ', 'ja', 'ri', 'mā́', ' ', 'mi', 'nā', 'ti'],
            "scansion": "SL S LL ,SS|L SLS",
            "caesura_position": 5,
            "search_term_positions": [9, 10],
            "search_term_found": "minā",
        }
    },
    # 10.87.14
    # testing search term with sandhi variant
    {
        "pada_text": "párārcíṣā mū́radevāñ chr̥ṇīhi",
        "stanza_meter": "",
        "search_term": "śr̥ṇī",
        "analysis": {
            "parts": ['pá', 'rār', 'cí', 'ṣā', ' ', 'mū́', 'ra', 'de', 'vāñ', ' ', 'cchr̥', 'ṇī', 'hi'],
            "scansion": "SLSL LSLL SLS",
            "caesura_position": -1,
            "search_term_positions": [9, 10],
            "search_term_found": "cchr̥ṇī",
        }
    },
    # 1.71.10
    # testing search term in the beginning
    {
        "pada_text": "nábho ná rūpáṁ jarimā́ mināti",
        "stanza_meter": "Triṣṭubh",
        "search_term": "nábh",
        "analysis": {
            "parts": ['ná', 'bho', ' ', 'ná', ' ', 'rū', 'páṁ', ' ', 'ja', 'ri', 'mā́', ' ', 'mi', 'nā', 'ti'],
            "scansion": "SL S LL ,SS|L SLS",
            "caesura_position": 5,
            "search_term_positions": [1, 2],
            "search_term_found": "nábh",
        }
    },
    # 7.97.2
    # meter fault in post-caesura position
    {
        "pada_text": "ā́ daíviyā vr̥ṇīmahe ávāṁsi",
        "stanza_meter": "Triṣṭubh",
        "search_term": "vr̥ṇī",
        "analysis": {
            "parts": ["ā́", " ", "daí", "vi", "yā", " ", "vr̥", "ṇī", "ma", "he", " ", "á", "vāṁ", "si"],
            "scansion": "L LSL ,SLS|L SLS",
            "caesura_position": 4,
            "fault_positions": [6],
            "search_term_positions": [5, 6],
            "search_term_fault_positions": [6],
        }
    },
    # 8.2.11
    # meter fault in cadence
    {
        "pada_text": "índremáṁ sómaṁ śrīṇīhi",
        "stanza_meter": "Gāyatrī",
        "search_term": "śrīṇī",
        "analysis": {
            "parts": ["ín", "dre", "máṁ", " ", "só", "maṁ", " ", "śrī", "ṇī", "hi"],
            "scansion": "LLL L|L LLS",
            "caesura_position": -1,
            "fault_positions": [5, 7],
            "search_term_positions": [6, 7],
            "search_term_fault_positions": [7],
        }
    },
]

#TEST_PADAS = [ TEST_PADAS[2] ]

###############################################################################

# Constants related to sanskrit chars used in our text

VOWELS_SHORT = [
    'a',
    'i', 'ï',
    'u', 'ü',
    'r̥',
    'l̥',
    # accented varieties
    'á', 'à',
    'í', 'ì',
    'ú', 'ù',
    'ŕ̥', 'r̥̀',
    # accented l̥ is not attested
    #
    # variants
    # instead of tracking these as separate characters, can choose to
    # normalize them, but using these make it more visible
    # TODO just implement this as part of normalize_sanskrit_chars()
    #
    # hiatus indication in ai/au: same as ï, ü
    '~i', '~u',
    # independent svarita: same as grave accented varieties above
    'a\\', 'i\\',
    'u\\', 'r̥\\', # these not present in vnh
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
    'r̥̄́', # grave version here is not attested
    'é', 'è', 'aí', 'aì',
    'ó', 'ò', 'aú', 'aù',
    #
    # variants
    # independent svarita: same as grave accented varieties above
    'ā\\', 'e\\', 'ai\\', 'o\\',
    'ī\\', 'ū\\', 'au\\' # these not present in vnh
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
    'ṁ', 'ḥ', 'm̐',
    'ḷ', 'ḷh',
]

WORD_BOUNDARY = ' '
AVAGRAHA = '\''
PAUSE = ' \u0300' # space followed by gravis, used in vnh text to mark metrical pauses

SPECIAL_CHARACTERS = [WORD_BOUNDARY, AVAGRAHA, PAUSE]

###############################################################################

# Constants related to meter

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
        "cadence_short_positions": [5, 7],
        "cadence_long_positions": [6],
        "scansion_cadence_main": PATTERN_IAMBIC, # positions 5,6,7
    },
    METER_ANUSTUBH: {
        "no_of_syllables": 8,
        "cadence_position": 4,
        "cadence_short_positions": [5, 7],
        "cadence_long_positions": [6],
        "scansion_cadence_main": PATTERN_IAMBIC, # positions 5,6,7
    },
    METER_TRISTUBH: {
        "no_of_syllables": 11,
        "cadence_position": 7,
        "cadence_short_positions": [9],
        "cadence_long_positions": [8, 10],
        "scansion_cadence_main": PATTERN_TROCHAIC, # positions 8,9,10
        "caesura_possible_positions": [4, 5],
        "short_after_caesura_relative_position": 2,
    },
    METER_JAGATI: {
        "no_of_syllables": 12,
        "cadence_position": 7,
        "cadence_short_positions": [9, 11],
        "cadence_long_positions": [8, 10],
        "scansion_cadence_main": PATTERN_TROCHAIC_IAMBIC, # positions 8,9,10,11
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
# '\' and '~' not included here since they mark variants in VOWELS
SPECIAL_CHARACTERS_SAMHITAPTHA_VNH = [
    '@', '+', # marks explicit restorations: https://lrc.la.utexas.edu/books/rigveda/RV00#bolle
    '&',      # marks modern editorial revisions: https://lrc.la.utexas.edu/books/rigveda/RV00#dagger
    '-',      # marks internal boundary of amredita (iterative) compounds
    '*',      # FIXME figure out what this means, eg: https://vedaweb.uni-koeln.de/rigveda/view/id/9.67.27
]

# TODO figure out meanings of each of these
# '\' not included here since they mark variants in VOWELS
SPECIAL_CHARACTERS_PADAPATHA_LUBOTSKY = ['-', '_', '=', '?', '+', '}', '!', '*']

###############################################################################

def clean_string(string, special_chars):
    return ''.join(c for c in string if c not in special_chars)

def clean_vnh_samhitapatha(string):
    return clean_string(string, SPECIAL_CHARACTERS_SAMHITAPTHA_VNH)

def clean_lubotsky_padapatha(string):
    return clean_string(string, SPECIAL_CHARACTERS_PADAPATHA_LUBOTSKY)

def clean_meter_scansion(string):
    return clean_string(string, SPECIAL_CHARACTERS_METER)

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

# TODO account for no of padas in the stanza too, for distinguishing
# between METER_GAYATRI and METER_ANUSTUBH. for our current analysis
# currently, not necessary since both the meters have 8 syllables
# def guess_meter(no_of_syllables):
#     meter_guessed = ""
#     for meter, meter_spec in METER_SPECS.items():
#         if no_of_syllables == meter_spec["no_of_syllables"]:
#             meter_guessed = meter
#             break
#     return meter_guessed

def stringify_dictionary(dict):
    return " ".join([f"{k}={v}" for (k, v) in dict.items()])

###############################################################################

# replace some of the conventions of the vnh text to our standards
# (for correct metrical analysis later)
# TODO revert these for the final syllables saved?
def normalize_sanskrit_chars(sanskrit_chars):
    chars_triplewise_iterator = triplewise(sanskrit_chars)

    chars_normalized = [sanskrit_chars[0]] # first char

    while (triple := next(chars_triplewise_iterator, ())): # all the middle chars
        c_prev, c, c_next = triple
        # CḷC: treat ḷ between consonants as a vowel character
        if c == 'ḷ' and is_sanskrit_consonant(c_prev) and is_sanskrit_consonant(c_next):
            c = 'l̥'
        # r̥r̥: long syllabic r
        elif c == 'r̥' and c_next == 'r̥':
            c = 'r̥̄'
            next(chars_triplewise_iterator) # skip next entry
        # r̥ŕ̥: long syllabic r (accented)
        # grave version not attested
        elif c == 'r̥' and c_next == 'ŕ̥':
            c = 'r̥̄́'
            next(chars_triplewise_iterator) # skip next entry
        # ŕ̥r̥: keep as separate chars (useful for the meter)
        # grave version not attested
        elif c == 'r̥' and c_prev == 'ŕ̥':
            pass
        # TODO include ch > cch logic here too? currently handled in get_sanskrit_chars()
        chars_normalized.append(c)

    if len(sanskrit_chars) > 1:
        chars_normalized.append(sanskrit_chars[-1]) # last char

    #print(chars_normalized)
    return chars_normalized


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
            # TODO move this to normalize_sanskrit_chars(), but better to keep here
            # since we handle avagraha too here?
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

    return normalize_sanskrit_chars(chars)


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


def normalize_sanskrit_text(text):
    # remove multiple spaces with single word boundary char
    text_normalized = re.sub(" +", WORD_BOUNDARY, text.strip())

    # this section commented out since we handle this in get_sanskrit_chars()
    # kept around in case we need it later
    #
    # replace some of the conventions of the vnh text to our standards
    # (for correct metrical analysis later)
    #
    # long syllabic r
    #text_normalized = text_normalized.replace('r̥r̥', 'r̥̄')
    #
    # long syllabic r (accented)
    # for 'ŕ̥r̥', we want to treat it as separate chars (for the meter)
    # also, grave version of these is not attested
    #text_normalized = text_normalized.replace('r̥ŕ̥', 'r̥̄́')

    return text_normalized


def generate_scansion(pada_text, meter=""):
    # normalize and clean special characters in the text
    pada_text_normalized = normalize_sanskrit_text(pada_text)
    pada_text_cleaned = clean_vnh_samhitapatha(pada_text_normalized)

    meter_spec = METER_SPECS.get(meter, {})

    # means there were special characters which indicates restorations:
    # see https://lrc.la.utexas.edu/books/rigveda/RV00#bolle
    # alt method:
    #has_restorations = len(pada_text_cleaned) != len(pada_text_normalized)
    has_restorations = any([c in pada_text_normalized for c in SPECIAL_CHARACTERS_SAMHITAPTHA_VNH])

    caesura_possible_positions = meter_spec.get('caesura_possible_positions', [])

    parts = get_pada_parts(pada_text_cleaned)
    scansion = ""
    all_caesura_positions = []
    # 0 for invalid, -1 when not applicable (eg: for meters like anustubh and gayatri)
    caesura_position = 0 if caesura_possible_positions else -1
    no_of_syllables = 0
    syllables = []
    notes = {}

    for part in parts:
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

        # word boundary in the middle of the syllable part
        # TODO! change where this marker goes based on whether the part before the
        # word boundary here is vowel or not?
        if WORD_BOUNDARY in part.strip(WORD_BOUNDARY):
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

    # if caesura position has still not been set, be less strict i.e.
    # if syllables in possible caesura positions have word boundary internally, count it
    if not caesura_position:
        all_caesura_positions = [
            n for n in caesura_possible_positions
                # word boundary in the middle of the syllable
                # no need to substract 1 from n here!
                # since we actually need to check the syllable after the possible position
                # (the part before the space in the next syllable would be actually before caesura)
                if WORD_BOUNDARY in syllables[n].strip(WORD_BOUNDARY)
        ]
        if all_caesura_positions:
            # FIXME decide win strategy on multiple caesura (first or last)
            caesura_position = all_caesura_positions[0] # first one wins
            notes['caesura_position_inside_syllable'] = True
            # insert the caesura marker at the appropriate place in the scansion string
            # TODO do this more cleanly above, by storing each scansion element in a more
            # structured fashion
            temp_scansion = ''
            temp_no_of_syllables = 0
            for c in scansion:
                temp_scansion += c
                if c in [MARKER_SYLLABLE_SHORT, MARKER_SYLLABLE_LONG, MARKER_PAUSE]:
                    temp_no_of_syllables +=1
                    if temp_no_of_syllables == caesura_position:
                        temp_scansion += MARKER_CAESURA
            scansion = temp_scansion

    # include info on other eligible caesura positions
    if len(all_caesura_positions) > 1:
        all_caesura_positions.remove(caesura_position)
        alt_caesura_position = ",".join([str(n) for n in all_caesura_positions])
    else:
        alt_caesura_position = ""
    if alt_caesura_position:
        notes['caesura_position_alt'] = alt_caesura_position

    return {
        "parts": parts,
        "scansion": scansion,
        "no_of_syllables": no_of_syllables,
        "caesura_position": caesura_position,
        "has_restorations": has_restorations,
        "notes": stringify_dictionary(notes),
        # simpler info
        "text_normalized": "".join(parts),
        "syllables": syllables,
        "scansion_syllables": scansion_syllables,
    }


def check_meter_faults(scansion, no_of_syllables, caesura_position, meter):
    if meter not in METER_SPECS:
        raise Exception(f"Unsupported meter: {meter}")

    faults = {}
    positions = []

    meter_spec = METER_SPECS[meter]

    # TODO we can just take last n chars as cadence too
    scansion_cadence_main = clean_meter_scansion(
        scansion.split(MARKER_CADENCE)[1]
    )[:-1] if MARKER_CADENCE in scansion else ""

    if no_of_syllables != meter_spec["no_of_syllables"]:
        faults["no_of_syllables"] = no_of_syllables
    elif scansion_cadence_main != meter_spec["scansion_cadence_main"]:
        # this should not really happen since we set cadence marker following the
        # meter spec and we already checked above that the syllable counts match
        # but just in case
        if len(scansion_cadence_main) != len(meter_spec["scansion_cadence_main"]):
            raise Exception(
                f"Length of main scansion cadence {scansion_cadence_main} does not match"
                + f" that of the expected: {meter_spec['scansion_cadence_main']}"
            )
        faults["scansion_cadence"] = scansion_cadence_main + MARKER_SYLLABLE_SHORT_OR_LONG
        # track the faulty position(s)
        for i, c in enumerate(meter_spec["scansion_cadence_main"]):
            if c != scansion_cadence_main[i]: # safe to do since the lengths match by this point
                positions.append(no_of_syllables - len(scansion_cadence_main) + i)

    if caesura_position == 0: # for meters where caesura is unapplicable, this is -1
        faults["caesura_position"] = caesura_position
    elif caesura_position > 0 and "short_after_caesura_relative_position" in meter_spec:
        # TODO if alt_caesura_position is there, explore using it too?
        scansion_post_caesura = clean_meter_scansion(
            scansion.split(MARKER_CAESURA)[1]
        )[:meter_spec["short_after_caesura_relative_position"]]
        if (
            len(scansion_post_caesura) != meter_spec['short_after_caesura_relative_position']
            or scansion_post_caesura[-1] != MARKER_SYLLABLE_SHORT
        ):
            # TODO just use name break here?
            faults['scansion_post_caesura'] = scansion_post_caesura
            # track the faulty position
            positions.append(
                caesura_position + meter_spec['short_after_caesura_relative_position']
            )

    return {
        "faults": faults,
        "positions": sorted(positions),
    }


# populated manually right now based on the sandhi/variant forms we see in our data
ALTERNATE_FORMS = {
    # sandhi variants
    "aśnā": "āśnā",   #-a a- > -ā-
    "śr̥ṇī": "cchr̥ṇī", #-n ś- > -ñch-
    # stem variants (root vowel shortened)
    "prīṇā": "priṇā",
    "prīṇī": "priṇī",
    "śrīṇī": "śriṇī",
}
def get_alt_form(term):
    return ALTERNATE_FORMS.get(term, "")


def find_syllable_positions(search_term, pada_text, pada_syllables):
    positions = []
    term_found = ""

    found_terms = []
    for variant in search_term.strip().split(" "):
        variant_alt = get_alt_form(variant)
        if variant in pada_text:
            found_terms.append(variant)
        if variant_alt and variant_alt in pada_text:
            found_terms.append(variant_alt)

    if len(found_terms) == 0:
        # should not occur for our data: if it does, might mean we have not covered
        # a possible variant of the search term yet
        raise Exception (
            f"Search term '{search_term}' not found in the pada_text '{pada_text}'"
        )
    elif len(found_terms) > 1:
        # we don't need to handle multiple variant matches in a single pada currently
        # since it doesn't happen for our data, but in case this occurs, this exception
        # will let us know
        raise Exception(
            f"More than one variant of the search term '{search_term}' found in the pada_text '{pada_text}'"
        )
    elif len(found_terms) == 1:
        term_found = found_terms[0]

        # get the syllable positions for the term
        start_position, end_position = 0, 0
        tracker = ""
        for i, syllable in enumerate(pada_syllables):
            tracker += syllable
            if term_found in tracker:
                end_position = i + 1
                break
        if end_position:
            tracker = ""
            for i, syllable in enumerate(reversed(pada_syllables[:end_position])):
                tracker = syllable + tracker
                if term_found in tracker:
                    start_position = end_position - i
                    break
        if start_position and end_position:
            # adding +1 to the end position for it to be inclusive in the range
            positions = list(range(start_position, end_position+1))
        else:
            # this shouldn't happen really, but just in case
            raise Exception (
                f"Search term '{search_term}' was found in the pada_text '{pada_text}'"
                + " but couldn't determine its syllable positions"
            )

    return {
        "positions": positions,
        "term_found": term_found,
    }

###############################################################################

def get_expected_scansion(position, meter, caesura_position=-1):
    if meter not in METER_SPECS:
        return ''

    meter_spec = METER_SPECS[meter]

    if position < 1 or position > meter_spec["no_of_syllables"]:
        raise Exception(f"Invalid position specified for meter {meter}: {position}")

    #if meter in [METER_TRISTUBH, METER_JAGATI] and not caesura_position > 0:
    #    raise Exception(f"Caesura position must be set for meter: {meter}")

    # copying since we will update the short positions. important since python
    # is pass-by-assignment (without copy, we would be modifying short_positions
    # on every call to the function, needing to nasty bugs)
    # TODO! check if we need to use copy() elsewhere too
    short_positions = meter_spec["cadence_short_positions"].copy()
    if caesura_position > 0:
        short_positions.append(
            caesura_position + meter_spec["short_after_caesura_relative_position"]
        )

    # copy not really needed here since we don't change it right now
    # but done for consistency with short_positions
    long_positions = meter_spec["cadence_long_positions"].copy()

    if position in short_positions:
        return MARKER_SYLLABLE_SHORT
    elif position in long_positions:
        return MARKER_SYLLABLE_LONG
    else:
        return MARKER_SYLLABLE_SHORT_OR_LONG


# can specify variant in the search_term with space
def analyze(pada_text, stanza_meter="", search_term=""):
    results = generate_scansion(pada_text, stanza_meter)

    # if stanza meter is specified, check the correctness of the pada meter too
    results["is_correct"] = -1 # not applicable
    results["faults"] = ""
    results["fault_positions"] = []
    # disabling the guess of stanza meter, does not alter our core result (count of nA/nI in
    # expected short syllables) even with a very permissive guess so no point in pursuing
    # this avenue right now, since we need to be careful with the guess assignment anyways.
    # if not stanza_meter:
    #     # try to guess the meter if it's not set
    #     stanza_meter = guess_meter(results["no_of_syllables"])
    #     if stanza_meter:
    #         # redo the scansion based on the new knowledge
    #         # TODO eliminate this extra call by moving guess_meter inside generate_scansion
    #         # itself (but need to modify it a bit first to allow for caesura/cadence markers)
    #         results = generate_scansion(pada_text, stanza_meter)
    #         results["stanza_meter_guessed"] = stanza_meter
    #         results["notes"] += f" meter_guessed={stanza_meter}"
    #         print(results["notes"])
    if stanza_meter:
        faults = check_meter_faults(
            results["scansion"], results["no_of_syllables"], results["caesura_position"],
            stanza_meter
        )
        # TODO just use strings for meter_is_correct?
        results["is_correct"] = 0 if faults["faults"] else 1
        results["faults"] = stringify_dictionary(faults["faults"])
        results["fault_positions"] = faults["positions"]

    if search_term:
        positions = find_syllable_positions(
            search_term,
            results["text_normalized"], results["syllables"]
        )
        results["search_term_positions"] = positions["positions"]
        results["search_term_found"] = positions["term_found"]

        # if we have positions where meter is faulty, check if
        # search term positions have overlap with it
        results["search_term_fault_positions"] = [
            n for n in results["search_term_positions"] if n in results["fault_positions"]
        ] if results.get("fault_positions", []) else []

    return results


COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'
def test_analysis(pada):
    success = True

    analysis_expected = pada.pop("analysis")
    analysis = analyze(**pada)

    print(" | ".join(pada.values()))

    for k, v_expected in analysis_expected.items():
        v_output = analysis[k]
        message = f"{k}: {v_output}"
        if v_output != v_expected:
            message += f"{COLOR_FAIL} ≠ {v_expected}{COLOR_END}"
            success = False
        print(message)

    # TODO include syllable count too?
    if analysis["faults"]:
        print("Faults:", analysis["faults"])

    print("")

    return success


# TODO take in arg here for custom analysis
# TODO move the tests to its own file
if __name__ == '__main__':
    results = [test_analysis(pada) for pada in TEST_PADAS]

    print(f"Ran {len(results)} test cases, {results.count(False)} failure(s)")

    # print(
    #     get_expected_scansion(6, "Triṣṭubh", 4),
    #     get_expected_scansion(6, "Triṣṭubh", 5),
    #     get_expected_scansion(7, "Triṣṭubh", 4)
    # )
