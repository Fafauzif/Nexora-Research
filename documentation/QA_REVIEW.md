# Independent data-preparation quality review

## Scope

This review checks the prepared files, source provenance, count reconciliation, schema, identifiers and documented cleaning. It does not analyze opinions, themes, commercial outcomes or causality, and does not validate the truth of individual social posts or app reviews. No dataset was modified by the reviewer.

The main checks below were conducted by a separate agent from the source collectors. The checks read the final compressed data streams and available raw source archives. Results refer to this snapshot; a subsequent data rewrite requires rerunning the appropriate checks and refreshing file hashes.

## Overall result

The app-review and historical Twitter data streams passed the independent structural checks completed for this review. No parsing, record-ID uniqueness, nonempty-text, text-integrity-hash, app rating-range, or recorded unknown-geography issues were found in the checked streams. These findings are technical verification, not evidence of representativeness, topical relevance, current market conditions, or correctness of source licenses.

Three large/small published-source strata comprise 2,348,965 retained source records before any separately collected live/search-index representations are added: 1,834,939 app reviews, 513,077 scoped historical support tweets, and 949 published Zenodo text records. This arithmetic is not a count of unique people, independent experiences or globally deduplicated statements.

## 1. Supplementary app reviews

### Independent checks performed

- Fully decompressed and parsed `app_reviews.jsonl.gz`, validating gzip trailer/stream integrity as a consequence of reading the full stream.
- Counted every retained JSON record, rather than relying on file size, sampling or source manifests alone.
- Checked each `record_id` for uniqueness in this stream.
- Verified each record's `text_sha256` against the exact normalized `text` field.
- Checked all retained text is nonempty and star ratings are integers within 1–5.
- Confirmed per-record `language` and `reviewer_country` remain null; no geolocation or language inference was inserted.
- Confirmed `nexora_data` is false and `sentiment_or_topic_analysis_performed` is false on every record.
- Independently recomputed date ranges by source and counts per source.
- Independently read all five selected raw CSV members from the three accepted original ZIPs, counted their rows, and compared their counts with collector records.
- Independently recomputed SHA-256 hashes of all three accepted raw ZIPs and compared them to the source manifest.
- Read the cleaning script to establish that it preserves case, meaningful words, punctuation, emoji and language: normalization is NFC, selected control-character replacement, whitespace collapse and trimming. It does not lowercase original text, stem, translate or perform sentiment/theme classification.

### Count reconciliation

| App | Raw selected member rows independently counted | Clean records independently counted |
|---|---:|---:|
| Shopee | 782,079 | 781,789 |
| Lazada | 775,323 | 774,911 |
| Tokopedia | 71,242 | 71,229 |
| Bukalapak | 90,147 | 90,127 |
| Blibli | 116,902 | 116,883 |
| **Total** | **1,835,693** | **1,834,939** |

The 754 exclusions reconcile to 701 empty/null-like text rows and 53 exact app/date/rating/normalized-text duplicate-key rows. Exact-key equality is an operational cleaning rule; it does not prove that the excluded entries were submitted by the same person. Repeated short text on different dates remains.

Source metadata declares CC BY-NC-SA 4.0 for the bwandowando Shopee/Lazada datasets and CC0 for rezkyyayang's multiapp dataset. The reviewer verified that those labels are present in the saved dataset metadata; this is not an independent legal determination of rights in every underlying review.

### Necessary interpretive boundaries

- These are Google Play app reviews, not product reviews, Reddit posts, X posts, or live Agent Reach results.
- Source app location/context does not identify each reviewer's nationality or location.
- Shopee/Lazada end in November 2023; Tokopedia/Bukalapak end in October 2024; Blibli ends in February 2025. Do not describe the entire corpus as current 2025–2026 reactions.
- The multiapp raw archive retains its original additional app files to preserve source integrity; only Tokopedia, Bukalapak and Blibli contribute to clean-corpus counts.
- Clean records remove direct author columns but free text is not guaranteed fully de-identified. The raw archives are original source exports.

Machine-readable checks: `qa_validation.json` and `qa_raw_validation.json`.

## 2. Historical Twitter support conversations

### Independent checks performed

- Fully decompressed and parsed the final `twcs_ecommerce_connected_clean.csv.gz`.
- Counted 513,077 clean rows and 513,077 unique record IDs.
- Independently counted 126,882 connected-component identifiers, matching the manifest.
- Independently counted 438,115 core marketplace/courier rows and 74,962 adjacent-retailer rows; those strata reconcile additively to the full scoped Twitter total.
- Verified all text is nonempty and each `text_sha256` equals SHA-256 of **casefolded** normalized/redacted text.
- Confirmed per-record language is `und` and country is `unknown`; source language context is not an individual-language classifier.
- Checked company-type and source `inbound_as_reported` fields exist and hold expected values.
- Independently verified date range: 2011-10-13T11:57:18+00:00 through 2017-12-03T23:13:02+00:00.
- Independently counted the scoped source-faithful raw CSV: 513,077 rows, matching clean count; this run reported no empty-text or duplicate-ID exclusions in that stratum.
- Read the selection/cleaning code: reply-component selection retains conversational context, not only complaints; repeated text with different source IDs is deliberately preserved.

