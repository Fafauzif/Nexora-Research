# Nexora indirect marketplace-mechanism corpus: collection protocol

**Protocol version:** 1.0  
**Prepared:** 26 October 2026, Asia/Jakarta  
**Status:** Collection specification. Actual availability, executed methods, counts, licensing decisions and failures must be read from the run manifests and collection/cleaning methodology. Planned targets below are not claims of completed collection.  
**Scope of this deliverable:** Raw data, cleaned data, documentation and continuity only. No sentiment results, inferred findings, regressions, causal estimates, strategy evaluation or recommendations are produced in this collection phase.

## 1. Purpose and authority

Nexora is the fictional company in the supplied IBSC 2026 case. Its casebook is the complete supplied internal evidence base. The user explicitly decided that the casebook takes precedence over the guidebook. External records must never be described as Nexora users, transactions, costs, events or internal evidence.

The external corpus is intended to make later original analysis possible around analogous marketplace mechanisms: participant economics, fees, incentives, switching, multi-homing, discovery, seller visibility, logistics, trust, returns and reasons for continued participation. The case question is how to achieve sustainable profitable growth while strengthening competitive position and mitigating seller/buyer attrition in Indonesia.

The user's current instruction is to conduct a broad, large collection run, ideally reaching hundreds of thousands of records, with raw and clean data in a ZIP, collection/cleaning methodology and an updated master context pack. Scale is subordinate to relevance, permitted access, provenance and accurate reporting. A target is not an entitlement to access a platform or a reason to include irrelevant records, duplicate text or synthetic examples. A shortfall must be reported transparently.

## 2. Corpus boundaries and independent units

Maintain separate tables for distinct object types rather than one undifferentiated scrape:

1. **Social records:** Original posts, comments, replies and thread text actually obtained from public Reddit/X content or attributable, reusable datasets.
2. **Search discoveries:** Search result snippets and metadata used to identify candidate records. A snippet is not full retrieved post text and must remain distinguishable.
3. **Official evidence:** Policy announcements, fee tables, eligibility rules, public reports and other authoritative documents that establish an event or benchmark.
4. **Source catalogs:** Dataset cards and landing pages that describe possible sources. A catalog entry is not a social record or a successful download.
5. **Technical records:** Requests, attempts, failures, access tests, manifests, checksums and source-specific cleaning decisions.

One post/comment is one record when it has a stable identifier. One thread is a cluster of related records. One author can contribute several records. One underlying text can appear on several websites. Counts of records, unique texts, unique authors when available, independent conversations and source files must not be treated as equivalent.

Do not declare independence between replies under one viral post, copied cross-posts, syndicated policy announcements or several datasets derived from the same original crawl. Store relationships so later analysis can cluster at conversation, author and source level.

## 3. Geographic and temporal strata

### 3.1 Geographic strata

- `indonesia_confirmed`: Explicit Indonesian marketplace/domain, location, currency/context, or reliable source documentation supports Indonesian relevance.
- `indonesia_probable`: Context is suggestive but incomplete. Document the evidence.
- `international_analogue`: Real non-Indonesian marketplace mechanism relevant to the case; preserve country/market where known.
- `geography_unknown`: Do not force a country assignment.

Language alone does not establish location or nationality. Bahasa Indonesia can occur outside Indonesia, and English can occur within it. Currency or a platform name can support the subject market without establishing the author's residence.

### 3.2 Temporal strata

- `historical_case_context`: 1 January 2023 through 31 December 2025. This covers the case's competitive-share history and 2024–2025 operating comparison.
- `current_benchmark`: 1 January 2026 through the collection cutoff on 26 October 2026, using Asia/Jakarta for user-facing cutoff language and UTC timestamps in data.
- `earlier_mechanism_analogue`: Before 2023, retained only when source relevance, a specific event or a defensible comparable mechanism warrants it.
- `date_unknown`: Preserve records with unknown date without inventing publication dates.

Current 2026 evidence may inform forward-looking feasibility. It cannot retrospectively explain a 2025 result. Retrieval time, publication time, event effective date and source-dataset release date must be separate fields. Preserve original timezone strings; convert to UTC only when parsable and unambiguous. Do not impute midnight or a day/month from partial dates without retaining precision metadata.

