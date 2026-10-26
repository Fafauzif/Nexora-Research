# Methodology — actual collection and cleaning

## 1. Research contract

The user requested a broad external-data run, ideally hundreds of thousands of observations, raw and cleaned outputs, collection/cleaning documentation, a ZIP, an updated master context and parallel subagents. The user explicitly requested **no analysis yet**. Nexora is fictional; its only supplied internal information is the casebook. The casebook takes precedence over the guidebook. External data support indirect benchmarking of mechanisms, not company-specific measurement.

The six mechanism families guiding source discovery were seller economic burden; buyer subsidies/delivered value; switching and multi-homing; delivery reliability/control; discovery/visibility; and reasons participants stay. Neutral, positive and contradictory experiences were intentionally eligible. Those families guided searches and source scope, but no per-record thematic or sentiment classification was performed in this run.

## 2. Parallel execution and acquisition routes

Separate subagents handled public social access and query expansion, Reddit dataset discovery, published Twitter dataset acquisition, supplementary app-review acquisition, protocol/context documentation and independent QA. The root agent inspected and installed an isolated Agent Reach package, ran public-only pilots, reconciled outputs, assembled documentation/context, validated the ZIP and saved deliverables.

### 2.1 Agent Reach — actually executed, bounded public route

Agent Reach was cloned from its GitHub repository and installed in a task-local virtual environment. The checked-out source commit is recorded in `tooling/AGENT_REACH_PROVENANCE.json`; version output is also included. No global tool/browser setup or account login was performed.

The selected explicit backend was `public-web`. This route delegates scoped discovery/read to a public search/page provider. It is not the authenticated Reddit/X site browser backend. Exact commands, result envelopes, timestamps, successes, failures and completeness flags are preserved. Reddit searches returned indexed material. X public-only probes did not establish complete site access. No Reddit or X credentials, browser cookies, profiles, private messages or accounts were harvested.

A direct Reddit anonymous JSON test returned 403; direct HTML responses included access/challenge material, and the X direct probe returned a logged-out shell rather than a tweet export. These are recorded as route-specific access failures, not proof that all public access is impossible. No challenge-solving or access-control bypass was used. A public archive endpoint also returned 403; no proxy bypass was attempted.

### 2.2 Built-in public web search and partial thread reads

A separate search route discovered publicly indexed Reddit/X links and text. Source-scoped captured excerpts, queries, partial page reads and normalized records are retained. These built-in-search capture files are curated raw-layer extracts, not byte-identical full provider responses; the actual Agent Reach JSON envelopes are separately retained unchanged. This route must not be credited to Agent Reach. Result snippets, page text, post-level entries and search appearances are distinct units. A single result may contain excerpts from several comments without reliable individual comment IDs. Such material is not split into invented independent commenter records.

Search retrieval is bounded and relevance-ranked. It is not a complete historical firehose, random sample or authoritative all-comments export. Where an exact source post date was unavailable, date quality remains marked unknown or approximate. Search summaries are not treated as verified user statements.

### 2.3 Published Twitter research data

A large licensed historical support corpus was acquired from Thoughtvector's original Kaggle dataset. The complete original source contained 2,811,774 source tweet rows. For this package, a reproducible graph filter retained complete connected reply components that included specified marketplace, courier or adjacent retail support accounts. Selected original rows are preserved unchanged as a **source-scoped raw subset**; this is not represented as the full original dataset.

The original downloaded archive URL, version, byte count and SHA-256 are recorded. The full unrelated source archive is not packaged; original selected row fields and context are. The scoped archive includes company responses as well as customer messages. Core marketplace/courier and adjacent retailer strata remain distinguishable. Source surrogate numeric tweet IDs are not relabeled as genuine live X status IDs. There are no fabricated status permalinks.

The dataset snapshot is from 2017, but some connected historical tweets are older. Use actual per-record dates and the recorded minimum/maximum rather than assuming every record was authored in 2017.

Two smaller Zenodo sources were also downloaded under their declared licenses. Original PDFs/CSV and page-level text extraction are retained. The PDFs were parsed conservatively using date-delimited reading order; page/row source locators remain available. Source titles and legacy research labels are not treated as verified topical eligibility or a newly computed label. Mixed-language, promotional and encoding-affected records remain visible and qualified. No claims of a representative Indonesian sample or verified seller role were added.

### 2.4 Supplementary marketplace-app reviews

Three public source ZIP archives were preserved byte-for-byte. Selected members cover Shopee, Lazada, Tokopedia, Bukalapak and Blibli. These are **Google Play app reviews**, not product reviews and not Reddit/X. A candidate discovered to contain product reviews was excluded; its rejection metadata remains for audit.

The original multiapp archive includes unrelated applications. Those members remain in the immutable original raw archive for source integrity, but **do not contribute to the clean corpus or reported selected-row counts**. Only the five specified e-commerce-app members enter the clean corpus.

The largest Shopee/Lazada exports are historically bounded and do not disclose individual reviewer geography or language. The other curator describes Indonesian applications; that describes the application context, not every reviewer's location. No geographic or role attributes were inferred merely from text language, app brand or platform country.

### 2.5 Excluded Reddit archive

A large public r/indonesia archive was inspected. Redistribution permission was unresolved, and its identifiers proved to be pseudonymous UUIDs rather than usable Reddit status/comment IDs. The source text and row-level derivatives were excluded from deliverables. Metadata, download/hash receipt, screening QC and exclusion explanation remain. Its screened rows and keyword matches contribute **zero** to delivered data counts. This exclusion avoids inflating the requested corpus with unusable or improperly characterized material.

