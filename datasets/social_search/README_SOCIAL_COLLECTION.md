# Social access pilot and public-index collection

## Scope and actual result

This is a bounded public-index discovery collection for indirect benchmarking of mechanisms relevant to the fictional Nexora case: fees, seller economics, vouchers, shipping, switching, discovery, marketplace usability and reasons participants stay. It is **not a complete Reddit/X scrape**. After initial direct-access failures, Agent Reach 1.6 was executed successfully using its explicit **public-web backend only**. No accounts, cookies, credentials, DMs or private groups were accessed.

The first discovery stream used the web-search service: 248 search-result appearances were normalized to **202 unique indexed source records: 163 Reddit thread excerpts and 39 X indexed URLs/short headings**. Of these, 117 are from Indonesian-context Reddit forums; 85 are international-comparator or unverified-context records. Forum context does not establish an author's nationality, location, role, or transaction history. Seven additional partial Reddit page-read representations are included as supporting context, not seven new independent conversations and not a full comment export.

A second, actual Agent Reach run executed 32 Reddit public-web queries (10 results each) and 3 X public-web access probes. With the root pilot included, 330 Reddit item appearances normalized to **251 unique indexed Reddit source records**. X returned no source items through Agent Reach. Across both discovery streams, the URL registry has **415 unique source URLs: 376 Reddit threads and 39 indexed X URLs**, with 38 URLs rediscovered in both streams. These are partial indexed excerpts/metadata, not full posts or complete comment datasets.

Counts describe files and record units only. No sentiment, substantive coding, causal analysis or findings were produced. Candidate relevance needs future human screening: broad retrieval includes noise and tangential discussions.

## Files

- `agentreach_raw/*.stdout.json`: exact Agent Reach JSON envelopes; paired stderr files preserve execution diagnostics. Explicit backend was `public-web`. Root pilot raw files remain under `../tooling/` and are referenced, not duplicated.
- `agentreach_clean/agentreach_publicweb_records.jsonl` and `.csv`: deduplicated Agent Reach source records, preserving scope and completeness flags, source dates where returned, and occurrence provenance.
- `logs/agentreach_queries.jsonl`: every executed command, query theme, start/end, status and returned item count.
- `logs/agentreach_inventory.json`: technical Agent Reach counts.
- `clean/social_source_url_registry.csv`: cross-stream URL registry; do not add stream record counts as independent conversations.
- `logs/cross_stream_inventory.json`: URL-level union and overlap counts.

- `raw/search_001.json` through `raw/search_008.json`: captured Reddit search excerpts (as returned) and indexed X metadata/short headings. They preserve source refs, original URL, capture file and retrieval representation. These are raw captured representations, not source-platform JSON exports.
- `raw/thread_reads_001.json`: seven partial Reddit indexed-page reads. The provider selects ranges; neither completeness nor full comment pagination is claimed.
- `raw/access_test_*.txt`: response bodies from direct endpoint checks. Some are application/challenge shells, not social data.
- `raw/arctic_api_README.md`: retrieved documentation for the independent Arctic Shift archive API; documentation is not collected social content.
- `clean/social_index_records.jsonl` and `.csv`: one deduplicated record per canonical source URL.
- `clean/reddit_thread_read_excerpts.jsonl` and `.csv`: supporting partial page reads, linked by canonical thread URL.
- `logs/access_tests.json`: direct connectivity checks.
- `logs/query_log.json`: discovery query batches, exact queries and known retrieval limits.
- `logs/collection_inventory.json`: technical row/unit counts.
- `scripts/normalize_collection.py`: repeatable cleanup and inventory script.

## Access outcomes and collection constraints

The Agent Reach current documentation states Reddit is an optional login-dependent channel and X is experimental and login-dependent. Those authenticated dependencies were not used. The isolated installed version also supported an explicit public-web backend; only that backend was executed. This distinction resolves the apparent difference between general README access requirements and the actual run. Source version and setup logs are retained by the root agent under `../tooling/`.

Direct access tests:
1. GitHub raw README: HTTP200, readable documentation.
2. Reddit public `search.json`: HTTP403.
3. Reddit public search HTML: HTTP200 but JavaScript challenge shell, not search results.
4. X public search HTML: HTTP200 but logged-out application shell, not tweet records.
5. Arctic Shift documented public post-search endpoint: HTTP403. No archive records obtained.