## 4. Broad retrieval design

The source priority is: relevant Indonesian public discourse and official documents; documented regional marketplace comparisons; directly relevant international marketplace mechanisms; general retail/social datasets only if they contribute a specific, separately labeled purpose.

Use a broad query matrix across themes, platforms, market relevance, language and time. Do not concentrate every query on "fees caused churn." Search neutral, adverse and favorable accounts; identify reasons people stay as well as leave. Search brand-only and neutral shopping vocabulary in a bounded pilot to discover language that a complaint-driven query list would miss.

The matrix is a retrieval design, not a statistical probability sample. Search ranking, authentication state, query terms, source coverage, platform moderation, deletion, API limits and search history can shape what is returned. Record whether a search was sorted by relevance, recency or another option; preserve unavailable filters as unavailable.

### 4.1 Brand and domain families

Use these as discovery terms, not an asserted mapping of the fictional companies to real firms:

| Stratum | Brand/domain seeds | Notes |
|---|---|---|
| Indonesian marketplace | Shopee; Tokopedia; Lazada; Bukalapak; Blibli | Add spelling and spacing variants found in the pilot. Do not label one as Nexora. |
| Indonesian content commerce | TikTok Shop; TikTok Shop by Tokopedia; shop Tokopedia; keranjang kuning; live shopping | Phrase availability and meaning can vary by date. |
| Logistics | SPX; Shopee Express; J&T; JNE; SiCepat; Anteraja; Pos Indonesia; Ninja Xpress | Disambiguate generic abbreviations and unrelated uses. |
| Regional comparisons | Shopee; Lazada; TikTok Shop in explicitly identified Southeast Asian markets | Retain country/domain; fees and logistics are market-specific. |
| International analogues | Etsy; Amazon Marketplace; eBay; Fiverr | Fiverr is a service-marketplace analogy and must remain distinct from parcel-based e-commerce. |
| Non-platform channels | toko sendiri; website toko; WhatsApp order; Instagram shop; direct purchase | Useful for multi-channel substitution when marketplace context is explicit. |

Do not run every possible Cartesian product if it merely repeats the same results. Log which combinations were attempted and why a query family was revised or stopped.

### 4.2 Mechanism and language matrix

The examples below are search concepts. They are not guaranteed Agent Reach CLI syntax or evidence that an expression has already returned records. Test simple phrases first; add platform-specific operators only after capability verification.

| Theme | Indonesian seeds and variants | English comparison seeds | Neutral / positive counter-search |
|---|---|---|---|
| Seller charges | biaya admin; biaya administrasi; potongan seller; komisi; biaya layanan; biaya per pesanan; biaya proses; biaya affiliate/afiliasi | seller fees; commission; transaction charge; selling costs; effective take rate | biaya sepadan; masih untung; worth the fees; profitable seller |
| Merchant economics | margin; laba; untung tipis; omzet; biaya iklan; boncos; modal; harga pokok; HPP | seller profit; margin squeeze; advertising costs; cost of selling | profitable demand; growing sales; better conversion |
| Buyer promotions | gratis ongkir; bebas ongkir; ongkos kirim; voucher; kupon; cashback; koin; minimum belanja; syarat voucher | free shipping; minimum spend; coupon restrictions; cashback; discount eligibility | voucher berguna; hemat; good value; useful promotion |
| Switching | pindah platform; pindah toko; belanja di tempat lain; berhenti belanja; uninstall; lebih murah di | switched marketplace; moved my shop; stopped buying; alternative platform | tetap pakai; tetap jualan; prefer marketplace; reasons to stay |
| Multi-homing | beberapa marketplace; jualan di dua platform; toko di mana-mana; banding harga; beli langsung | multiple marketplaces; multichannel selling; cross-listing; direct purchase | complementary channels; convenient comparison |
| Discovery | pencarian; cari produk; rekomendasi; live; livestream; kreator; affiliate; keranjang kuning; produk viral | product discovery; live shopping; creator recommendations; search relevance | produk unik; ketemu barang; useful recommendation |
| Seller visibility | toko sepi; jualan sepi; iklan seller; produk tenggelam; traffic toko; susah muncul | organic visibility; sponsored listings; seller ads; traffic decline | improved visibility; organic orders; repeat customers |
| Delivery allocation | pilihan kurir; kurir otomatis; tidak bisa pilih kurir; pickup; jemput paket | courier choice; assigned courier; in-house delivery; seller pickup | reliable pickup; flexible shipping; faster delivery |
| Fulfillment failures | telat; terlambat; nyangkut; gagal antar; paket rusak; hilang; salah alamat | late parcel; failed delivery; damaged package; lost shipment | tepat waktu; paket aman; resolved delivery |
| Reverse logistics | retur; pengembalian; refund; dana kembali; komplain; sengketa; klaim | returns; refunds; claims; dispute resolution | refund cepat; solved complaint; good support |
| Trust and quality | barang palsu; tidak sesuai; penipuan; rating; review; garansi | authenticity; not as described; trust; counterfeit; buyer protection | barang sesuai; trusted seller; reliable marketplace |
| Working capital | pencairan dana; saldo tertahan; dana ditahan; pembayaran seller | settlement delay; funds on hold; reserve; seller cash flow | fast settlement; predictable payout |
| Product/basket economics | harga murah; barang kecil; berat; ongkir lebih mahal dari barang; gabung pesanan | low basket value; shipping more than item; split shipments; bundling | minimum order useful; combined shipping savings |
| Platform value | pelanggan; pembeli; jangkauan; kemudahan; perlindungan; kepercayaan | qualified demand; convenience; reach; protection; customer acquisition | tetap bayar; worth paying; saves time |

