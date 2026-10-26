# Supplementary app-review collection: methodology and cleaning

## Status and boundaries

This is a **historical supplementary Google Play app-review stratum**, collected by downloading existing public datasets from Kaggle. It is **not Reddit or X collection**, not a live scrape performed by Agent Reach, not a representative sample of Indonesian customers, and not Nexora internal data. No sentiment/topic analysis, causal analysis, or business recommendation was performed.

The user requested a very broad collection with raw and clean records. Five marketplace-app files were selected from three public source archives because app experience can cover shipping, vouchers, shopping, discovery, seller/buyer usability and platform service. All non-empty reviews were retained regardless of rating, text length or whether they mention a predefined hypothesis. The historical collection is intentionally broad. Relevance-to-mechanism screening can be performed later under a separate analysis request; clean records do not claim every text discusses fees or shipping.

## Achieved counts and temporal coverage

| App | Selected raw rows | Clean rows | Empty text excluded | Exact duplicates excluded | Source date range |
|---|---:|---:|---:|---:|---|
| Shopee | 782,079 | 781,789 | 287 | 3 | 2015-06-22 to 2023-11-13 |
| Lazada | 775,323 | 774,911 | 396 | 16 | 2013-06-09 to 2023-11-13 |
| Tokopedia | 71,242 | 71,229 | 0 | 13 | 2018-09-12 to 2024-10-25 |
| Bukalapak | 90,147 | 90,127 | 0 | 20 | 2018-09-12 to 2024-10-27 |
| Blibli | 116,902 | 116,883 | 18 | 1 | 2013-12-11 to 2025-02-09 |
| **Total** | **1,835,693** | **1,834,939** | **701** | **53** | **2013-06-09 to 2025-02-09** |

These are cleaning/coverage QA counts, not analytical findings about opinions. There were zero unparseable date strings among retained rows. Repeated short reviews at different dates remain separate records; clean row count is not unique authors, unique buyers, unique transactions or independent experiences.

## Sources and license attribution

1. **bwandowando — Shopee App Reviews from Google Store**: https://www.kaggle.com/datasets/bwandowando/shopee-app-reviews-from-google-store . Original `SHOPEE_REVIEWS.csv`; dataset-declared license **CC BY-NC-SA 4.0**. International app corpus; individual reviewer location and record-level language are not supplied. The dataset card discusses app perception. Images being AI-generated on the card does not mean the reviews are synthetic; those are distinct objects.
2. **bwandowando — Lazada App Reviews from Google Store**: https://www.kaggle.com/datasets/bwandowando/lazada-app-reviews-from-google-store . Original `LAZADA_REVIEWS.csv`; dataset-declared license **CC BY-NC-SA 4.0**. Card states reviews were retrieved using RapidAPI. Individual reviewer geography and record-level language are unavailable.
3. **rezkyyayang — Reviews of Indonesian Startup Apps on Playstore**: https://www.kaggle.com/datasets/rezkyyayang/reviews-of-indonesian-app-startups-on-playstore . Dataset-declared license **CC0: Public Domain**. The curator describes scraping Google Playstore reviews of Indonesian applications. Only `tokopedia.csv`, `bukalapak.csv`, and `blibli.csv` enter the clean corpus. Original archive also contains Dana, Gojek, OVO, Ruangguru and Traveloka; those files remain in the immutable raw archive for integrity but **do not contribute to the reported corpus count**.

License names are reproduced from dataset metadata, not independently adjudicated ownership claims. Retain attribution and the noncommercial/share-alike terms for the two bwandowando sources and their cleaned derivatives. A common ZIP does not replace source-specific licenses with one umbrella license.

## Acquisition procedure

- Kaggle public dataset search endpoint was used for discovery; raw JSON search responses are in `metadata/search_*.json`.
- Dataset detail metadata was obtained through `https://www.kaggle.com/api/v1/datasets/view/{owner}/{slug}` and preserved unchanged or semantically equivalent pretty-printed JSON.
- Public archive bytes were downloaded through `https://www.kaggle.com/api/v1/datasets/download/{owner}/{slug}` with Python standard-library `urllib.request`.
- Three accepted original ZIP archives were retained without altering their contents. The source-manifest records download URL, original compressed bytes, SHA-256 hash, archive member names/sizes, source version and update date where available.
- Downloads used no login cookies, passwords, private APIs, account harvesting or access-control circumvention. Four candidates were downloaded for schema inspection; one was excluded after its metadata/schema showed product rather than app reviews.
- `grikomsn/lazada-indonesian-reviews` was rejected because it is a product-review dataset. Its inspection/download metadata is retained, but the downloaded payload was removed from the delivered accepted raw corpus and no records were cleaned from it.
- `shymammoth/shopee-reviews` was inspected at metadata level but was not downloaded because provenance was insufficient to establish that it was an app-review corpus.

## Cleaning procedure

Raw original archives are immutable. Cleaning reads selected CSV members directly from the ZIP without extracting or overwriting source files.

