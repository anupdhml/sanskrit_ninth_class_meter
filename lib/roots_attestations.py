import json
import requests
import time

# from ./roots.py
from lib.roots import NINTH_CLASS, FIFTH_CLASS

from bs4 import BeautifulSoup
from pprint import pprint

VEDAWEB_API_URL = "https://vedaweb.uni-koeln.de/rigveda/api"

def parse_vedaweb_search_highlight_text(text):
    word_instances = []

    for instance_text in BeautifulSoup(text, "lxml").text.split('/'):
        word_gloss = {}
        for prop in instance_text.split(';'):
            prop_parts = prop.split(':')
            prop_name = prop_parts[0].strip()
            prop_value = prop_parts[1].strip()

            #if prop_name in ["lemma", "lemma type"]:
            #    continue

            word_gloss[prop_name] = prop_value

        word_instances.append(word_gloss)

    return word_instances

def search_verb_form_attestations_vedaweb_helper(stem, root=None, results_no=10, results_from=0):
    search_block = {
        "lemma type": "root",
        # make sure we get verbal forms only
        # (i.e. ignore nominal forms like participles which are not marked for person)
        "person": "*", # is present
        "required": True,
        "distance": 0
    }

    # handle stems that have spaces to mark variants too!
    # when multiple terms are present separated via space, vedaweb interprets it as an
    # "or" search which is convenient for us
    # TODO break down the search for each variant so that we can track results for each
    # separately? not needed at this stage though
    stem_variants = [ '*' + stem_variant + '*' for stem_variant in stem.split(" ")]
    search_block["term"] = ' '.join(stem_variants)
    #print(search_block["term"])

    # if root is specified, pass it in too (useful to disambiguate certain forms from others)
    if root:
        search_block["lemma"] = root
        #print(search_block["lemma"])

    response = requests.post(
        VEDAWEB_API_URL + "/search/grammar",
        headers = {"Content-Type": "application/json"},
        json = {
            "mode": "grammar",
            "accents": False,
            "blocks": [search_block],
            "scopes": [],
            "meta": {
                #"hymnAddressee": [],
                #"hymnGroup": [],
                #"strata": [],
                #"stanzaType": [],
                #"lateAdditions": []
            },
            "size": results_no,
            "from": results_from
        }
    )

    # raises an exception on non-200 responses, since we want to know and act on it
    response.raise_for_status()

    #pprint(response.request.body)
    #pprint(response.json()["hits"][0])

    response_json = response.json()

    results = {}
    found_lemmas = set()
    for hit in response_json["hits"]:
        stanza_no = hit["docId"]

        words = []
        for word, highlight_text in hit["highlight"].items():
            word_instances = parse_vedaweb_search_highlight_text(highlight_text)
            for word_gloss in word_instances:
                lemma = word_gloss.pop("lemma")
                #lemma = word_gloss.get("lemma")
                # we don't need this since everything is root for us
                word_gloss.pop("lemma type")
                words.append({
                    "word": word,
                    "gloss": word_gloss
                })
                found_lemmas.add(lemma)

        if stanza_no in results:
            # shouldn't happen in our case at all, but just in case
            raise Exception(f"Unexpected, duplicate stanza number found: {stanza_no}")
        else:
            results[stanza_no] = words

    # safeguard while testing
    time.sleep(1)
    return {
        "lemmas": list(found_lemmas),
        "count": len(results),
        "total": response_json["total"],
        "results": results
    }

# TODO remove since we don't use this anymore
ROOT_VARIANT_SUFFIXES = [
    # try with different order, see if we get different results?
    # also need to try all of them?
    # marker of seṭ roots (goes back to PIE roots ending in laryngeals)
    #"ⁱ",
    # numbers used to mark roots of same phonetic shape but different semantics
    #" 1", " 2",
    # try this next
    #" 3",
    # up to 3 really should be enough but just in case
    # try with just these for roots where we don't get any hits
    #" 4", " 5",
    # last resort: matches anything that follows
    # needed to catch cases like vr̥ ~ vr̥̄ in vedaweb
    # kind of safe because we also limit our searches by stem where we specify
    # the suffix directly following the root, but to limit false positives,
    # we put this last and specify predicatable variants above
    "*"
]

