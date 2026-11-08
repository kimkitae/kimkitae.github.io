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
