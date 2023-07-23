import json

def pada_char_to_no(char):
    # TODO turn this into a dict
    match char:
        case 'a':
            return 0
        case 'b':
            return 1
        case 'c':
            return 2
        case 'd':
            return 3
        case 'e':
            return 4
        case 'f':
            return 5
        case 'g':
            return 6
        case _:
            raise Exception(f"Invalid pada char: {char}")


def get_stanza_words(stanza_padas):
    stanza_words = {}

    for pada_data in stanza_padas:
        for word_grammar_data in pada_data["grammarData"]:
            word = word_grammar_data["form"]

            word_grammar_data_props = word_grammar_data["props"]
            word_position = word_grammar_data_props.pop("position", '')
            word_lemma_type = word_grammar_data_props.pop("lemma type", '')

            word_data = {
                # tracker for when we later search for the actual attested words
                "found": False,
                "data": {
                    "pada_id": pada_data["id"],
                    # TODO test with this and later eliminate
                    #"pada_index": pada_data["index"],
                    "pada_label": pada_data["label"],
                    "word": word,
                    "word_position_no": word_grammar_data["index"], # not-zero-indexed!
                    # TODO be careful of this, does not seem to be accurate
                    # (eg: for "punīhi" for 9.67.24 )
                    # TODO use these for checks
                    "word_position": word_position,
                    "word_lemma_type": word_lemma_type,
                    # FIXME pass this and use to validate further
                    #"word_lemma": word_grammar_data["lemma"]
                    "word_props": word_grammar_data_props,
                    # TODO this not needed since all of it is contained in props
                    # but pass and validate they are the same...
                    #"word_gloss": word_tracker_gloss
                }
            }

            if word in stanza_words:
                stanza_words[word].append(word_data)
            else:
                # need to use a list since the word may appear multiple times in the stanza
                stanza_words[word] = [word_data]

    return stanza_words


def get_words_by_pada(stanza_attested_words, stanza_padas, stanza_no=None):
    words_by_pada = []

    #pprint(stanza_attested_words)
    #pprint(stanza_padas)

    # transform data in stanza_padas to be amenable for searching the attested words
    stanza_words = get_stanza_words(stanza_padas)
    #pprint(stanza_words)

    for attested_word_data in stanza_attested_words:
        attested_word = attested_word_data["word"]
        attested_word_gloss = attested_word_data["gloss"]

        if attested_word in stanza_words:
            for word_instance in stanza_words[attested_word]:
                # if this word instance was already found, skip to the next one
                if word_instance["found"]:
                    continue

                word_instance_data = word_instance["data"]
                word_instance_lemma_type = word_instance_data.pop("word_lemma_type")

                # FIXME check for lemma too?
                # TODO also ensure this is not causing us to drop valid lines
                if (word_instance_lemma_type and word_instance_lemma_type != "root"):
                    print(
                        f"Skipping an instance of attested word {attested_word} because its lemma type",
                        f"'{word_instance_lemma_type}' is not root"
                    )
                    continue

                if (word_instance_data["word_position"] and
                        "position" in attested_word_gloss and
                        # python "and" operator is short-circuiting so can access "position" below
                        # TODO can we trust this?
                        word_instance_data["word_position"] != attested_word_gloss["position"]
                    ):
                    # even if we skip for a valid instance we will come back to it with a valid position later
                    print(
                        f"Skipping an instance of attested word {attested_word} because it's position '{word_instance_data['word_position']}'",
                        f"does not match the actual attested position '{attested_word_gloss['position']}'"
                    )
                    continue

                # TODO not needed since all of this info is already in word_instance_data
                #word_instance_data["gloss"] = attested_word_gloss
                words_by_pada.append(word_instance_data)

                # no need to do this in-place for python!
                word_instance["found"] = True
                break
        else:
            # TODO handle this better? ok to let go maybe
            raise Exception(
                f"Word {attested_word} was not found in the stanza {stanza_no}: {stanza_padas}"
            )

    # something went wrong and we need to investigate
    if len(words_by_pada) != len(stanza_attested_words):
        raise Exception("No of word instances by pada does not match the input no of word instances attested in the stanza")

    return words_by_pada