For exploratory international work, prioritize English plus the original language actually supplied by an accessible source. Do not invent translations or claim multilingual coverage from a query list alone. Preserve original text and language uncertainty. Translation, if later performed, must be stored in a separate derived field with method/version.

## 5. Acquisition routes and feasibility checks

### 5.1 Agent Reach route

Before scale-up, verify the installed version, available channels, actual action names, output schema, authentication requirements and pagination behavior. Repository documentation is a capability claim; an executed retrieval is evidence of access. Do not fabricate command flags from examples or report a channel as tested merely because its documentation was read.

The proposed social route is read-only. Obtain posts and contextual replies without posting, liking, messaging or interacting with users. Do not scan browser profiles or copy authentication cookies implicitly. Authentication, if required, must use the supported account-selection and login route; credentials and session tokens never belong in the corpus.

The actual run may instead use accessible public source datasets, official exports or search-discovery records. Record the implemented route per source. If Reddit/X channels cannot run in the execution environment, state it directly and preserve attempted access logs. Search snippets and public datasets are distinct substitutions, not a successful live Agent Reach scrape.

### 5.2 Public research-dataset route

Inspect each candidate dataset card or original publication for platform identity, provenance, population, date range, geography, fields, source size, reuse conditions and access method. Retain its original downloaded archive/files and a checksum when redistribution is supported. Avoid generic sentiment corpora unrelated to commerce merely to meet a row target.

A candidate source can be:

- accepted as relevant social text;
- accepted as a separately labeled adjacent benchmark;
- cataloged but not downloaded;
- downloaded but excluded from the cleaned corpus;
- blocked by authentication/access;
- excluded for insufficient provenance or incompatible redistribution conditions.

Record the reason. Do not treat availability on a mirror as proof of its original origin or reuse status. Do not call a dataset "Twitter" or "Reddit" unless its documentation supports that attribution. App-store reviews, product reviews and transaction records must be labeled as their actual source types.

### 5.3 Search discovery and official evidence

Search can identify public discussions and policy-event sources. Capture queries and returned locators; retrieve full records when possible. If only a snippet is available, set `text_completeness=search_snippet` and exclude it from counts of fully retrieved social records. Do not stitch snippets into a purported full post or infer missing reply text.

Official evidence should preserve policy effective dates and scope. A help-center page retrieved today may reflect a new version; it is not automatically evidence of historical policy. An archived capture must retain archive/capture metadata separately from original publication metadata.

### 5.4 Respect source access boundaries

Use documented public downloads, permitted APIs, ordinary accessible pages or authorized sessions. Do not bypass authentication, paywalls, access denial, rate limits or CAPTCHA controls. When blocked, record the block and switch to a legitimate alternative or mark the dependency unresolved. Repeated rotating-identity attempts are not part of this protocol.

