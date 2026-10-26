# X/Twitter published-corpus collection and cleaning

This package contains published historical Twitter records used as indirect mechanism benchmarks for the fictional Nexora case. It is a data collection/cleaning output only: no sentiment labels, theme classification, inferred user roles beyond source metadata, impact estimates, business findings or causal analysis were generated.

## 1. Scope and source strata

### A. Thought Vector / Stuart Axelbrooke: Customer Support on Twitter

- Original provider: Thought Vector, creator Stuart Axelbrooke.
- Official dataset: https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter
- Download route: public anonymous Kaggle dataset download endpoint, recorded in metadata and logs. No account, login cookies, private page, CAPTCHA or access-control bypass used.
- Official metadata identifies version 10, last updated 2017-12-03 and license CC BY-NC-SA4.0. This source is predominantly English and historical. It is not a current scrape of X, not Indonesian marketplace evidence, and not a Nexora internal dataset.
- Whole downloaded source archive contains 2,811,774 tweet records. The exact ZIP size and SHA256 are recorded in `metadata/twcs_manifest.json`. The complete multi-industry ZIP was used as an intermediate but intentionally omitted from the deliverable to avoid distributing unrelated industry records.
- Delivered raw CSV is **scope-filtered source-faithful rows**, not the entire dataset: source field values are unchanged and in original source order, but serialization is reconstructed as CSV and gzip compressed.
- Company support seeds selected: marketplace `AmazonHelp` and `AskeBay`; courier `UPSHelp`; adjacent retailers `AskTarget`, `ArgosHelpers`, `NeweggService`, `Walmart`, `NikeSupport`. These roles describe the organization, not a proven topic for every record. No grocery, airline, telecom, gaming or unrelated corporate corpus was added to increase size.
- Build an undirected graph from source `tweet_id`, `in_response_to_tweet_id` and `response_tweet_id` reply links. Retain the complete connected reply components containing at least one tweet authored by a selected company. Keep customer replies and generic responses in these components to preserve context rather than select only complaints.
- Numeric tweet identifiers are anonymized/surrogate identifiers in this published source. They are **not usable Twitter status IDs**. No fabricated live post URLs are constructed; `source_url` points to the dataset, while `source_record_id` locates the raw record.
- `conversation_id` denotes a connected component under the source reply graph. It is not a count of independent customers or a guarantee of a single issue. Parent IDs absent from the dataset can join components, and multi-company conversations can exist.
- Company-linked record counts can overlap and must not be summed. `records_by_stratum_additive` is additive. Record count, conversation count and unique text count are separately reported.
- `inbound_as_reported` and source `author_id` preserve source metadata. Role `company_support` identifies a selected company author. `customer_or_other_inbound` is a source direction flag, not independently verified identity. Other support participants may remain in mixed-company components.
- Country is unknown; no geography is inferred from a brand name or English text. Per-record `language` is `und` (unknown/not classified); `language_basis` supplies only the source-level predominantlyEnglish/multilingual context. Dates are parsed from each source row; the collection is historical even if a very early linked tweet predates the main source period.

### B. Zenodo record15845921: Data Posting Shopee dan Tokopedia

- Source: https://zenodo.org/records/15845921 ; DOI10.5281/zenodo.15845921.
- Creator: Dian Kurnianingrum, Binus University; published metadata2025. Actual dates in the PDFs are recorded per row and should not be relabeled as the publication year.
- License: CC BY4.0, as returned by the public Zenodo API metadata retained in `metadata/`.
- Files: two8-page PDFs. PyMuPDF natural reading order is used; `created_at` date patterns delimit rows. The complete page text is retained as JSONL, and original PDFs are delivered unchanged.
- The extraction yields418 Shopee rows and460 Tokopedia rows. Record locators contain source filename, physical PDF page and row position. These are extracted text observations, not independently hydrated or live-verified tweets.
- PDFs do not supply reliable original tweet IDs or full post permalinks. No IDs, authors or locations are invented. The dataset contains mixed-country/mixed-language promotions, listings and discussions. It is a broad brand-keyword sample, not a representative Indonesian consumer corpus.
- Source files already contain mojibake, unusual ligatures and possible line-reading artifacts. These are not silently rewritten. Exact PDF sources remain authoritative for checking extraction.

