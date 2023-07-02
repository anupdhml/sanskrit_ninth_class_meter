import lib.meter as meter

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
    # metrical pauses (after vowel)
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
    # 1.174.9.b
    # metrical pauses (after consonant)
    {
        "pada_text": "r̥ṇór apáḥ ̀ sīrā́ ná srávantīḥ",
        "stanza_meter": "Triṣṭubh",
        "analysis": {
            "parts": ["r̥", "ṇó", "r a", "páḥ", " \u0300", " ", "sī", "rā́", " ", "ná s", "rá", "van", "tīḥ"],
            # SL SL · LL L SLL
            "scansion": "SL_SL · ,LL |_LSLL",
            "caesura_position": 5,
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
            "fault_positions": [5, 7], # with iambic cadence
            "search_term_positions": [6, 7],
            "search_term_fault_positions": [7], # stem vowel
        }
    },
    # 8.2.11
    # potential trochaic gayatri pada
    {
        "pada_text": "índremáṁ sómaṁ śrīṇīhi",
        "stanza_meter": "Gāyatrī (Trochaic)",
        "search_term": "śrīṇī",
        "analysis": {
            "parts": ["ín", "dre", "máṁ", " ", "só", "maṁ", " ", "śrī", "ṇī", "hi"],
            "scansion": "LLL L|L LLS",
            "caesura_position": -1,
            "fault_positions": [6], # with trochaic cadence
            "search_term_positions": [6, 7],
            "search_term_fault_positions": [6], # root vowel
        }
    },
]

#TEST_PADAS = [ TEST_PADAS[-1] ]

###############################################################################

COLOR_FAIL = '\033[91m'
COLOR_END = '\033[0m'

def test_analysis(pada):
    success = True

    analysis_expected = pada.pop("analysis")
    analysis = meter.analyze(**pada)

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
if __name__ == '__main__':
    results = [test_analysis(pada) for pada in TEST_PADAS]

    print(f"Ran {len(results)} test cases, {results.count(False)} failure(s)")

    # print(
    #     meter.get_expected_scansion(6, "Triṣṭubh", 4),
    #     meter.get_expected_scansion(6, "Triṣṭubh", 5),
    #     meter.get_expected_scansion(7, "Triṣṭubh", 4)
    # )
