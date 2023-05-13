TEST_PADAS = [
    {
        "text": "agním īḷe puróhitaṁ",
        "stanza_meter": "Gāyatrī",
        "analysis": {
            "parts": ["ag", "ní", "m_ī", "ḷe", " ", "pu", "ró", "hi", "taṁ"],
            "scansion": "HS_HH | LHLH",
        }
    },
]


def analyze(pada_text, stanza_meter=""):
    #"Triṣṭubh"
    #"Aṇuṣṭubh"
    #"Gāyatrī"
    return {
        "parts": [],
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
        if analysis != analysis_expected:
            print(f'Not as expected: \n{analysis_expected["parts"]} {analysis_expected["scansion"]}\n')
