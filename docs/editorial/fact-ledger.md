# Fact ledger for the Opus review fixes

Internal evidence ledger. Not reader-facing prose. Paths are relative to this worktree; source references point to the original corpus at `../source`.

## Hardware: assembled, not integrated

| Corrected claim | Source evidence | Treatment |
|---|---|---|
| Hardware was assembled; software integration was not finished | `../source/_posts/2024-07-31-makingAutomationTesterWhoNeverBeTired.md:108-110` | Historical fact retained. |
| Original sample bound the Flask service to `0.0.0.0` without access control | `../source/_posts/2024-07-31-makingAutomationTesterWhoNeverBeTired.md:63` | Historical fact; current post uses it only as a lesson and does not publish a runnable insecure service. |
| CPU and memory pressure motivated separate hardware | `../source/_posts/2024-07-31-makingAutomationTesterWhoNeverBeTired.md:22-23` | Historical fact retained. |
| XY plotter was bought off the shelf; camera connected to Arduino or Raspberry Pi | `../source/_posts/2024-07-31-makingAutomationTesterWhoNeverBeTired.md:26` | Historical fact retained. |
| Proposed loop: Appium check, Raspberry Pi camera, Arduino serial, servo tap, Appium check | `../source/_posts/2024-07-31-makingAutomationTesterWhoNeverBeTired.md:32-36,66-67` | Labeled proposed flow; not verified end to end. |
| Fixed two-second wait in the original | `../source/_posts/2024-07-31-makingAutomationTesterWhoNeverBeTired.md:58` | Historical code detail; completion-signal feedback is current advice. |
| One phone, one plotter, 24/7 BDD ambition | `../source/_posts/2024-07-31-makingAutomationTesterWhoNeverBeTired.md:108` | Historical stated goal, not deployment. |

Removed as unsupported: deployed calibration experience, reason for abandoning, 127.0.0.1 binding history, approved-account history, and the claim that no real data was used.

## SMS: 10-minute TTL, no invented controls

| Corrected claim | Source evidence | Treatment |
|---|---|---|
| Android receiver app forwards SMS codes to Slack | `../source/_posts/2024-09-12-sms-management-system.md:12` | Historical fact retained. |
| FastAPI + Redis + WebSocket server | `../source/_posts/2024-09-12-sms-management-system.md:51` | Historical fact retained. |
| 10-minute retention | `../source/_posts/2024-09-12-sms-management-system.md:52` | Restored as `ex=600`; source code at `:194-195` uses `ttl=300`, so the source is internally inconsistent. The prose and brief take precedence. |
| 30-minute WebSocket session with cleanup | `../source/_posts/2024-09-12-sms-management-system.md:268` | Historical fact retained. |
| Device description, manager, Slack channel UI | `../source/_posts/2024-09-12-sms-management-system.md:280` | Historical fact retained. |
| Anyone who can install the app can share the test number | `../source/_posts/2024-09-12-sms-management-system.md:344` | Historical weakness retained; approval boundaries are current advice. |
| `createFromPdu(byte[])` deprecated in API 23; use `createFromPdu(byte[], String)` | `../source/_posts/2024-09-12-sms-management-system.md:22`; Android docs https://developer.android.com/reference/android/telephony/SmsMessage | Technical correction. |

Removed as unsupported: an enforced authorization boundary, a working sender allowlist, extracted configuration, retry behavior, a blanket no-message-body-storage claim, an "operating lesson" about access control, and Android 11 as the cause of SMS policy restrictions.

## testing1 and testing2

| Corrected claim | Source evidence | Treatment |
|---|---|---|
| testing1 is a 2021 reading note; the thread was updated at that time | `../source/_posts/2021-01-16-testing1.md:10-14` | Historical framing retained; no application-to-work claim. |
| "30 minutes" was not in the source | `../source/_posts/2021-01-16-testing1.md` (no such figure) | Removed from Korean, English, Naver, and diagram. |
| testing2 is a reading note on DevelopSense, not the author's own view | `../source/_posts/2021-01-16-testing2.md` structure matches https://developsense.com/blog/2018/06/test-cases-and-coverage (2018-06-28); the original has no attribution | Rewritten as a short attributed note. Source-derived summary is under 180 words across Korean, English, and Naver. |

The DevelopSense author name is not stated in the source or the review, so the note cites the publication and date only.

## Mobile flagship: preserve 2024 assessment, separate current advice

| Corrected claim | Source evidence | Treatment |
|---|---|---|
| The original 2024 post was positive about GPT self-healing and script generation | `../source/_posts/2024-07-28-mobile-automation.md:37` | Historical assessment retained. |
| "Do not fully trust automatic repair" | New wording | Marked as current advice, not as the 2024 judgment. |
| No code exists in this post | `../source/_posts/2024-07-28-mobile-automation.md` and current post | Removed "code and tool usage" boilerplate. |

