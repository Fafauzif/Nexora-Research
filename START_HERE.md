# Nexora indirect-benchmarking data collection — start here

**Run date:** 26 October 2026. **Purpose:** collect and clean broad external reference data for a fictional e-commerce case. **No new sentiment, topic, causal, financial or strategy analysis was performed in this collection run.**

## What this package is

This is a multi-stratum collection. It combines public research dataset imports, supplementary marketplace app reviews, limited current search-index retrieval and an actual Agent Reach public-web pilot. It is **not** millions of fresh Reddit/X records, not Nexora internal data, and not a representative sample of Indonesian buyers or sellers.

The casebook remains the complete supplied internal evidence base and takes precedence over the guidebook by the user's explicit decision. External records are material for indirect mechanism benchmarking, not observations of Nexora.

## Exact counts

| Stratum | Raw selected records | Clean records / leads | What these are |
|---|---:|---:|---|
| Supplementary app reviews | 1,835,693 | 1,834,939 | Historical Google Play reviews of five e-commerce apps; not Reddit/X |
| Historical Twitter support | 513,077 | 513,077 | Individual tweets in selected connected components; snapshot2017 with older context |
| Published small e-commerce/X samples | 951 | 949 | Source PDF/CSV samples; mixedlocale and promotional content retained/qualified |
| **Published-source record inventory total** | **2,349,721** | **2,348,965** | **Record inventory only; not globally independent people/posts** |
| Public indexed social leads, separate | 330 Agent Reach +248 built-in-search appearances; overlaps retained in logs | 415 unique source URLs | 376 Reddit-thread URLs and39 X metadata records; partial representations, separate from above |


Raw/clean row counts describe records, not unique people, unique customers, independent experiences or verified events. Company support messages and customer messages are both retained where needed for conversation context. Duplicated text may be legitimate separate tweets. Do not pool the strata into a market sentiment percentage.

## File map

- `documentation/METHODOLOGY_COLLECTION_AND_CLEANING.md`: actual acquisition routes, screening, cleaning, accounting and limitations.
- `documentation/COLLECTION_PROTOCOL.md`: refined broad research protocol and planned query matrix; proposals are distinguished from actions actually performed.
- `documentation/QA_REVIEW.md`: independent audit, plus source-level validation files.
- `documentation/DATA_DICTIONARY.md`: route-specific schemas and joining/reading rules.
- `documentation/LICENSE_AND_ATTRIBUTION.md`: dataset authors, source links and declared licenses; this package does not override source conditions.
- `datasets/app_reviews/raw/`: three unchanged original downloaded ZIP archives.
- `datasets/app_reviews/clean/app_reviews.jsonl.gz`: authoritative cleaned app-review data; exclusions are in a separate file.
- `datasets/app_reviews/source_manifest.json`, `metadata/`, `scripts/`, `METHODOLOGY.md`: provenance, exact counts and reproducibility.
- `datasets/twitter/`: licensed source-scoped historical support tweets and smaller published e-commerce samples, raw and clean, with source metadata/scripts/methodology.
- `datasets/social_search/`: actual Agent Reach envelopes, built-in search retrieval, partial source reads, cleaned/indexed lead records, query/access logs and cross-route URL registry. Search results are not guaranteed full posts or complete threads.
- `source_discovery/`: sources considered but excluded; these contribute **zero** delivered corpus records.
- `tooling/`: Agent Reach version/channel outputs, source commit, public-only pilot scripts and run logs. No credentials, browser profiles or environments are included.
- `context/IBSC_2026_Nexora_Master_AI_Context_Pack_UPDATED.md`: full earlier context plus the subsequent conversation and actual run status. Prior analyses are historical context, not new analysis of this corpus.
- `MANIFEST_FILES.csv` / `MANIFEST_FILES.json`: relative filenames, byte sizes and SHA-256 checksums for payload files.
- `RUN_SUMMARY.json`: machine-readable counts and scope.
- `scripts/verify_package.py`: integrity and parse-count verification of the delivered files.

## Reading large clean files

The `.gz` files are gzip-compressed text, not proprietary formats. Use Python/R/SQL tools or decompress them before loading. The app corpus exceeds the worksheet row limit of a single Excel sheet; do not expect opening it in Excel to preserve every row.

```python
import gzip, json, csv
with gzip.open('datasets/app_reviews/clean/app_reviews.jsonl.gz', 'rt', encoding='utf-8') as handle:
    for line in handle:
        row = json.loads(line)
        # process one record at a time; no need to hold all records in memory

with gzip.open('datasets/twitter/clean/twcs_ecommerce_connected_clean.csv.gz', 'rt', encoding='utf-8', newline='') as handle:
    for row in csv.DictReader(handle):
        pass
```

CSV fields may contain quoted newlines. Use a CSV parser, not physical line counts, to count tweets. The `.jsonl` app file has one JSON object per physical line. CSV copies and JSONL copies of the same records are alternate formats, not additional observations.

## How to use this later

Begin with a decision-linked slice of the data, retaining source/date/geography and record-type distinctions. The archive deliberately retains positive, neutral, short and negative app reviews; they are not all mechanism-relevant. Any future analysis should define eligibility, validate language/role/geography where material and avoid confusing company responses with customer testimony.

The historical majority is useful for exploring mechanisms or developing a codebook, not measuring 2025–2026 Indonesian policy impacts. The smaller contemporary/indexed material has a different retrieval bias. No representativeness, completeness or causality claim is attached to either.
