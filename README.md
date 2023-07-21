### Old Patterns in the Meter: The Curious Case of Sanskrit Ninth Class Vowels

WIP. For details on the study, please see [README.pdf](README.pdf).

---

Our study is composed of the following distinct stages – the details of each are documented in the corresponding Python notebook file, which can also be used to reproduce its final results. For a summary of what each stage entails, please see [README.pdf](README.pdf).


#### 1. Raw Rigveda Corpus

notebook: [1_raw_corpus.ipynb](1_raw_corpus.ipynb) | helper: [src/transform_json_corpus.py](src/transform_json_corpus.py)<br>
results: [data/rv_samhitapatha_vnh.txt](data/rv_samhitapatha_vnh.txt), [data/rv_padapatha_lubotsky.txt](data/rv_padapatha_lubotsky.txt)


#### 2. Roots and Stems of the Ninth (and Fifth) Class

notebook: [2_roots.ipynb](2_roots.ipynb) | helper: [src/lib/roots.py](src/lib/roots.py)<br>
results: [data/roots.csv](data/roots.csv)


#### 3. Searching for Stanza Attestations of the Roots and Stems

notebook: [3_roots_with_attestations.ipynb](3_roots_with_attestations.ipynb) | helper: [src/lib/roots_attestations.py](src/lib/roots_attestations.py)<br>
results: [data/roots_with_attestations.csv](data/roots_with_attestations.csv), [data/roots_with_attested_words.json](data/roots_with_attestations.csv)


#### 4. Verse Lines (for attested stems; enriched with stanza metadata)

notebook: [4_verse_lines.ipynb](4_verse_lines.ipynb) | helper: [src/lib/verse_lines.py](src/lib/verse_lines.py)<br>
results: [data/rv_lines.csv](data/rv_lines.csv)


#### 5. Metrical Analysis of the Verse Lines

notebook: [5_verse_lines_with_meter.ipynb](5_verse_lines_with_meter.ipynb) | helper: [src/lib/meter.py](src/lib/meter.py), [src/test_meter_analysis.py](src/test_meter_analysis.py)<br>
Final Files: [data/rv_lines_with_meter.csv](data/rv_lines_with_meter.csv)


#### 6. Final Analysis

notebook: [6_analysis.ipynb](6_analysis.ipynb)<br>
