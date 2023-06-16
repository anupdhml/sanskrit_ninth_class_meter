EARLIER_LANGUAGE_HEADER = "A. Earlier Language"
EARLIER_AND_LATER_LANGUAGE_HEADER = "B. Earlier and Later Language"
LATER_LANGUAGE_HEADER = "C. Later Language"

CLASS_HEADER = "-class" # matches both "4. nu­class" and "6. nā-class"

NINTH_CLASS = "ninth"
NINTH_CLASS_STRONG_MARKER = "ā"
NINTH_CLASS_WEAK_MARKER = "ī"

FIFTH_CLASS = "fifth"
FIFTH_CLASS_STRONG_MARKER = "o"
FIFTH_CLASS_WEAK_MARKER = "u"


def adjust_root_guess_to_vedaweb(root, variant_no, present_class):
    if present_class == NINTH_CLASS:
        # FIXME better place to keep these?
        if root == "pu":
            root = "pū"
        elif root == "ju":
            root = "jū"
        elif root == "ji":
            root = "jī"
        elif root == "vr̥" and variant_no == '2': # choose, will match
            # variant_no 1 'cover' is attested only in AV. 2 is 'choose'
            # FIXME set stem as variant here too and ensure both are searched for
            # but long variant doesn't have any hits here so safe to ignore this here
            #root = "vr̥ ~ vr̥̄"
            # also if we pass it like this, we should also change the stems here
            root = "vr̥ vr̥̄" # other root is vr̥ (1, cover which won't match in RV)
        # FIXME better way to pass these exceptions
        # modifying the root here ensures for now we only find matches for the variants
        # used in vedaweb
        # SrI 1 mix: yes
        # SrI 2 boil: not (VB: SrInati..)
        elif root == "śrī" and variant_no == '2': # boil
            root = "śrī 2" # other root is śrī (1, mix) which WILL match
        # aS 1 attain: not (only in mahabhharata 'aSnIs')
        # aS 2 eat yes
        elif root == "aś" and variant_no == '1': # eat
            root = "aśⁱ" # other root is aś (2, attain) which won't match
        # gR as gr̥̄ 1 "sing" attested
        # gR 2 "swallow" not (only in AVS)
        elif root == "gr̥" and variant_no == '1': # sing
            root = "gr̥̄ 1" # other root is gr̥ (2, swallow) which won't match
        elif root == "i": # send (won't match in RV)
            root = "i 2" # other root is i (1, go) which doesn't have ninth class
        #elif variant_no:
            # FIXME assign vedaweb equivalent variant numbers here?
        #    root += ' ' + variant_no

    elif present_class == FIFTH_CLASS:
        if root == "ci" and variant_no == '1': # gather
            root = "ci 1" # other root is ci (2, observe) which won't match
        elif root == "mi" and variant_no == '1': # fix
            root = "mi 1" # other root is mi (2, damage) which won't match
        elif root == "pr̥" and variant_no == '1': # fill (wont' match either)
            root = "pr̥ 1" # other root is pr̥ (2, be busy) which won't match
        elif root == "vr̥" and variant_no == '2': # choose, won't match
            root = "vr̥ vr̥̄" # other root is vr̥ ūr (just vr̥ in vedaweb) (1, cover) which WILL match
        elif root == "i": # send
            root = "i 2" # other root is i (1, go) which doesn't have fifth class
        elif root == "u": # proclaim
            root = "u 1" # there's no u 2 variant
        elif root == "r̥": # go, send
            root = "r̥ 1" # there's no r̥ 2 variant

    else:
        raise Exception(f"Unsupported present class: {present_class}")


    return root


def parse_whitney_rootline(line, present_class):
    if present_class == NINTH_CLASS:
        class_strong_marker = NINTH_CLASS_STRONG_MARKER
        class_weak_marker = NINTH_CLASS_WEAK_MARKER
    elif present_class == FIFTH_CLASS:
        class_strong_marker = FIFTH_CLASS_STRONG_MARKER
        class_weak_marker = FIFTH_CLASS_WEAK_MARKER
    else:
        raise Exception(f"Unsupported present class: {present_class}")

    variant_no = None
    attestation_texts = None
    weak_only = False

    line_parts = line.split()
    if line_parts[0].isdigit():
        variant_no = line_parts.pop(0)
    stem = line_parts.pop(0)
    if line_parts:
        attestation_texts = " ".join(line_parts)

    # this is an assumption safe to make for our data even if there's multiple stem variants
    if present_class == NINTH_CLASS and stem.endswith(class_weak_marker):
        weak_only = True

    # if stem has a variant it will be marked '/'
    stem_variants = stem.split('/')
    weak_stem_variants = []
    strong_stem_variants = []
    root_variants = []

    # populate all the variants above
    for stem_variant in stem_variants:
        # removes the last two chars
        # at this stage, this is a guess only and may not match what is actually used
        # in the grammars/ dictionaries
        root_variants.append(stem_variant[:-2])

        if stem_variant.endswith(class_weak_marker):
            weak_stem_variants.append(stem_variant)
            strong_stem_variants.append(stem_variant[:-1] + class_strong_marker)
        else:
            strong_stem_variants.append(stem_variant)
            weak_stem_variants.append(stem_variant[:-1] + class_weak_marker)
    root_variants = sorted(list(set(root_variants)))

    # set the final strings
    root = ' '.join(root_variants)
    strong_stem = ' '.join(strong_stem_variants)
    weak_stem = ' '.join(weak_stem_variants)

    root = adjust_root_guess_to_vedaweb(root, variant_no, present_class)

    return {
        "root_guess": root, # this is really an estimated guess based on the stem
        "variant_no": variant_no,
        "strong_stem": strong_stem,
        "weak_stem": weak_stem,
        "weak_only": weak_only,
        "attestation_texts": attestation_texts,
    }

###############################################################################

def parse_whitney_roots(filepaths):
    whitney_roots = []

    for filepath in filepaths:
        present_class = None
        if "ninth_class" in filepath:
            present_class = NINTH_CLASS
        elif "fifth_class" in filepath:
            present_class = FIFTH_CLASS

        with open(filepath, 'r') as whitney_file:
            language_period = None

            while line := whitney_file.readline():
                line = line.rstrip()

                if not line or CLASS_HEADER in line:
                    continue
                elif EARLIER_LANGUAGE_HEADER in line:
                    language_period = "Earlier"
                    continue
                elif EARLIER_AND_LATER_LANGUAGE_HEADER in line:
                    language_period = "Earlier & Later"
                    continue
                elif LATER_LANGUAGE_HEADER in line:
                    language_period = "Later"
                    continue

                whitney_roots.append(
                    parse_whitney_rootline(line, present_class) | {
                        "language_period": language_period,
                        "present_class": present_class,
                    }
                )

    return whitney_roots