## RAG: source structure, current verification advice

| Corrected claim | Source evidence | Treatment |
|---|---|---|
| Local Llama 3 with Ollama; mxbai-embed-large embeddings; FAISS; Slackbot access | `../source/_posts/2024-08-02-quick-start-rag-and-llm-for-automation.md:23,37,64,117,237,255` | Historical facts retained. |
| Chunk size/overlap 100/25 | `../source/_posts/2024-08-02-quick-start-rag-and-llm-for-automation.md:76` | Restored in prose and diagram. |
| Temperature 0 | `../source/_posts/2024-08-02-quick-start-rag-and-llm-for-automation.md:207,213` | Historical fact retained. |
| LoRA memory 130GB | `../source/_posts/2024-08-02-quick-start-rag-and-llm-for-automation.md:26` | Source figure retained, not generalized. |
| Failed-embedding logging and dimension check | `../source/_posts/2024-08-02-quick-start-rag-and-llm-for-automation.md:40-120` | Source code retained; failure-count logging is current advice. |

Removed as unsupported: observed intermittent embedding API failures, "we never allowed execution" in the actual build, example annotation work, and a diagnostic history. Auto-execution exclusion is now a recommendation.

### RAG depth rewrite: source, current docs, synthetic reproduction

Historical source lines:

| Claim | Source evidence | Treatment |
|---|---|---|
| Local Llama 3 via Ollama, `mxbai-embed-large`, FAISS HNSW, Slackbot with retrieved snippets | `../source/_posts/2024-08-02-quick-start-rag-and-llm-for-automation.md:23,37,64,117,237,255` | Retained as 2024 implementation, not current recommendation. |
| `create_index` appends a successful embedding and its chunk in the same branch; logs failures and checks equal dimensions | same source, `create_index` block | Retained as a paired-metadata invariant. No alignment bug is claimed in that code. |
| Chunk parameters 100 and overlap 25, capped by `[:max_chunks_per_script]` default 10 | same source, `create_index` signature and slice | Retained. `chunk_text` is undefined, so units and algorithm are unproven; the cap can exclude later code. |
| Search filter is `if i < len(scripts)`; score is `1 / (1 + distance)`; `truncate_context` slices strings with default 9000, call site 3000 | same source, `search_scripts` and `truncate_context` | Retained as the historical code path. Current article explains the consequences. |
| A separate test-case Q&A service used LLM keyword extraction and pre-generated keyword data to reduce context | same source, final paragraph | Restored as an actual deterministic-lookup alternative, not a new experiment. |
| Ollama request puts `temperature`, `top_p`, `max_tokens` at the top level | same source, `ask_ollama` request body | Treated as an unknown 2024 server behavior; not asserted to be correct or rejected. |

Current documentation:

| Claim | Source | Treatment |
|---|---|---|
| FAISS pads missing labels with `-1` when fewer neighbors than `k` exist | https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexFlat.html | Used to explain the reproduction. |
| FAISS L2 indexes return squared L2; cosine is normalized dot product | https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances | Used for metric consistency and the non-probability warning. |
| `/api/generate` puts runtime controls under `options`; generation limit is `num_predict` | https://docs.ollama.com/api/generate | Labeled current API advice, not a claim about the 2024 server. |
| No local Ollama binary or runtime was found | Root environment check | No live embedding or generation test is claimed. |

New synthetic reproduction (2026-11-08):