1. Decode CSV using UTF-8 with optional BOM removal; retain CSV quoted newlines through the parser.
2. Preserve the source dataset/member and zero-based CSV data-row index for every retained record and every exclusion.
3. Normalize review text to Unicode NFC.
4. Replace selected ASCII control characters with a space and collapse whitespace runs into a single space; trim outer whitespace. Preserve case, punctuation, slang, emoji and original language. Do not stem, translate, rewrite, classify, strip URLs or infer intent.
5. Exclude only empty text and literal null-like text values (`null`, `nan`, `none` after casefolding).
6. Deduplicate using exact `app platform + source date string + source rating string + normalized review text`, hashed SHA-256. This is conservative exact-record deduplication. It does not assert that near-identical reviews come from the same person, and it does not collapse matching reviews across different apps.
7. Parse dates with Python ISO datetime parsing solely for a `published_date` field and coverage checks. Preserve the original date string. The bwandowando field explicitly contains UTC; multiapp source timestamps lack an offset, so their timezone remains **unknown**, rather than silently assuming UTC or WIB.
8. Parse integer ratings/helpful-vote counts when possible. Preserve native rating information without treating rating as verified sentiment.
9. Exclude author display names and author identifiers from the clean schema. Raw archives retain the source's original fields. Per-review language, reviewer location and user role remain null/unknown; no attributes are inferred from app country or review language.
10. Export UTF-8 newline-delimited JSON and compress as `clean/app_reviews.jsonl.gz`. Every row contains provenance fields. `clean/exclusions.jsonl` records only excluded row locators/reasons; original source data can be inspected in the raw archive.

There is no native platform review ID in the selected exports that can be reliably used as a review key. CSV `id`/unnamed index columns and masked author IDs are not relabeled as native review IDs. Dataset/source-row IDs are synthetic **record locators**, not synthetic reviews.

## Clean schema

| Field | Meaning |
|---|---|
| `record_id` | Dataset-specific source-row locator |
| `source_id`, `source_url` | Source registry key and public dataset page |
| `source_archive_member`, `source_row_index` | Exact raw member and zero-based data-row locator |
| `native_review_id` | Null: no reliable native ID supplied |
| `collection_stratum` | `supplementary_public_app_reviews` |
| `record_type` | `google_play_app_review` |
| `platform_discussed` | App associated with the source CSV; not a text-inferred opinion target |
| `published_at_source`, `published_date`, `source_timezone` | Original timestamp, parsed calendar date, explicit/unknown timezone |
| `text` | Normalized review text; original bytes retained in raw archive |
| `rating`, `helpful_votes`, `app_version` | Source fields, parsed where appropriate; null if unavailable |
| `language`, `reviewer_country` | Null: not supplied per record |
| `geography_note` | Dataset context with reviewer-location limitation |
| `license_declared_by_dataset` | Source-specific license metadata |
| `text_sha256`, `dedup_key_sha256` | Text integrity and exact-dedup hashes |
| `collection_mode` | `downloaded_existing_public_dataset` |
| `nexora_data` | False |
| `sentiment_or_topic_analysis_performed` | False |

## Known limitations

- Public app reviewers are self-selected. The source collectors' query language, country configuration, sorting, sampling and completeness are not fully documented. These exports cannot be treated as random app-user samples or full review histories.
- Shopee and Lazada exports end in November 2023. They are historical mechanism-reference material, not a measurement of current 2025-2026 policy reactions.
- Tokopedia/Bukalapak end in October 2024; Blibli ends in February 2025. Cross-app historical coverage differs substantially.
- The mixed-source selection is not comparable in platform market share, review generation propensity or user population.
- Dates and star ratings are inherited source fields. The pipeline validates parseability, not the truth of experiences or the integrity of the source collector.
- No language filtering was performed; the two international corpora may be multilingual. The Indonesian-app dataset describes its apps' market context, not individual user geolocation.
- Exact-deduplication cannot detect edited, syndicated or paraphrased reviews reliably. No author-level independence claim is made.
- Raw archives may contain public display names and text personal details. Clean schema drops direct author fields, but does not claim comprehensive personal-information redaction of free text.
- No analytical themes, sentiment estimates, platform rankings, sampling weights, causal effects or Nexora-specific findings are produced.

## Reproduction

From the delivered ZIP root, run `python datasets/app_reviews/scripts/collect.py`, then `python datasets/app_reviews/scripts/clean.py`, then `python datasets/app_reviews/scripts/finalize.py`. Python standard-library modules suffice. Each script resolves the source-stratum base directory from its own file location (`Path(__file__).resolve().parents[1]`), so the folder can be moved without editing paths. If this stratum is distributed separately, use its actual relative path to the same scripts. Public endpoints and dataset latest versions may change, so use saved version metadata, hashes and original archives to reproduce this exact snapshot. A download of `latest` later is not automatically the same source version.

`source_manifest.json` and `metadata/cleaning_counts.json` are the machine-readable count/provenance records. The root package may add its own higher-level inventory without changing this source stratum's identity or counts.

## Validation completed

The compressed clean stream was decompressed fully and passed gzip integrity checking; its line count is exactly 1,834,939. 193 JSON/schema spotchecks across the stream passed. All three accepted raw archives were rehashed and matched saved SHA-256 values. These are file/data-preparation checks, not validation of reviewer statements. See `metadata/validation.json`.