### C. Zenodo record18198239

- Source: https://zenodo.org/records/18198239 ; DOI10.5281/zenodo.18198239.
- Creator: Gian Gefriel Hernando Banna, Binus University; publication2026-01-09; CC BY4.0 per saved metadata.
- Original file `sentiment_analysis_data (1).csv` contains73 records. Its title mentions AI implementation, but inspected rows contain mixed-language broad Shopee-related posts and promotions. The title is not treated as a verified topical label.
- All source rows are retained in raw; text record IDs, source language codes and reported URLs are carried forward. Many source URLs contain `/undefined/`; they are flagged, not presented as verified accessible tweet links. No URL hydration was performed.
- Geographic identity is unknown. Source language code `in` is retained as reported, not converted into proof of Indonesian residence.

## 2. Cleaning

- UTF8 decoding with the input's expected CSV/PDF encoding; original bytes are preserved separately.
- NFC Unicode normalization, HTML entity unescaping, control-character removal for TWCS, and whitespace normalization. `text_sha256` is SHA256 of casefolded normalized/redacted clean text encoded asUTF8; it is not an exact-case source-byte fingerprint.
- Empty text removed; duplicate source tweet IDs removed for TWCS. Repeated exact text with different source IDs is retained to preserve conversation structure; count unique text hashes separately.
- Zenodo exact normalized text duplicates are removed **within source**; cross-source potential duplicates are not merged because PDF records lack IDs and source context differs. Two duplicate PDF rows removed in this run.
- Emails and long numeric sequences are replaced conservatively in the clean text. Zenodo's recognizable public address spans are also masked. These automated redactions can mask non-contact number strings; raw data allow validation. No de-identification completeness guarantee is made.
- Usernames in source text are not automatically role-labeled; no names, personal profiles, account histories or private information were enriched. Original source-supplied author fields remain in source-faithful raw.
- No stopword removal, stemming, translation, sentiment inference, topic inference, geolocation inference or promotional-content deletion. This leaves the corpus suitable for later screening without pretending that cleaning equals relevance validation.
- No labels already present in a source are treated as verified facts. The delivered normalized schema does not add sentiment labels.

## 3. Counts, reproducibility and limits

Read `metadata/twcs_manifest.json` and `metadata/zenodo_manifest.json` for exact raw/clean counts, date coverage and exclusions. `metadata/zenodo_cleaning_exclusions.json` records removed row IDs. Download logs contain original public request URLs, byte lengths and SHA256 fingerprints; redirects with temporary signed URLs are not recorded in user-facing provenance.

The scripts reproduce imports, scope selection and cleaning. They are deterministic conditional on the same downloaded versions and Python/PyMuPDF behavior. `collect.py` downloads public source files; `process_twcs.py` requires the complete intermediate Kaggle ZIP; `process_zenodo.py` requires the delivered PDFs and CSV. The source APIs can change or remove access. No completeness claim is made for all X discussion, all company conversations, all customers or contemporary Indonesia.

Current scope does not include fresh X scraping or Agent Reach live results because this task did not establish an authenticated local X session. These records must never be labeled as a new Agent Reach scrape. A later live collection should retain separate run/query logs and remain a separate source stratum.

## 4. Attribution and redistribution

Thought Vector / Stuart Axelbrooke, *Customer Support on Twitter*, Kaggle dataset version10, last updated2017-12-03. Derived scoped clean/raw row exports in this folder are distributed under the source's CC BY-NC-SA4.0 conditions with attribution and notice of the scope and cleaning changes. Original tweet rights and platform conditions may also apply; the uploader license is provenance, not proof of unrestricted rights to every underlying text.

Dian Kurnianingrum, *Data Posting Shopee dan Tokopedia*, Zenodo record15845921, DOI10.5281/zenodo.15845921, CC BY4.0. Gian Gefriel Hernando Banna, *Dataset of Comparison of User Sentiment towards AI Implementation in Shopee and Tokopedia–TikTok Shop Applications Based on X/Twitter*, Zenodo record18198239, DOI10.5281/zenodo.18198239, CC BY4.0. Text normalization, extraction, deduplication and redaction are modifications made for this package; source metadata is preserved.