## 6. Pilot and stopping rules

### 6.1 Access pilot

For each route, test a small number of records, one search, one full record and a thread/comment retrieval if supported. Check that URL, ID, text, date and pagination can actually be preserved. Detect whether output is full text, metadata or a snippet. Record elapsed time, HTTP/tool errors and limitations without storing secrets.

### 6.2 Relevance pilot

Inspect a bounded sample from the main query families. Include ambiguous abbreviations, neutral expressions, positive experiences and international sources. Identify obvious irrelevant vocabulary, spam, product ads and customer-service boilerplate. Refine query families and deterministic eligibility rules before a larger pass. Record protocol changes and their effect on which records can be captured; do not retrospectively present a revised scheme as preregistered.

### 6.3 Scale-up

Partition source work by query family, date windows or independent source files with stable task IDs. Resume from logged cursors/checkpoints where supported. Save each source batch before attempting the next dependent step. Do not append a completed batch again after a restart. Deduplicate after acquisition using stable source identifiers and source-text fingerprints.

The aspirational scale is hundreds of thousands of eligible records if accessible. Final reporting must separately state original downloaded rows, parseable rows, eligible rows, duplicate rows, excluded rows, unique cleaned rows and full-text versus snippet counts. Never count the same full corpus twice because it is offered as both CSV and JSONL.

### 6.4 Stop or narrow when

- Source access is denied, requires unavailable authentication or returns repeated documented errors.
- Incremental pages repeat previous IDs or pagination no longer advances.
- Additional queries predominantly yield unrelated or duplicate material.
- A source's identity or reuse conditions cannot be established sufficiently for inclusion.
- Remaining source size exceeds the practical run budget without a reasonable relevance payoff.

Log the stop reason. A bounded relevant corpus with honest coverage is preferable to a padded large one.

## 7. Canonical record schema

Raw files preserve their original source format. A canonical cleaned social table should use nullable fields rather than inventing unavailable metadata. Source-specific extra fields can be retained in a separate namespaced JSON object.

| Field | Type / rule |
|---|---|
| `record_id` | Stable canonical ID; deterministic namespace + source ID, otherwise clearly marked deterministic content-based ID |
| `source_id` | Key to source register |
| `source_record_id` | Original platform/dataset identifier when available; retain as text to avoid numeric precision loss |
| `source_platform` | Actual platform or `unknown`; never infer from a filename alone |
| `source_type` | Reddit post/comment; X post/reply; app review; product review; search snippet; official document; other specified type |
| `source_url` | Canonical public record locator when available |
| `raw_file` / `raw_locator` | Relative file plus line, row, JSON path or archive member needed to recover raw input |
| `retrieval_method` | Executed route, not intended route |
| `query_id` / `batch_id` | Search/batch provenance; many-to-many query matches may live in a link table |
| `published_at_original` | Unchanged source timestamp string |
| `published_at_utc` | Parsed UTC value only if justified |
| `date_precision` | exact timestamp; day; month; year; unknown |
| `collected_at_utc` | Actual acquisition timestamp |
| `parent_id` / `thread_id` | Original or namespaced relationship; nullable |
| `author_id_hash` | Optional stable source-scoped pseudonymous identifier; no inferred real identity |
| `title_original` | Original title where applicable |
| `text_original` | Unaltered decoded source text |
| `text_clean` | Deterministically normalized text; no translation or meaning rewrite |
| `text_completeness` | full; source-truncated; search_snippet; metadata_only; unknown |
| `language` / `language_method` | Supplied or detected value and method; distinguish mixed/unknown |
| `subject_market` / `geography_status` | What market the content concerns, with explicit/probable/unknown evidence |
| `temporal_stratum` | historical_case_context; current_benchmark; earlier_mechanism_analogue; date_unknown |
| `brand_matches` / `term_matches` | Deterministic matched vocabulary for retrieval/relevance; not sentiment findings |
| `eligibility_status` / `exclusion_reason` | Included/excluded/quarantined plus explicit rule |
| `duplicate_group_id` | Stable exact-text or identifier duplicate relationship; nullable |
| `raw_text_sha256` / `clean_text_sha256` | Integrity and dedup support |
| `license_or_terms_ref` | Source-register reference; not a guessed blanket license |