No challenge solving, restriction bypass, residential proxy, cookie extraction or session reuse was attempted. The successful routes were the available public web-search service and Agent Reach public-web search for Reddit, which surfaced indexed material. Agent Reach public-web X probes returned no usable source items; indexed X URLs/short headings came only from the separate search-service discovery stream. Provider ranking, cache coverage and excerpt selection constrain this collection. Search-index visibility can differ from current platform availability.

## Discovery methodology

### Agent Reach public-web run

`run_agentreach_public.py` uses the isolated executable supplied by the root agent. It forces `--backend public-web`, `--limit 10`, and `--timeout 20`, with two concurrent subprocesses and a 55-second outer timeout. It stops subsequent work if a 429/rate-limit response is seen; no alternate authenticated or browser backend is attempted. 32 query themes cover seller fees, buyer value, switching, logistics, discovery, positive counterexamples and international analogies; three X probes test public discovery. The exact command vectors and raw JSON envelopes are retained.

`normalize_agentreach.py` deduplicates canonical URLs, preserves returned source publication timestamps without fabricating missing ones, hashes author strings into pseudonyms in the clean table, retains raw textual words, and attaches every query occurrence to its retained record. Multiple comments in a returned item remain one thread excerpt. Root pilot provenance is included without copying its raw file. `build_social_registry.py` provides a source-URL union across this and the web-search-service stream.

### Separate web-search-service stream

Eight batches of four queries (32 queries total) covered Indonesian marketplaces and seller/buyer/logistics mechanisms, plus separately retained international analogies. The query log contains the exact query strings. Negative, neutral and positive phrases were included. No claim of balanced or representative sampling follows from this inclusion.

The provider search engines were used for discovery; selected Reddit URLs were opened for contextual page excerpts. Search batches can return results tangential to a query. The record capture preserves that fact instead of silently labeling all results relevant.

There was no date filter applied consistently to all searches. Date references in query strings are not equivalent to strict platform time filters. Therefore this is a mixed-date discovery set. `created_utc` is null: relative Published/Crawled labels are retained as labels and are not converted into invented source timestamps. Later work should validate post dates and split historical versus current evidence.

## Cleaning methodology

1. Parse source headings, URLs and provider references from captured result blocks.
2. Keep Reddit and X domains in this social subset; unrelated news/articles were not redistributed here as raw article text.
3. Canonicalize Reddit URLs to subreddit + post ID, removing translated-view query strings and slug variants. Canonicalize X status URLs to account + status ID where available. Profile-only URLs remain clearly metadata records.
4. Deduplicate records by canonical URL. Retain all capture-file and source-ref appearances and the longest captured Reddit excerpt, rather than counting rediscovery as a new source.
5. Normalize whitespace only. No paraphrasing or translation is applied to captured excerpts.
6. Do not split a multi-comment page excerpt into supposed individual comments when platform comment IDs were not returned. The unit remains an indexed thread excerpt.
7. Retain unknown author location, source publication time and role as unknown rather than infer them from forum or language.
8. Give each canonical record a stable SHA256-derived ID and hash the clean text.
9. Store raw captures separately from normalized CSV/JSONL files. The normalization script reconstructs the normalized files from those captures.

For X, only metadata and a maximum 20-word indexed source heading are retained; no full tweet/thread text was captured. This is deliberate limited source representation, not proof that Agent Reach scraped X. Search-provider wrappers are not a substitute for the original platform record.

## Data interpretation and provenance boundaries

- A Reddit thread excerpt is not a unique respondent or a verified seller.
- Partial page reads may include related-thread widgets and deleted-content markers. Do not code these as thread comments without checking context.
- Forum context, Indonesian language, self-description, engagement and policy claims need independent validation for any later substantive use.
- Source refs are search-tool provenance; canonical URLs are portable source locators.
- This set should not be used to estimate national seller/buyer prevalence or causal effects.
- Search data should be refreshed and underlying URLs checked before quotation in a submission.
- A future authenticated Agent Reach run would be a distinct new source stream with its own version, access, query, export and pagination records.

## Recommended continuation (not performed)

The public-web Agent Reach stream is complete for this bounded run. For any future authenticated collection, first validate access and stable structured exports through the user's chosen authorized platform sessions. If unrestricted scale is unavailable, use a legitimately distributed archive whose provenance and terms can be checked. For massive collections, keep the unscreened raw corpus distinct from the e-commerce-focused clean subset, preserve date/query/pagination boundaries and never count a broad unrelated archive as targeted Nexora evidence. Do not recover intentionally removed or private content.