## 3. Cleaning principles

The immutable source layer is distinct from cleaned derivatives. Original source wording is not translated, paraphrased, stemmed or converted to lowercase in the clean text. No synthetic records, augmentation, imputed testimony or inferred Nexora facts were created.

### 3.1 App-review cleaning

- Read selected CSV members directly from original ZIPs; decode UTF-8/BOM as documented.
- Preserve source ID, member and zero-based source data-row index.
- Normalize Unicode to NFC; replace selected control characters and collapse whitespace; preserve case, punctuation, slang and emoji.
- Exclude empty/null-like text only, before exact deduplication.
- Deduplicate on exact app + original date string + original rating string + normalized text. This is not author-level, semantic or near-duplicate deduplication.
- Parse dates without inventing missing timezones; preserve source date strings.
- Preserve native ratings/helpful votes as source attributes, not sentiment findings.
- Drop direct author fields from clean schema; raw archives retain original fields. Free-text anonymization is not claimed to be complete.
- Leave unavailable language, role, native review ID and reviewer country unknown.
- Write UTF-8 JSONL and gzip; retain row-level exclusion locators/reasons and source hashes.

The exact source-level procedure, schema and raw/clean/exclusion reconciliation are in `datasets/app_reviews/METHODOLOGY.md` and its manifests.

### 3.2 Historical support-tweet cleaning

Reply edges define connected components. Retain all source rows in qualifying components, then normalize text conservatively, parse datetimes, preserve links between source surrogate tweet IDs and component IDs, and retain repeated text when attached to distinct tweet IDs. Dropping identical support responses globally could destroy conversational context; therefore repeated text is not automatically a duplicate record.

Company versus customer flags originate from source fields, not inference that an individual is an Indonesian buyer. Company categories are registry assignments used for source scope, not text-analysis labels. Per-record language/country remain unknown where absent. Source description language may be recorded as context, but is not individual language detection.

Read `datasets/twitter/METHODOLOGY_X_COLLECTION.md` and the scripts for the specific graph, null, redaction and exclusion rules. The raw CSV is a selected original-row subset; the clean CSV is a normalized, provenance-rich derivative.

### 3.3 Small published tweet samples

Preserve original PDF/CSV files and original page text extraction. Separate extraction artifacts from cleaned records. Normalize Unicode/HTML/whitespace conservatively, preserve original encodings where not reliably repairable, deduplicate within source as documented and retain row/page locators. Limited pattern-based contact-detail redaction is recorded where performed; it is not claimed as comprehensive anonymization. The two output formats are alternate representations of the same records.

### 3.4 Indexed social material

Canonicalize usable URLs and deduplicate repeated retrievals within routes. Preserve all query appearances and exact raw envelopes so one cleaned lead can be traced to multiple retrievals. Use the cross-route URL registry to distinguish unique discovered URLs from appearances across Agent Reach and built-in search. Do not add overlapping route counts as independent posts or conversations.

No unsupported language/geography/participant-role inference, search-result-to-full-post conversion, or comment multiplication is allowed. Snippets and partial reads retain their scope flags. Archived research samples cannot always be joined to search URLs because true native IDs are absent.

## 4. Counting and reconciliation

`RUN_SUMMARY.json` and the start page provide the final achieved counts. Their units are explicit. Source rows scanned, raw original archive members, scoped raw rows, clean records, distinct text hashes, conversations, indexed URL leads and query appearances are different quantities.

- Main large historical dataset/import record counts are additive only as a **record inventory**, not independent evidence or people.
- Multiple formats of one source are not counted twice.
- App exclusions reconcile selected raw rows to retained clean rows.
- Conversation counts refer to connected components of the observed source graph, not verified complete real-world conversations.
- Company-level counts can overlap where components touch several companies; use the explicitly additive stratum counts for totals.
- Search-route results can overlap each other and source datasets. No unsupported global unique-person or global unique-post claim is made.
- Unrelated members inside an original raw multiapp archive and excluded discovered sources are not part of the reported clean corpus.

## 5. Data-quality verification

Verification is technical and provenance-focused, not substantive analysis. It includes complete compressed-stream readability, parsed record counts, source/field checks, timestamp parseability, source archive hashes, date-range inventory, duplicate/exclusion reconciliation and package-file checksums. Independent QA findings and limits are retained, including unknown source collection configurations, historical coverage differences, per-record language/geography gaps and search-index selection bias.

The final ZIP is checked for structural corruption and path safety. Payload hashes are listed separately so extracted files can be verified. No credentials, sessions, browser profiles, virtual environments, partial downloads or hidden synchronization copies are intentionally packaged. Exact environment paths in historical run logs are provenance; reproduction entry points use packaged relative paths or document necessary path adaptation.

## 6. Reproduction and remaining limits

Use original retained archives for exact re-cleaning. Public latest-version downloads can change, so a later API download is not guaranteed to reproduce the recorded snapshot. Source versions, archive SHA-256 and source metadata are the identity anchors. Agent Reach search rankings and provider coverage can change over time; preserve this run's envelopes, queries, commit and timestamps rather than promising identical future search results.

Applicable source-declared licenses remain attached to each source, including non-commercial/share-alike conditions where declared. Package documentation does not relicense underlying records. Source collector completeness and authenticity are inherited provenance limits, not verified by successful parsing.

The package fulfills a broad **collection** objective. It does not claim that every retained review or support message discusses a predefined mechanism, every record is Indonesian, every record is recent, or any source measures Nexora. A later analysis should make a narrower evidence-based selection appropriate to the specific decision and retain its exclusions and denominators.