Do not force every canonical row into every metadata field. Missing ratings, engagement, author location, product category, seller status or source URL remain missing. If a source contains only text and labels, do not synthesize post IDs, real URLs, dates or identities. A deterministic local ID must be visibly local.

## 8. Cleaning protocol

Cleaning is data preparation, not an analysis of findings. Preserve a versioned script/config and source-specific mapping. Run deterministic transformations; retain intermediate audit counts.

### 8.1 Intake and decoding

1. Record original filename, byte size, download route, content type and SHA-256.
2. Verify actual file type instead of trusting suffixes. Detect HTML access-denial/login pages saved with a data extension.
3. Parse the source format using explicit encoding and schema. Log invalid rows and archive-member errors.
4. Preserve the raw artifact unchanged. Never overwrite raw text with a cleaned or translated version.
5. Keep parse failures and source notices in quarantine with enough provenance to reproduce the failure.

### 8.2 Text normalization

- Normalize line endings and Unicode using a documented form, ordinarily NFC.
- Decode HTML entities once where the source genuinely encodes them; do not render or execute embedded content.
- Remove markup only with an explicit source-specific rule while retaining meaningful links, mentions, emojis and punctuation in the original field.
- Trim leading/trailing whitespace and collapse excessive horizontal whitespace in `text_clean` without changing word order.
- Preserve Indonesian slang, negation, spelling, emojis, code-switching and sarcasm cues. Do not stem, translate, spell-correct, lowercase irreversibly or remove stopwords in the canonical clean text.
- Do not remove price, percentage or date expressions merely because they look like noise.
- Represent deleted/removed/source-empty records explicitly; do not replace them with inferred text.

A separate comparison-normalized string may be lowercased and whitespace-normalized for fingerprints. It must not replace the readable text.

### 8.3 Eligibility screening

A core social record needs evidence of marketplace/e-commerce relevance, not merely a positive/negative sentiment label. Brand-only product advertisements and unrelated uses of generic terms should be excluded or assigned a separate adjacent stratum.

Suggested exclusion reasons are `unrelated_topic`, `commercial_promotion_only`, `customer_service_boilerplate_only`, `empty_or_deleted`, `metadata_only`, `search_snippet_only_for_core_corpus`, `unparseable`, `duplicate_id`, `duplicate_text`, `source_provenance_insufficient`, `future_date_or_date_error`, and `source_specific_rule`.

Use deterministic keyword relevance as an initial broad screen if practical, then clearly label its limits. A keyword match is not a human-validated mechanism classification. If manual review is performed, record the reviewed sample, reviewer and actual decisions. Do not claim all rows were manually checked.

### 8.4 Deduplication

Use layered rules and retain the duplicate map:

1. Exact stable ID within source/platform.
2. Cross-source match of stable platform IDs or canonical URLs.
3. Exact normalized text with contextual checks; very short generic text can recur legitimately and should not automatically be treated as the same event.
4. Near-duplicate or cross-post similarity only if implemented and documented. Store the similarity rule and threshold; do not claim it happened if only exact deduplication ran.

Retain one canonical representative in the analysis-ready table and preserve all raw origins and retrieval-query matches in provenance/link tables. Do not merge two different comments solely because they express the same idea. Reposts, quoted text and replies should retain source/context relationships where known.

### 8.5 Dates, geography and identifiers

Parse timestamps conservatively. Reject or quarantine impossible dates without silently coercing them into a valid period. Do not infer author location from text language. Keep all platform IDs as strings. Preserve source-specific units and original labels. Set absent optional fields to null, not fabricated zero values.

### 8.6 Sensitive and irrelevant fields

Exclude authentication material, cookies, keys, hidden session metadata and private messages from every output. Do not enrich public posts with real identities or unrelated profile details. Source-provided names/handles are not required in the canonical analytical table; retain source locators for verification and use pseudonymous IDs when author grouping is needed. Any redaction of raw material must be documented transparently as a redacted preservation copy rather than described as byte-identical raw data.

## 9. Quality assurance and reproducibility