The complete original source contains 2,811,774 records. It was an intermediate input and is not the delivered scoped Twitter count. The delivered raw file contains selected original field values reserialized as CSV and gzip; it is source-faithful, not byte-identical to the entire original archive.

### Issues caught and corrected during preparation

The initial Twitter language value could be mistaken for a per-record English assertion despite multilingual rows. The collector changed it to `und` and retained an explicit source-level language-context note. The final schema also contains `company_types` and `inbound_as_reported`, distinguishing marketplace/courier versus adjacent retail and preserving the source direction flag.

The two similarly named text-hash fields use different definitions across strata: app reviews hash exact normalized text; TWCS hashes casefolded normalized/redacted text. Source dictionaries describe this difference. They are not a shared universal cross-source deduplication key.

### Necessary interpretive boundaries

- This is a published historical support dataset snapshot from 2017, with some older linked tweets; not all individual tweet dates are 2017.
- It is not an Indonesian-only corpus, fresh X scrape, or Nexora internal evidence.
- The source's numeric tweet identifiers are surrogate/anonymized IDs. They must not be interpolated into fabricated live X status URLs.
- Connected components are not independent customers; company-linked counts may overlap and must not be summed.
- Existing source CC BY-NC-SA 4.0 terms remain attached to the derived scoped exports. No single umbrella ZIP license replaces source-specific conditions.

Machine-readable checks: `qa_twitter_validation.json`. Original-source value checking also passed: 21 systematically selected scoped raw rows matched every original field value while independently scanning all 2,811,774 source CSV rows. Results are recorded in `qa_twitter_source_fidelity.json`.

## 3. Small published X/Zenodo sources

The prepared Zenodo JSONL contains 949 parseable records with 949 unique record IDs, matching its manifest. Provenance includes dataset source, original file and PDF page/row locators where original post IDs are unavailable.

The first inspected PDF-derived example is a Malaysian-currency promotional listing. That illustrates why source title/brand keywords are not verified Indonesian geography, seller identity or mechanism relevance. These sources must remain labeled mixed-language brand-keyword samples; promotions were not removed as though cleaning were completed topical analysis.

Some `created_at_utc` values are date-only. Treat them as source calendar dates, not verified UTC times. PDF extraction is not live tweet hydration, and malformed `/undefined/` links are flagged rather than represented as verified public post URLs. The original PDFs/CSV are retained for checking extraction and source artifacts.

## 4. Search-index and live public-web representations

The final actual Agent Reach public-web stream contains 251 records, all Reddit, deduplicated by canonical URL from 330 result appearances. Its inventory contains 36 raw query envelopes (including the root pilot), 35 subagent query-log rows (32 successful Reddit queries and three failed X queries), plus one successful root Reddit pilot. Thus the combined represented run has 33 successful envelopes and three failed envelopes; the reported inventory's 32-success field refers to the subagent log scope. Failed X public-web attempts are retained as failures, not records.

The separate built-in search-service stream contains 202 records: 163 Reddit and 39 X source URLs. There are seven partial Reddit thread-read representations, which can overlap these URL records and are not additional independent source posts.

Independent final parsing verified 251 and 202 stream records, unique canonical URLs within each stream, a cross-stream union of 415 source URLs and an overlap of 38 URLs. The source registry contains exactly those 415 URLs. Final registry scope is 376 Reddit URLs and 39 X URLs. These are URL-level discovery records, not unique users or guaranteed independent conversations; the X search-service representation can be metadata/excerpt-limited. No authenticated live X collection was achieved.

Source envelopes, queries and limited representations remain separate from the downloaded historical datasets. This QA does not establish full-text completeness, complete comment trees, representative recruitment, exhaustive search or business relevance. Machine-readable checks are in `qa_social_validation.json`.

## 5. Packaging checks and recommendations

- Package only explicit manifest-listed deliverables. Working folders contain large dotfiles, partial downloads and temporary synchronization artifacts that are not research records.
- Keep accepted raw archives/scoped rows, clean streams, exclusion logs, source metadata, licenses/attribution, method descriptions, scripts and technical manifests separate and discoverable.
- Do not package virtual environments, browser/session data, caches, access keys or temporary signed download URLs.
- Preserve archived source hashes and source version metadata; future “latest” downloads may differ.
- Count records by stratum and disclose overlapping representations. Do not claim global unique people or all data collected by Agent Reach.
- Final ZIP integrity/manifest checks are the packager's responsibility after source agents stop writing. The independent data checks above precede the final ZIP and do not establish its integrity by themselves.

## Reproduction of QA

`run_qa_validation.py` validates the full app clean stream. `run_qa_raw.py` validates app raw counts and hashes. `run_qa_twitter.py` validates full scoped Twitter clean/raw streams. `run_qa_twitter_source_fidelity.py` checks systematic raw-row samples against the original intermediate source archive when available. Paths in these reviewer scripts describe the working collection layout; packaged copies may need path adjustment to the final layout. They are technical verification scripts, not sentiment or business-analysis code.
