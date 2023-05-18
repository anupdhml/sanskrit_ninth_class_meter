import json
import sys

# from ./meter.py
import meter

from pathlib import Path


# get items missing in list 2 but present in list 1
def missing_items(list1, list2):
    return sorted(list(
        set(list1).difference(set(list2))
    ))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f'Usage: {sys.argv[0]} <sanskrit_text_json_file>')
        sys.exit(1)

    sanskrit_text_json_file = sys.argv[1]

    # use the same base filename as the input file for the output
    output_file = f'data/{Path(sanskrit_text_json_file).stem}.txt'

    with open(sanskrit_text_json_file) as f:
        sanskrit_text_json = json.load(f)

        # rudimentary determination for which special chars to use
        if "vnh" in sanskrit_text_json_file:
            special_chars_to_filter = meter.SPECIAL_CHARACTERS_SAMHITAPTHA_VNH
        elif "lubotsky" in sanskrit_text_json_file:
            special_chars_to_filter = meter.SPECIAL_CHARACTERS_PADAPATHA_LUBOTSKY
        else:
            # might cause problems for other texts, be careful!
            special_chars_to_filter = \
                meter.SPECIAL_CHARACTERS_SAMHITAPTHA_VNH + meter.SPECIAL_CHARACTERS_PADAPATHA_LUBOTSKY

        sanskrit_text = ""
        unique_sanskrit_chars = set()

        for stanza_no, padas in sanskrit_text_json.items():
            for pada in padas:
                pada_id = pada[0]
                pada_text = pada[1]

                # line 4.046.06b seems to have extra 'f' at the end which is not
                # there in the original. so remove it
                # https://lrc.la.utexas.edu/books/rigveda/RV04#H046
                # can port this to jupyter notebooks too, if it ever crops up there
                if pada_text == "táṁ devébhiḥ sajóṣasāf":
                    pada_text = "táṁ devébhiḥ sajóṣasā"

                sanskrit_text += f"{stanza_no}{pada_id} | {pada_text}\n"

                pada_text_cleaned = meter.clean_string(pada_text, special_chars_to_filter)
                unique_sanskrit_chars.update(
                    meter.get_sanskrit_chars(pada_text_cleaned)
                )

            sanskrit_text += "\n"

        with open(output_file, "w") as f2:
            f2.write(sanskrit_text)

        print(f"Successfully wrote the sanskrit text to {output_file}")

        sanskrit_chars = {
            "vowels_short": [],
            "vowels_long": [],
            "consonants": [],
            "special_chars": [],
            "others": []
        }

        for char in sorted(unique_sanskrit_chars):
            if char in meter.VOWELS_SHORT:
                sanskrit_chars["vowels_short"].append(char)
            elif char in meter.VOWELS_LONG:
                sanskrit_chars["vowels_long"].append(char)
            elif char in meter.CONSONANTS:
                sanskrit_chars["consonants"].append(char)
            elif char in meter.SPECIAL_CHARACTERS:
                sanskrit_chars["special_chars"].append(char)
            else:
                # these should all be chars prefixed with avagraha,
                # an artifact of how mark chars for our uses
                sanskrit_chars["others"].append(char)

        print(f"\nList of sanskrit chars used in the text:\n")
        [print(f"{k}: {v}") for (k, v) in sanskrit_chars.items()]

        sanskrit_chars_missing = {
            "vowels_short": missing_items(meter.VOWELS_SHORT, sanskrit_chars["vowels_short"]),
            "vowels_long": missing_items(meter.VOWELS_LONG, sanskrit_chars["vowels_long"]),
            "consonants": missing_items(meter.CONSONANTS, sanskrit_chars["consonants"]),
            "special_chars": missing_items(meter.SPECIAL_CHARACTERS, sanskrit_chars["special_chars"]),
        }

        # need to investigate if these missing are ok to ignore, or they
        # are written differently in the text
        print(f"\nList of sanskrit chars missing:\n")
        [print(f"{k}: {v}") for (k, v) in sanskrit_chars_missing.items()]