Required checks, reported only if actually executed:

- SHA-256 matches for packaged raw and clean files.
- All source IDs resolve to the source register.
- All cleaned rows link to an existing raw locator or documented transformation source.
- Canonical IDs are unique; duplicates are accounted for.
- JSONL parses or CSV/parquet schema validates without silent truncation.
- Text columns remain text; identifiers are not corrupted by spreadsheet numeric conversion.
- Null counts and parse-error counts reconcile with source mappings.
- Row flow reconciles: input → parseable → screened → duplicate disposition → final cleaned corpus, with order of operations explicit.
- Full-text, snippet, official-document and catalog counts remain separate.
- Platform attribution and geography/date precision are not upgraded during normalization.
- A bounded sample of start/middle/end records and edge cases is inspected for mapping/encoding correctness, with actual review scope logged.
- Re-running cleaning against identical raw files/config produces the same cleaned hashes, or explains non-deterministic fields separately.

Quality-control counts and exclusion summaries are permitted in this phase because they describe preparation, not substantive social-listening findings. No sentiment distribution, theme prevalence or business conclusion is necessary to validate the corpus.

## 10. Collection and cleaning documentation

The final methodology should distinguish **planned**, **executed**, **blocked** and **not attempted** tasks. It must name exact source versions and methods, collection cutoff, source/date/geography limits, deduplication order, keyword dictionaries, cleaning transformations, validation scope, counts and unresolved dependencies.

A request log should contain `attempt_id`, `task_id`, source, method, query/filter, requested window, timestamp, status, returned/accepted counts when known, cursor/page metadata, error category, stop reason and output file. Redact ephemeral credentials and signed token parameters. Do not expose a success claim on the basis of a landing-page fetch or a catalog search.

Recommended package layout:

```text
README.md
raw/<source_id>/<original_source_files>
clean/<source_id>/<clean_files>
clean/combined_<clearly_defined_scope>.jsonl-or-csv
provenance/source_register.csv
provenance/file_manifest.csv
provenance/retrieval_log.jsonl
provenance/row_lineage-or-source_mapping.csv
provenance/duplicate_map.csv
provenance/exclusions.csv-or-summary.json
documentation/COLLECTION_PROTOCOL.md
documentation/METHODOLOGY_COLLECTION_AND_CLEANING.md
documentation/DATA_DICTIONARY.md
documentation/LIMITATIONS_AND_ACCESS.md
scripts/<reproducible_collect_and_clean_scripts>
config/<query_matrix_and_cleaning_configuration>
checks/<validation_results_and_checksums>
```

Adapt filenames to actual outputs; do not ship empty files that imply nonexistent collection. If raw sources are compressed, document how to extract and locate records. If a source cannot be redistributed, package its metadata, acquisition instructions and allowed derived material rather than pretending raw bytes are included.

The updated master context pack is a separate requested deliverable. It should record the complete source/history context, the user's explicit fictional-case correction, the casebook-precedence decision, the new collection scope and actual run results without adding substantive analysis. Root is responsible for integrating and saving final deliverables.

## 11. Interpretation boundary for future analysis

This corpus is an external, non-probability evidence base. Later users may investigate patterns, develop coding, examine counterexamples and compare mechanisms. They must not describe corpus proportions as market prevalence, call self-reported intentions observed churn, identify social posters as Nexora users, estimate Nexora's causal effects from public discussion, equate a surge in posts with a surge in incident rates, or transfer foreign effect sizes directly into financial forecasts.

Do not use post volume, upvotes, likes, views or query result counts as a direct market-size denominator. Engagement metrics change with collection time and ranking. Report "within the collected records" and retain the source/cluster/date boundaries. External voices can inform mechanism plausibility and strategy design; the official casebook remains the evidence for what happens to Nexora.

## 12. Completion definition

A successful collection deliverable contains the actual obtainable corpus, unchanged raw sources where permitted, prepared cleaned records, honest count reconciliation, reproducible scripts/configuration, clear access-failure records, source-level provenance, methodology and the updated context. A six-figure record count is achieved only if validated eligible records actually reach it; otherwise state the true result and the exact route needed to expand further.

**No substantive analysis is included in this phase.**
