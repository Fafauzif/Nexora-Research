# Data dictionary and record units

There is intentionally no single flattened file combining all sources. Their observation units, fields and sampling routes differ. Use source-specific clean files and retain the source/stratum key.

## App reviews

Authoritative file: `datasets/app_reviews/clean/app_reviews.jsonl.gz`.

- `record_id`: source-specific row locator, not a platform-native review ID.
- `source_id`, `source_url`, `source_archive_member`, `source_row_index`: raw lineage; the row index is zero-based after the CSV header.
- `collection_stratum`, `record_type`: historical supplementary Google Play app-review identity.
- `platform_discussed`: app associated with source file, not a predicted target of the text.
- `published_at_source`, `published_date`, `source_timezone`: original date, parsed calendar date, explicit or unknown timezone.
- `text`: conservative NFC/whitespace normalization, case/slang/punctuation retained.
- `rating`, `helpful_votes`, `app_version`: source attributes, not new analysis.
- `native_review_id`, `language`, `reviewer_country`: unknown/null where source does not provide them.
- `geography_note`: source-context qualification, not verified per-person location.
- `license_declared_by_dataset`: dataset metadata license.
- `text_sha256`: SHA-256 of **exact normalized text** for this stratum.
- `dedup_key_sha256`: app/date/rating/text exact-record identity used for deduplication.
- `nexora_data`: false; `sentiment_or_topic_analysis_performed`: false.

Full schema and counting criteria: `datasets/app_reviews/METHODOLOGY.md`. Exclusions file is a QC ledger, not part of the clean record count.

## Historical Twitter support records

Authoritative file: `datasets/twitter/clean/twcs_ecommerce_connected_clean.csv.gz`.

Fields include source record locators, source URL/platform, tweet record type, core/adjacent stratum, source datetime, company/courier/retail category, original inbound flag, company/customer/other role, cleaned text, reply references and a connected-component conversation ID. See `datasets/twitter/DATA_DICTIONARY_X.md` for all fields.

Important details:

- Numeric source tweet IDs are surrogates; do not build live `x.com/status/` links from them.
- `conversation_id` is a connected component in the observed source graph. It does not certify complete conversation coverage.
- `company_handles` can include several accounts, so counts grouped by handle can overlap.
- `company_types` distinguishes marketplace, courier and adjacent retail source scope.
- `inbound_as_reported` preserves source directional metadata.
- Per-record language is `und`/unknown. Source-predominantly-English wording is contextual; some actual text is in other languages.
- `source_year` denotes the 2017 snapshot, not every record's year. Actual dates span older linked context.
- `text_sha256` here is SHA-256 of **casefolded cleaned/redacted text**, unlike the app-review exact-text hash. Do not use identically named hashes across strata as a universal duplicate key.
- Identical text with distinct tweet IDs remains separate when preserving conversation context.

Raw scoped original-row file: `datasets/twitter/raw/twcs_ecommerce_connected_original_rows.csv.gz`. It contains original source columns and selected original values; CSV serialization/gzip are generated, so it is not byte-identical to a subsection of the source ZIP. The full original ZIP fingerprint is in metadata.

## Smaller published e-commerce tweet samples

Authoritative clean representation: `datasets/twitter/clean/zenodo_ecommerce_twitter_clean.jsonl`. CSV is an alternate representation of the same 949 records, not another 949 observations.

Read the source-specific dictionary for page/row locators, original versus parsed dates, redaction flags and inherited labels. A field named `created_at_utc` can contain **date-only information** when the source lacks a timestamp; do not assume a verified UTC time. Source country/language/role are not inferred from the dataset title. Mixed promotional content and encoding artifacts remain qualified.

## Indexed social source leads and excerpts

Authoritative clean files are under `datasets/social_search/clean/` and `datasets/social_search/agentreach_clean/`. The cross-route URL registry is the inventory of unique discovered source URLs. Inspect `datasets/social_search/README_SOCIAL_COLLECTION.md` and route logs for actual filenames and fields.

A result is an indexed URL/excerpt, not necessarily full post text. X metadata headings are not tweet bodies. Partial page reads are supplementary representations of already discovered URLs and must not be added to post counts. Retrieval appearances, unique URLs, complete posts and individual comments are not interchangeable.

## Provenance joins and missing values

Use the source registry key + row/member locator within each archive. Do not join individuals across sources using names, masked IDs, numeric surrogates, repeated text or inferred identity. Missing language/country/role stays unknown until explicitly supported by a later authorized processing step. Do not impute empty text or create synthetic source records.
