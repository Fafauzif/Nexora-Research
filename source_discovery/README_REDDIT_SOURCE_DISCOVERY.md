# Reddit source discovery — excluded candidate inventory

No row-level Reddit text or metadata from the datasets assessed here is incorporated into the delivered corpus. These files document source discovery and exclusion decisions only. Their QC counts must not be added to delivered-record counts.

## Assessed sources

1. **bwandowando/reddit-rindonesia-subreddit-dataset-2026** (Kaggle), snapshot283, updated2026-10-23. Metadata lists Reddit API Terms rather than a clear open redistribution license. A public unauthenticated individual-file request retrieved `indonesia_subreddit_comments.csv` (303,257,437 bytes; SHA-256 in receipt). Local screening found809,078 source rows and4,013 rows matching broad e-commerce/platform/shipping terms, representing3,998 unique archive IDs. These counts are screening diagnostics only. Quality inspection revealed comment/thread/parent identifiers are pseudonymous UUIDs, not valid live Reddit IDs, and no original permalink field exists. Therefore metadata-only rows could not provide useful live discovery leads. Source bodies and usernames were never exported; the downloaded source and all derived row-level metadata are excluded/deleted after checking.
2. **bwandowando/reddit-rindonesia-subreddit-dataset** (Kaggle), roughly5GB broad archive, also labeled Reddit API Terms. Not downloaded: scope and redistribution uncertainty did not justify ingestion.
3. **w11wo/reddit_indonesia_sarcastic** (HuggingFace). Dataset card declares Apache2.0; approximately14k selected comments from2020–2023 are designed for sarcasm detection, not broad contemporary e-commerce listening. Metadata inspected, content not downloaded or incorporated.

## Preserved evidence

- Kaggle dataset-view and first files-list metadata responses.
- Download receipt containing public source request, size and original hash.
- Source candidate inventory with inclusion/exclusion status.
- Screening summary (QC counts and regexes, no body text).
- Reproduction scripts demonstrating how the candidate was downloaded and screened. These are audit scripts, not a request to distribute the source content. Code was revised after QA to recognize UUID identifiers and avoid fabricating live Reddit URLs; no such reconstructed URLs are retained in the final files.

No user login, cookie copying, proxies, CAPTCHA handling or access-control bypass was used. Searches also found product-review corpora, which were handed to the separate app-review collection task rather than duplicated here.

## Method summary

Source discovery used public HuggingFace/Kaggle metadata APIs and search-engine discovery. Queries targeted Reddit/e-commerce, Indonesian marketplace names and specific commerce communities. The source CSV was streamed with Python `csv.DictReader`. Local keyword screening used platform aliases, online-shopping terms and shipping terms; mechanical matches were never interpreted as validated relevance or analytical findings. Duplicate IDs were tracked mechanically. Source `created_utc` strings were parsed as UTC because the source field explicitly labels UTC; no individual location or role inference occurred.

The final source inventory, not the excluded candidate records, is the deliverable of this task. It documents an important coverage gap: a large downloadable archive was found, but its terms and pseudonymous IDs made it unsuitable for the requested traceable full-text collection.