def search_verb_form_attestations_vedaweb(stem, root=None, results_no=10, results_from=0):
    results = search_verb_form_attestations_vedaweb_helper(stem, root, results_no)

#     if results["count"] == 0:
#         for root_variant_suffix in ROOT_VARIANT_SUFFIXES:
#             # our initial root data comes from whitney but how it's represented in vedaweb
#             # may be different so gotta try with other variant forms
#             root_variant = root + root_variant_suffix
#             # useful while debugging
#             #print(
#             #    f"No results found for root:{root} stem:{stem}.",
#             #    f"Retrying with root variant: {root_variant}"
#             #)
#             results = search_verb_form_attestations_vedaweb_helper(stem, root_variant, results_no)

#             # we found a match for a working suffix so stop now
#             if results["count"] > 0:
#                 break


    # FIXME implement getting all results
    # not needed right now since we get all results at once
    all_results = results["results"]
    all_results_count = len(all_results)

    if len(results["lemmas"]) > 1:
        raise Exception(
            f"Unexpected, multiple roots found while searching for {stem}: {results['lemmas']}"
        )

    return {
        "root_vedaweb": results["lemmas"][0] if (all_results_count > 0) else None,
        "count": all_results_count,
        "total": results["total"],
        "results": all_results
    }


def check_for_dup_roots(roots, present_class):
    temp = set()
    dup_roots = [root["root"] for root in roots if (
        root["present_class"] == present_class and
        (root["root"] in temp or temp.add(root["root"]))
    )]
    if len(dup_roots) > 0:
        # means some other roots also resolved to these during our search
        # we need to ensure our code handles these too now
        raise Exception(f"Final list of {present_class} class roots contain duplicates: {dup_roots}")

###############################################################################