def is_stem_present(stem, text):
    is_present = stem in text

    # account for accent variation for fifth class strong and weak stems (-no-/-nu-)
    # don't need to do similar for ninth because its strong stem (-nā́/-nī́-) is already composed of 2 chars
    if not is_present:
        if stem[-1] == "o":
            stem_with_accent = stem[:-1] + "ó"
        elif stem[-1] == "u":
            stem_with_accent = stem[:-1] + "ú"
        else:
            stem_with_accent = stem

        is_present = stem_with_accent in text

    return is_present


def annotate_line(line, roots_with_attested_words):
    with open(f"downloads/vedaweb/{line['stanza']}.json") as f:
        stanza = json.load(f)

        # TODO get pada no for each line (could be multiple) using data in:
        # roots_with_attested_words
        # we will be ultimately returning multiple lines here sometimes
        #if line["pada"]:
        #    pada_no = pada_char_to_no(line["pada"][-1])
        #    #pada_no = pada_char_to_no(line["pada_id"])
        #else:

        #pada_no = 0

        stanza_attested_words = roots_with_attested_words[line["present_class"]][line["root"]][line["stem_type"]][line["stanza"]]

        words_by_pada = get_words_by_pada(stanza_attested_words, stanza["padas"], line["stanza"])
        #pprint(words_by_pada)

        padas = []

        for word in words_by_pada:
            pada = line | word

            # TODO rename line_no to location everywhere
            pada["line_no"] = pada["stanza"] + "." + pada["pada_id"]
            # this is not needed now
            pada.pop("pada")
            #pada["pada"] = pada["stanza"] + "." + pada["pada_id"]

            # FIXME add each of these as a separate field too
            word_props = pada.pop("word_props")
            pada["word_gloss"] = f"{word_props['person']}.{word_props['number']}" + \
                f".{word_props['tense']}.{word_props['mood']}.{word_props['voice']}"

            # TODO try out getting index from stanza info directly and see if we still
            # get the same results
            pada_no = pada_char_to_no(pada["pada_id"])
            # TODO testing remove
            #pada_no = 0

            for version in stanza["versions"]:
                if version["id"] == "version_lubotsky":
                    pada["text_padapatha"] = version["form"][pada_no]
                    break

            for version in stanza["versions"]:
                if version["id"] == "version_vannootenholland":
                    # need to override pada no for the vnh version here, since it does
                    # not match the padapatha:
                    # https://vedaweb.uni-koeln.de/rigveda/view/id/08.039.06
                    if pada["line_no"] == "08.039.06.e" and pada["stem"] == "vr̥ṇu ūrṇu":
                        # FIXME update line_no also here?
                        pada_no = pada_char_to_no("d")
                    # TODO deal with * at the begining of the text here?
                    pada["text_samhitapatha"] = version["form"][pada_no]
                    pada["meter_scansion"] = version["metricalData"][pada_no]
                    break

            pada["stanza_meter"] = stanza["stanzaType"] or ''

            # historical info
            # TODO get these info from hellewig too?
            # normalize smallcase strata values
            pada["stanza_strata"] = stanza["strata"].upper()
            # if false, based on both meter and linguistic evidence
            pada["stanza_strata_based_on_meter_only"] = stanza["strata"].islower()
            pada["stanza_late_addition"] = stanza["lateAdditions"] or ''

            # hymn extra metadata (maybe handy)
            pada["hymn_absolute_no"] = stanza["hymnAbs"]
            pada["hymn_addressee"] = stanza["hymnAddressee"]
            pada["hymn_group"] = stanza["hymnGroup"]

            # this shouldn't really happen since the results we got were done
            # via stem searches on the padapatha but validate, just in case
            if not any([
                is_stem_present(stem_variant, pada["text_padapatha"])
                for stem_variant in pada["stem"].split(" ")
            ]):
                raise Exception(
                    f'Stem {pada["stem"]} not found in the padapatha text "{pada["text_padapatha"]}"'
                )

            padas.append(pada)

        return padas
