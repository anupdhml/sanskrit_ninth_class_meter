### Old Patterns in the Meter: The Curious Case of Sanskrit Ninth Class Vowels

Computational corpus analysis of the [Rigveda](https://en.wikipedia.org/wiki/Rigveda), in order to check if the [poetic meter](https://en.wikipedia.org/wiki/Vedic_metre) there preserves any traces of a pre-form _**-ni-_ for the Sanskrit ninth class weak suffix _-nī-_.

Also validate metrical restorations in the Rigveda, in relation to the short root vocalism of the ninth class forms.

---

Our study is composed of the following distinct stages – the details of each are documented in the corresponding Python notebook file, which can also be used to reproduce its final results.

#### 1. Raw Rigveda Corpus

notebook: [1_raw_corpus.ipynb](1_raw_corpus.ipynb) | helper: [src/transform_json_corpus.py](src/transform_json_corpus.py)<br>
results: [data/rv_samhitapatha_vnh.txt](data/rv_samhitapatha_vnh.txt), [data/rv_padapatha_lubotsky.txt](data/rv_padapatha_lubotsky.txt)

Retrieve the raw text for the two versions of Rigveda that we are using, used to quickly validate the results in subsequent stages.

#### 2. Roots and Stems of the Ninth (and Fifth) Class

notebook: [2_roots.ipynb](2_roots.ipynb) | helper: [src/lib/roots.py](src/lib/roots.py)<br>
results: [data/roots.csv](data/roots.csv)

Parse and compile a list of ninth and fifth class roots/stems based on the comprehensive listing given by [Whitney (1887: 213–214)](https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-whitroot/disp/index.php?page=214).

#### 3. Searching for Stanza Attestations of the Roots and Stems

notebook: [3_roots_with_attestations.ipynb](3_roots_with_attestations.ipynb) | helper: [src/lib/roots_attestations.py](src/lib/roots_attestations.py)<br>
results: [data/roots_with_attestations.csv](data/roots_with_attestations.csv), [data/roots_with_attested_words.json](data/roots_with_attestations.csv)

Using [VedaWeb’s](https://vedaweb.uni-koeln.de) grammar search api, search the Rigveda for the finite verb forms associated with each of the ninth and fifth class stems, recording the RV location (_book.hymn.stanza_) where they are attested.

#### 4. Verse Lines (for attested stems; enriched with stanza metadata)

notebook: [4_verse_lines.ipynb](4_verse_lines.ipynb) | helper: [src/lib/verse_lines.py](src/lib/verse_lines.py)<br>
results: [data/rv_lines.csv](data/rv_lines.csv)

Compile the exact pādas with the verbal attestations, saving its text as well as other metadata like stanza meter and strata, obtained via the VedaWeb api.

#### 5. Metrical Analysis of the Verse Lines

notebook: [5_verse_lines_with_meter.ipynb](5_verse_lines_with_meter.ipynb) | helper: [src/lib/meter.py](src/lib/meter.py), [src/test_meter_analysis.py](src/test_meter_analysis.py)<br>
Final Files: [data/rv_lines_with_meter.csv](data/rv_lines_with_meter.csv)

For each of the pādas, programmatically generate its metrical scansion (i.e. whether each syllable is long or short), noting down meter failures (if any); also record the expected scansion of our stem vowels based on their position in the meter. This stage produces the final dataset for our main analyses.

#### 6. Final Analysis

notebook: [6_analysis.ipynb](6_analysis.ipynb)<br>

Analyze the overall as well as per-strata counts of _-nī-_ in each of the expected metrical positions (S, L, X), in relation to the control suffixes _-nā-_ and _-no-_, focussing on pādas composed in one of the popular meters.