def get_attestations(whitney_roots):
    roots = []

    roots_attested_words_by_stanza = {
        NINTH_CLASS: {},
        FIFTH_CLASS: {},
    }

    for root in whitney_roots:
        #if root["present_class"] == NINTH_CLASS:
        #if root["present_class"] == FIFTH_CLASS":
        #    continue

        #if root["root_guess"] not in ["kr̥"]:
        #if root["root_guess"] not in ["ci", "ci 1"]:
        #if root["root_guess"] not in ["mi", "mi 1"]:
        #if root["root_guess"] not in ["pr̥", "pr̥ 1"]:
        #if root["root_guess"] not in ["vr̥ ūr", "vr̥ vr̥̄", "vr̥"]:
        #   continue

        # TODO remove this test filter
        #if root["root_guess"] not in ["iṣ 1", "pū", "vr̥~ vr̥̄"]:
        #
        #if root["root_guess"] not in ["śr̥", "dr̥", "pr̥"]:
        #if root["root_guess"] not in ["i", "uṣ", "mi mī", "muṣ"]:
        #if root["root_guess"] not in ["uṣ", "muṣ"]:
        #if root["root_guess"] not in ["vr̥ vr̥̄", "vr̥", "śrī", "śrī 2", "aśⁱ", "aś", "gr̥̄ 1", "gr̥"]:
        #if root["root_guess"] not in ["pū", "gr̥bh", "iṣ"]:
        # if root["root_guess"] not in ["pū"]:
        #     root["root"] = root["root_guess"]
        #     root["strong_attestations"] = ''
        #     root["weak_attestations"] = ''
        #     roots.append(root)
        #     continue

        # test cases
        #results = search_verb_form_attestations_vedaweb("iṣṇā", "iṣ 1", 10)
        #results = search_verb_form_attestations_vedaweb("pun", "pū", 10)

        # for certain roots, actually pass in the root to disambiguate its forms from others
        # FIXME find a better place for these overrides
        root_for_disambiguating = None
        if root["present_class"] == NINTH_CLASS and root["root_guess"] in [
            # FIXME auto-figure out by subset (if the stem is a subset already pass root to disambiguate)
            "i", "uṣ", # to dismabiguate from *mi* and *muṣ*
            "vr̥ vr̥̄", "vr̥", "aśⁱ", "aś", "gr̥̄ 1", "gr̥",
            "śrī", "śrī 2", # FIXME vedaweb does not actually have the second variant at all
        ]:
            root_for_disambiguating = root["root_guess"]
        elif root["present_class"] == FIFTH_CLASS and root["root_guess"] in [
            "ci 1", "ci", "mi 1", "mi",
            "vr̥ vr̥̄", # for "vr̥ ūr" we don't pass the root_guess and based on the stem it resolves to vr̥
            "pr̥ 1", "pr̥", # to dismabiguate from *spr̥* too
            "i", "u", "r̥",
        ]:
            root_for_disambiguating = root["root_guess"]

        # TODO add exception if the no of total matches is greater than 150
        # for our data, no of attestations per stem does not exceed 150 so it's safe
        # to not do it right now
        results_strong = search_verb_form_attestations_vedaweb(
            root["strong_stem"], root_for_disambiguating, 150
        )
        results_weak = search_verb_form_attestations_vedaweb(
            root["weak_stem"], root_for_disambiguating, 150
        )

        #pprint(results_strong["09.067.27"])
        #pprint(results_strong)
        #pprint(results_weak)

        # unlikely to happen but still test for this
        if (results_strong["root_vedaweb"] and results_weak["root_vedaweb"] and
                results_strong["root_vedaweb"] != results_weak["root_vedaweb"]
            ):
            raise Exception(
                f"Root '{results_strong['root_vedaweb']}' inferred from strong-stem results " +
                f"does not match root '{results_weak['root_vedaweb']}' from weak-stem results"
            )
        # both strong and weak results are the same (or one of them is None) by this point
        # so can generalize in either order here
        results_root_vedaweb = results_weak["root_vedaweb"] or results_strong["root_vedaweb"]

        if results_root_vedaweb and root["root_guess"] != results_root_vedaweb:
            # FIXME add notes colummn?: root form originally present as ""
            print(
                f"note: using '{results_root_vedaweb}' for root guess {root['root_guess']}",
                "(as done in vedaweb)"
            )
            # FIXME handle this better without losing the order of the column?
            root["root"] = results_root_vedaweb
            #root["root_variant_vedaweb"] = results_root_vedaweb
        else:
            #root["root_variant_vedaweb"] = ''
            root["root"] = root["root_guess"]

        root["strong_attestations"] = " ".join(list(results_strong["results"].keys()))
        root["strong_attestations_total"] = results_strong['total']

        root["weak_attestations"] = " ".join(list(results_weak["results"].keys()))
        root["weak_attestations_total"] = results_weak['total']

        #root["strong_attestations_data"] = results_strong
        #root["weak_attestations_data"] = results_weak

        roots.append(root)

        # save full results data, for use later
        roots_attested_words_by_stanza[root["present_class"]][root["root"]] = {
            "strong": results_strong["results"],
            "weak": results_weak["results"]
        }

        # useful diagnostic message
        print(
            # print the variant root form found in vedaweb, if it's there
            #f"{' (' + root['root_variant_vedaweb'] + ')' if root['root_variant_vedaweb'] else ''}",
            f"[{root['present_class']}] {root['root']}: {results_strong['total']} strong, {results_weak['total']} weak attestations"
        )

        # so that we don't hammer the api
        #time.sleep(0.5)

    check_for_dup_roots(roots, NINTH_CLASS)
    check_for_dup_roots(roots, FIFTH_CLASS)
    #pprint(roots)

    return (roots, roots_attested_words_by_stanza)