| Observed/derived fact | Evidence | Treatment |
|---|---|---|
| Python 3.12, `faiss-cpu 1.15.1`, `numpy 2.5.4`; two synthetic 2-D vectors and two synthetic chunks | `../rag-original-bug-reproduction.json`; root venv `../rag-lab-venv` | Labeled synthetic; proves label handling, not retrieval quality. |
| `k=5` returns labels `[0, 1, -1, -1, -1]` for both `IndexFlatL2(2)` and `IndexHNSWFlat(2, 32)` | same JSON, both cases | Reproduced result. |
| Original filter maps to `[cancel_order.py, archive_order.py, archive_order.py, archive_order.py, archive_order.py]`; the last chunk appears four times total (one real hit plus three `-1` copies). Bounded filter yields `[cancel_order.py, archive_order.py]` | same JSON, both cases | Reproduced result. |
| Synthetic fixtures produce squared L2 distances 0.01 and 0.81 for the two real neighbors | `examples/rag-search-diagnostics/lab.py` fixtures | Derived from the published vectors; the vectors are synthetic, not actual embeddings, and this is not a production measurement. |
| Empty-index fixture keeps two metadata records with zero vectors, so the original filter maps all five `-1` labels to the last chunk; `create_index` returns `(None, None)` when no embedding exists, and empty metadata would raise `IndexError` instead of inventing a chunk | `examples/rag-search-diagnostics/lab.py`, `test_lab.py`, `README.md` | Deliberately inconsistent split-load boundary, not a normal historical path. Bounds alone do not detect same-length reordered metadata. |
| 1,100-character cap example assumes complete 100-character windows with stride 75: 14 complete windows, first 10 cover characters 0–775; partial-tail handling is undefined in the original | article worked example | Illustrative convention only, not a claim about the original helper's exact window count. |
| Original joins the top three chunk `content` strings with spaces, then truncates at 3000 characters. Under the illustrative 100-character assumption, three chunks plus two separators total at most 302 characters, so the cut cannot explain a missing signature. `chunk_text` is undefined, so units and returned lengths are unknown; the source does not prove a historical truncation event. Larger chunk configurations can make the string limit relevant | `../source/_posts/2024-08-02-quick-start-rag-and-llm-for-automation.md`, `truncate_context` and `search_scripts`; F1 review | Qualified correction: diagnose small chunks and omitted paths first; count real characters and target-model tokens before blaming truncation. |
| The reproduction deliberately uses `ntotal=2 < k=5`. The original 2024 HNSW index size is unknown, so no claim that the bug triggered in production. A large index is not sufficient safety: IVF with low `nprobe` can search too few candidates, and HNSW with low `efSearch` or a candidate-removing filter can also pad | FAISS FAQ section “What does it mean when a search returns -1 ids?” https://github.com/facebookresearch/faiss/wiki/FAQ; https://faiss.ai/cpp_api/struct/structfaiss_1_1Index.html; F2 review | Applicability stated in KO/EN/Naver and README. Filtered-search generalization depends on index/filter implementation and is not measured. |
| Padded distances are float32-max-like, about `3.4028e38`; the article's `1 / (1 + d²)` printed with `{score:.4f}` displays `0.0000`, not necessarily mathematically zero. A repeated last path plus `0.0000` is a hint, not proof; confirm raw `-1` labels | `lab.py` / reproduction output; F3 review | Qualified correction: keep correct arithmetic; describe the display rounding and diagnostic limit. |
| The original caller already has an `if results` / not-found branch. Accepting `-1` keeps the result list non-empty when metadata remains, so that branch is bypassed. `create_index` returns `(None, None)` when no embedding exists; inconsistent empty-index metadata is a separate split-load fixture | `../source/_posts/2024-08-02-...`; `test_lab.py`; F4 review | Accepted recommendation; no claim that the empty-metadata case was a normal historical path. |
| Exact-key lookup is a dictionary or SQL equality lookup; SQLite FTS is lexical ranked retrieval, not deterministic unique-record lookup. The original keyword extraction still uses an LLM, so the service is not fully deterministic unless the extracted key is validated | `../source/_posts/2024-08-02-quick-start-rag-and-llm-for-automation.md`, final paragraph; current article | Distinguishes exact-key, full-text lexical, and semantic vector search; no unmeasured hybrid improvement claim. |
| Academy AX table (attendance count, make-up rule, leave approval) is illustrative | article section | Explicitly not a deployment or actual-institutional-data claim. |
| Lab tests assert Flat/HNSW padding, original and bounded mapping, empty index with retained metadata, out-of-range positive label, and metric identity | `examples/rag-search-diagnostics/test_lab.py` | Execution belongs to the review environment; not claimed as passed here. |
| New figure `rag-padding-bug.svg` shows the reproduced flow at 640x1210 with visible labels at 22px or larger | `assets/img/posts/renewal/rag-padding-bug.svg` | Source added; browser and PNG raster checks belong to the review environment. |

Review disposition: F2 (applicability), F4 (existing not-found branch), F5 (independent Naver lesson), and F6/F7 (wording, coverage, figure label) are accepted as written. F1 and F3 are accepted with qualification: F1's claim that truncation ran in the original configuration is not supported because `chunk_text` is undefined and the illustrative 100-character chunks total far less than 3000 characters; F3's `0.0` is a four-decimal display of a float32-max-like distance and a diagnostic hint, not mathematical zero or proof.

Removed as unsupported in this rewrite: a live semantic retrieval test, LLM answer-quality measurement, production performance numbers, a historical failure actually observed in 2024, and any claim about how an unknown 2024 Ollama server parsed top-level runtime parameters.

## Sound: screen recording has no audio

