# X/Twitter clean data dictionary

## Files and units

- `clean/twcs_ecommerce_connected_clean.csv.gz`: UTF8 CSV, one source tweet per row, 513,077 records. No dataframe or decompression library beyond Python stdlib is required: `gzip.open(path,'rt')` + `csv.DictReader`.
- `clean/zenodo_ecommerce_twitter_clean.csv` and matching `.jsonl`: **two formats of the same949 clean records**, not additional records. The CSV has the union of optional fields; missing source fields remain blank. Do not count CSV and JSONL twice.
- TWCS individual tweet, connected conversation and unique text counts are separate measures. Customer identity is not verified; one person may have multiple tweets, and company replies are part of the count.

## Common fields

| Field | Type | Meaning |
|---|---|---|
| record_id | string | Stable source-prefixed ID generated for this collection |
| source_id | string | Published source dataset identifier |
| source_record_id | string | Source surrogate tweet ID or PDF file/page/row locator |
| source_url | URL | Source dataset record, not an invented live tweet link |
| source_platform | string | Twitter/X as attributed by source |
| record_type | string | Tweet or tweet extracted from published PDF |
| stratum | string | Historical international core/retail context or multilingual Zenodo sample; not a topic finding |
| country | string | Unknown unless explicitly supplied; currently unknown |
| geography_basis | string | Why geography is not inferred |
| created_at_utc | string | Per-row parsed timestamp or date. Date-only PDF rows lack time-of-day/timezone. Source publication year is different. |
| retrieval_method | string | Published-source import and scope selection route; never live Agent Reach scraping |
| source_license | string | License metadata reported by original repository |
| text | string | Cleaned text with original meaning preserved as far as machine transformations allow |
| text_sha256 | string | SHA256 of Unicode clean text after **casefolding**, encodedUTF8; source-specific rule may differ from other corpora in the overall package |
| cleaning_flags | pipe-separated string | Processing/quality flags; no sentiment or behavioral conclusions |

## TWCS additional fields

| Field | Meaning |
|---|---|
| language | `und`: individual language was not classified |
| language_basis | Original corpus described as predominantlyEnglish but contains other languages |
| author_id_source | Source author handle for company, numeric anonymized/source customer author ID otherwise; no identity enrichment |
| author_role | `company_support` for chosen corporate handle; `customer_or_other_inbound` means source inbound=True, not verified identity; other participants may occur |
| inbound_as_reported | Exact source `True` / `False` direction flag |
| conversation_id | Source-reply-graph connected-component ID, not guaranteed independent customer/issue |
| company_handles | One or more seed companies whose reply components contain this tweet |
| company_types | One or more of `marketplace`, `courier`, `retail_adjacent`; does not say every tweet discusses that company's core service |
| response_record_ids | Original comma-separated reply IDs; may refer to records not present in published source |
| in_response_to_record_id | Original parent source ID; may be missing from published source |
| source_year | Dataset publication/update year2017, **not a claim all tweets were posted in2017** |

Company count by component is nonadditive if two selected handles share a conversation. Use `stratum` for additive coarse slices or define an explicit multibrand counting convention. The source's numeric tweet IDs cannot be inserted into an X status URL.

## Zenodo additional fields

- `source_page` / `source_file`: physical PDF page and filename for auditing extraction. Not supplied for originalCSV rows.
- `source_language`: original CSV language code, unchanged, not proof of country. Original code `in` means the source reports an Indonesian language classification, not that residence was verified.
- `tweet_url_reported`: URL as supplied. Some contain `/undefined/`; no claim that they work or were hydrated.
- Original raw PDFs/CSV and page extractions preserve source text. Existing mojibake/ligature artifacts are flagged rather than silently repaired.

## Reproduction

Delivered scripts run relative to their parent folder. Run `python scripts/collect.py` from any working directory to re-download the public originals into the folder's`raw/` and metadata; this also obtains the omitted multi-industry TWCS intermediate ZIP. Then run `python scripts/process_twcs.py` and `python scripts/process_zenodo.py`; reconstructed outputs are written into a new `ready/` subfolder to avoid silently replacing this package. PyMuPDF is required for the PDF parser. Python stdlib is sufficient for TWCS. Reproduction assumes the same source versions and validates against recorded source fingerprints. The scripts do not log in or scrape live X.