| Corrected claim | Source evidence | Treatment |
|---|---|---|
| Screen recording, then format conversion | `../source/_posts/2024-08-01-compare-sounds-automation.md:83-84` | Historical steps retained, but audio capture is now a separate prerequisite. |
| `adb shell screenrecord` records video only | https://developer.android.com/tools/adb#screenrecord | Technical correction. |
| Dejavu with PostgreSQL | `../source/_posts/2024-08-01-compare-sounds-automation.md:20-42`; https://github.com/worldveil/dejavu | Restored `postgres`; GitHub project is the primary reference. |
| TV and family conversation observation | `../source/_posts/2024-08-01-compare-sounds-automation.md:88` | Retained as a specific observation, not a performance guarantee. |

The historical capture path is unknown and is no longer guessed. MoviePy is labeled as 1.x/2.x compatible guidance; FFmpeg is the primary extraction example.

## Slack, MCP, Netplan, WDA, log viewer

| Corrected claim | Source evidence | Treatment |
|---|---|---|
| Slack app uses `app_mention`, install, and reinstall | `../source/_posts/2024-09-25-setup-slackbot-initialization.md:85,88,95,130` | Historical facts retained. |
| App token `connections:write`; bot `app_mentions:read`, `chat:write` | Official Slack docs https://api.slack.com/scopes | Added as required scopes and links. |
| MCP 2025 used `@latest`, not a verified historical pin | `../source/_posts/2025-07-15-mobile-mcp-setup-guide.md:65-79` | Installation block removed; readers are told to use upstream instructions and record the resolved version. |
| MCP archive notice should point to the original revision | `_posts/2024-12-20-mobile-mcp-setup-guide.md`; revision `bbcc4f1` | Notice links the Git revision instead of claiming the original body is in the notice. |
| Netplan Wi-Fi with networkd needs `wpasupplicant` | Netplan docs https://netplan.readthedocs.io/en/stable/netplan-yaml/ | Added as a prerequisite. |
| WDA current guidance is the xcuitest driver | `../source/_posts/2021-01-30-webdriveragent-upgrade.md`; https://appium.github.io/appium-xcuitest-driver/ | Link updated; historical framing preserved. |
| Kafka interest is source-backed | `../source/_posts/2024-09-13-log-view-system.md:14` | Retained. The retrospective lesson was replaced with current advice. |

## About and Naver distribution

| Corrected claim | Source evidence | Treatment |
|---|---|---|
| Workato cross-department automation, Slack account approval, release regression, deploy monitoring | `../source/_tabs/about.md` project entries | Restored as "previously in the public career history"; internal metrics omitted. |
| KFlowLabs is the author's AX/automation collaboration contact | User-selected identity from the brief | Stated without sponsorship or company-case claims. |
| Academy AX topics are proposals | Brief and existing editorial policy | Marked as future topics, not published proof. |
| Naver campaign: 8 weekly, 8 archive/reference | Opus review recommendation | Recorded in `docs/editorial/distribution/manifest.yml`; no publication claimed. |
| Naver image upload uses PNG exports, not SVG | Root export mapping `naver-images/<slug>.svg.png` | Manifest maps each slug; HTML comments removed from all 16 drafts. |

## Diagram pass

All 15 non-flagship SVGs were rewritten by hand to `viewBox` width 640 with explicit matching `width`/`height`. Visible text is 22px or larger, headings 28px. Hardware now has a solid completed node, dashed proposed nodes, Arduino, camera, and an Appium/camera feedback arrow. `mobile-automation.svg` was left unchanged as instructed.

No rasterization or browser check was performed in this worker tier; root owns PNG rendering and visual inspection.

## Remaining unknowns

- The SMS source prose says 10 minutes, while its code sample uses `ttl=300`. The correction follows the brief and prose (`ex=600`); the discrepancy remains in the source.
- The original notification-sound post does not specify which audio capture path it used. The corrected post treats audio as a separate prerequisite and does not guess the path.
- The historical Mobile MCP package version is not recorded in the source. The corrected post points to upstream instructions and asks readers to record the resolved version.
- The archive link uses revision `bbcc4f1`; this worker did not fetch the Git host to verify the commit URL resolves.
- The original Korean source lacked attribution. Opus recheck verified Michael Bolton on the DevelopSense page; the final notes now name the author as well as the publication and date.


## RAG abstention clarification after campaign review

The original search_scripts explicitly removes threshold filtering with filtered_results = results. A nonempty successful index search can return nearest neighbors for an unrelated question. The existing empty-list branch is not a validated relevance/abstention policy. KO, EN and Naver now distinguish this from the -1 bounds bug and recommend unrelated-question negative controls without inventing a universal cutoff or a measured abstention score.
