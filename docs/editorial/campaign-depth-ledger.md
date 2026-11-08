# Campaign depth ledger: seven bounded revisions

Internal evidence record for the depth pass over seven campaign posts. Paths are relative to this worktree; `../source` is the original corpus. Not reader-facing. No post in this set was published, scheduled, or committed.

Scope: the KO post under `_posts/`, the EN post under `en/posts/`, the Naver draft under `docs/editorial/distribution/naver/`, and the existing topic SVG under `assets/img/posts/renewal/` for each of the seven slugs. This seven-post pass did not modify the RAG exemplar or its figure, `examples/`, `_config.yml`, `.gitignore`, the 2024 MCP archive, the publication manifest, templates, or brand/about pages. A later bounded corrections pass updated the seven posts and figures below, plus `rag-padding-bug.svg`, `examples/rag-search-diagnostics/README.md`, `fact-ledger.md`, `depth-checklist.md`, and this ledger; those edits are listed under "Bounded corrections pass" at the end.

## 1. mobile-automation

Files: `_posts/2024-07-28-mobile-automation.md`, `en/posts/mobile-automation.md`, `docs/editorial/distribution/naver/mobile-automation.md`, `assets/img/posts/renewal/mobile-automation.svg`.

### Source evidence

| Claim | Source line |
|---|---|
| Appium in 2014; 4+ devices in parallel through Parallels; result reporting | `../source/_posts/2024-07-28-mobile-automation.md:15` |
| 2018 commerce QA, Android and iOS, Jenkins CI | `:17` |
| Missing/changed resource IDs, retry loop, native transition, release cadence | `:21` |
| Espresso/XCUITest white-box comparison and maintenance/access cost | `:25-27` |
| Katalon + POM, one month conversion | `:31` |
| API-shaped data, GPT self-healing, image vision | `:37,39` |

### Decisions added

- Verification split: state preparation, one business UI interaction, evidence, cleanup. The later corrections pass replaced the undefined-helper code with an input/expected/observed/evidence/cleanup table using consistent 10,000 → 9,000 coupon values.
- Native ≠ compile-time safety: Android `R.id` constant references compile; iOS accessibility identifier queries are runtime strings. Build integration/source access and selector checking are stated as separate dimensions.
- Appium fails at the locating step. The source records delayed feedback but not its cause; suite-level result aggregation is described as a possible pipeline issue, not a confirmed historical cause.
- Diagnostic matrix: environment, locator/rendering, data state, business rule — with evidence and next action per class.
- False-pass mechanism for automatic selector repair: ambiguous candidates, silent reselection, weak assertion. Mitigations: fail on ambiguity, log old/new selector, assert business outcome.
- Release-cadence contribution is qualified, not causal.

### Reader takeaway

Decide which checks belong in the UI and which in an API, then classify a failure before changing tools.

### Verification limits

No Appium, Espresso, XCUITest, or Katalon run was performed. No failure-rate, accuracy, or release-cycle metric is claimed. The table is illustrative only. The former “forty UI tests / one API plus five checks” numerical result was removed; the replacement is labeled a proposed allocation, not a measurement.

## 2. setup-slackbot-initialization

Files: `_posts/2024-09-25-setup-slackbot-initialization.md`, `en/posts/setup-slackbot-initialization.md`, `docs/editorial/distribution/naver/setup-slackbot-initialization.md`, `assets/img/posts/renewal/setup-slackbot-initialization.svg`.

### Source evidence

| Claim | Source line |
|---|---|
| Functions built: auth reset, account ID lookup, point charging, order handling | `../source/_posts/2024-09-25-setup-slackbot-initialization.md:47-50` |
| RTM web server; inbound restriction; Socket Mode switch | `:74` |
| `app_mention` + Event Subscriptions; bot install | `:82-88` |
| Original `app_mention` async handler with `say` | `:128-133` |

### Current primary docs

- Ack behavior and the ~3 second expectation: https://docs.slack.dev/tools/bolt-python/concepts/acknowledge/
- Scope names: https://api.slack.com/scopes

### Decisions added

- Ack vs job completion. Interactive handlers ack explicitly; events are acknowledged by the SDK. The article does not tell readers to add manual acks to every event handler.
- Socket Mode changes transport only; it grants no caller authorization and no exactly-once execution.
- Minimal scopes: `connections:write` for the app token; `app_mentions:read` and `chat:write` for the original mention/reply example. Other surfaces are linked to Slack docs rather than guessed.
- Server-side authorization is separate from button visibility; payloads can be replayed and Slack may retry. Authorization covers actor and target/action, not only an actor allowlist.
- The later corrections pass replaced the incomplete handler with a request/state sequence: operation identity, duplicate delivery, double click, later intentional re-run, durable job result, and reconciliation. A `SET NX` TTL lock is described as reducing concurrent duplicates only; TTL expiry, worker crash, queue handoff loss, and two authorized actors remain. The table does not claim exactly-once execution.

### Reader takeaway

Treat a Slack button as an untrusted request: ack fast, authorize the actor and target on the server, deduplicate the operation, report state in place, and add durable result and downstream idempotency for crash safety.

### Verification limits

No Slack app, Socket Mode connection, or Redis instance was run. The sequence is illustrative. No historical approval implementation is claimed; approved-actor limits are labeled as current advice.

## 3. compare-sounds-automation

Files: `_posts/2024-08-01-compare-sounds-automation.md`, `en/posts/compare-sounds-automation.md`, `docs/editorial/distribution/naver/compare-sounds-automation.md`, `assets/img/posts/renewal/compare-sounds-automation.svg`.

### Source evidence

| Claim | Source line |
|---|---|
| PostgreSQL docker-compose; `songs`, `fingerprints` tables | `../source/_posts/2024-08-01-compare-sounds-automation.md:22,29-30` |
| `fingerprint_directory` reference load | `:47` |
| Screen Recording → ADB pull → MP4 → MP3 → match | `:81-86` |
| TV on, family talking, still matched | `:88` |

### Current primary docs

- `adb shell screenrecord` records video only: https://developer.android.com/tools/adb#screenrecord
- Fingerprint project: https://github.com/worldveil/dejavu

### Decisions added

- Four separate questions: audio stream present, sound occurred, expected sound, business completion. Each has different evidence.
- `ffprobe -select_streams a:0` checks for an audio stream; empty output means capture failure, not silence. The command has an explicit existence precondition.
- `volumedetect` separates silent capture from absence of sound; it does not test the fingerprint algorithm.
- Positive, negative, and confuser controls; threshold chosen between measured distributions. Overlap means no error-free separating threshold exists on those samples; the policy must trade false positives and negatives or change signals. Threshold-selection samples and validation samples are separated. “No match” alone is not attributed to acquisition failure; stream, signal, reference, and time window are checked first.
- Failed comparison retains recording, extracted audio, reference version, score, and scenario step.

### Reader takeaway

Check acquisition before matching, calibrate the threshold with controls, and never treat a match as proof of delivery.

### Verification limits

No device, real recording, PostgreSQL instance, or Dejavu run was performed. No accuracy, threshold, or processing-time figure is claimed. Root did run the exact `ffprobe -select_streams a:0` and `ffmpeg volumedetect` patterns on generated fixtures with FFmpeg 8.1 (`../audio-command-check.json`): video-only MP4 → empty codec; silent WAV → `pcm_s16le`, mean/max -91.0dB; 440Hz tone → `pcm_s16le`, -21.1/-18.1dB. The articles cite that narrow command check separately from untested recording and recognition. The earlier `appbaseio/dejavu` mix-up is corrected.

## 4. sms-management-system

Files: `_posts/2024-09-12-sms-management-system.md`, `en/posts/sms-management-system.md`, `docs/editorial/distribution/naver/sms-management-system.md`, `assets/img/posts/renewal/sms-management-system.svg`.

### Source evidence

| Claim | Source line |
|---|---|
| Prose: codes kept 10 minutes | `../source/_posts/2024-09-12-sms-management-system.md:52,168,246` |
| `set_key(..., ttl=300)` for both keys | `:194-195` |
| `get_code` reads `sms:{phone}` then `json.loads` | `:250-261` |
| 30-minute WebSocket session | `:268` |
| Anyone who can install the app can share the number | `:351` |

### Decisions added

- TTL inconsistency is documented, not resolved by assertion. `ttl=300` looks like five minutes, but the wrapper is undefined and its unit is unknown, so the deployed value is unverified.
- Verification procedure: `redis-cli TTL`/`PTTL` immediately after send and six minutes later; `-1` and `-2` semantics explained.
- Current policy example uses explicit `redis.set(..., ex=600)` as a chosen 10-minute policy, not a historical claim.
- Latest-value semantics: the code overwrites per phone through `_redis.set_key`; no list/`RPUSH`, so no invented “list retention” bug. The later corrections pass removed a shortened excerpt that used `_redis.set` and now references the actual `send_code` calls.
- Source-level inference, labeled as inference: `get_code` stores a code string but parses it as JSON. `json.loads('1234')` returns an integer and `json.loads('0123')` raises. No runtime or production observation is claimed.
- Synthetic two-run timeline shows arrival order differing from request order; the article states it is not a recorded incident. Receive time and expected sender are freshness hints only; they do not resolve two concurrent requests on one phone. Leasing/serialization or a provider correlation identifier is required for genuine run correlation.
- Four separate concerns: retention, session lifetime, access control, run correlation.

### Reader takeaway

Verify the effective TTL from Redis instead of trusting prose, and lease a phone or carry correlation data before parallel runs share it.

### Verification limits

No Redis, FastAPI server, Android app, or Slack call was executed. The wrapper implementation and the historical runtime are unknown. The JSON parsing consequence is derived by reading the source. Access controls and sender allowlists remain current recommendations.

## 5. log-view-system

Files: `_posts/2024-09-13-log-view-system.md`, `en/posts/log-view-system.md`, `docs/editorial/distribution/naver/log-view-system.md`, `assets/img/posts/renewal/log-view-system.svg`.

### Source evidence

| Claim | Source line |
|---|---|
| Kafka chosen for volume/bottleneck concerns and interest | `../source/_posts/2024-09-13-log-view-system.md:14` |
| `sadd` service names; key `{service}_{timestamp}`; Kafka send | `:136-140` |
| Consumer saves then publishes | `:182-210` (consumer block) |
| UI drops display updates while paused | `:315` |
| `fetchLogsForService` reads the DB on resume/filter change | `:333-368` |
| `@app.on_event("startup")` | `:77` |

### Current primary docs

- Redis Pub/Sub does not persist or replay missed messages: https://redis.io/docs/latest/develop/pubsub/

### Decisions added

- Storage path vs live path, with the order “save then publish” and its consequence.
- Correction of the earlier simplification: the UI reads the database not only on refresh but also on pause-resume and filter changes.
- Pause stops display, not collection; resume can refill from history.
- Failure matrix: Kafka send, DB write, publish, disconnect, duplicate — each with the evidence that separates it.
- No Kafka offset/commit claim; the article says the manager implementation is absent from the source.
- The consumer sample is labeled shortened, not verbatim source; the DB-save-before-publish order is supported.
- UI ping/pong is described as connection bookkeeping, not a business requirement that would make WebSocket necessary over SSE.
- Current alternatives: SSE, WebSocket, no Kafka, Redis Streams for replay. Labeled as design judgment, not a migration history.
- No exactly-once claim; message-key uniqueness is recommended.

### Reader takeaway

Ask “is it in the database?” before debugging Kafka: a live gap is not a storage failure.

### Verification limits

No Kafka, Redis, MariaDB, FastAPI, or browser run was performed. Pub/Sub behavior is cited from Redis docs. SSE/WebSocket comparisons are current judgment.

## 6. mobile-mcp-setup-guide

Files: `_posts/2025-07-15-mobile-mcp-setup-guide.md`, `en/posts/mobile-mcp-setup-guide.md`, `docs/editorial/distribution/naver/mobile-mcp-setup-guide.md`, `assets/img/posts/renewal/mobile-mcp-setup-guide.svg`.

### Source and current upstream evidence

| Claim | Source |
|---|---|
| Original accessibility-snapshot framing, `@latest` install, Cursor/Claude config, device steps, tool list | `../source/_posts/2025-07-15-mobile-mcp-setup-guide.md:16,73-74,117,150,260-273` |
| Current repository, device listing, Mobilewright examples | https://github.com/mobile-next/mobile-mcp |
| Protocol reference | https://modelcontextprotocol.io/ |

### Decisions added

- Exploration vs regression table: goal, input, judgment, failure handling, stage.
- Tool names are not enumerated as stable API; readers are pointed to upstream and asked to record the resolved `@latest` version.
- Model completion text is explicitly outside the evidence boundary. Tool output may include text, images, and structured results; the model's prose is distinguished from the observed tool output.
- Evidence set: before/after screenshots, accessibility snapshot, device log/app state, business state.
- Accessibility limits: unlabeled buttons, WebView internals, canvas; coordinate taps are resolution-sensitive.
- Exploration → reviewed regression procedure: record, review identifier collisions, pin preconditions, run twice, require cleanup. Two matching runs are a smoke check, not proof of determinism; a second failure does not by itself prove missing cleanup, so waits, environment, unstable locators, and product defects remain candidates.
- Cursor configuration distinguishes the user-level `~/.cursor/mcp.json` and project-level `.cursor/mcp.json`.
- Destructive-action and permission boundaries; no “AI replaces QA” claim.

### Reader takeaway

Use MCP for exploration, but require action evidence and human review before turning a flow into a deterministic test.

### Verification limits

No emulator, device, MCP server, Cursor, or Claude Desktop run occurred. Upstream content was taken from the repository's current documentation as verified by root; tool names and result formats may differ by version.

## 7. makingAutomationTesterWhoNeverBeTired

Files: `_posts/2024-07-31-makingAutomationTesterWhoNeverBeTired.md`, `en/posts/makingAutomationTesterWhoNeverBeTired.md`, `docs/editorial/distribution/naver/makingAutomationTesterWhoNeverBeTired.md`, `assets/img/posts/renewal/makingAutomationTesterWhoNeverBeTired.svg`.

### Source evidence

| Claim | Source line |
|---|---|
| CPU/memory pressure; Xeon E5 3GHz 8-core, 64GB; CPU >90%, swap 200GB | `../source/_posts/2024-07-31-makingAutomationTesterWhoNeverBeTired.md:22-23` |
| Off-the-shelf XY plotter; camera on Arduino or Raspberry Pi | `:26` |
| Fixed `time.sleep(2)` | `:58` |
| Flask bound to `0.0.0.0` without authentication | `:63` |
| Servo pins 9/10; click delay 500ms; return to 90 | `:77-78,93-95` |
| Hardware assembled, software unfinished; 24/7 BDD ambition | `:108` |

### Decisions added

- Coordinates are the hard part: a 2-D affine map needs one output equation per axis. The later corrections pass replaced the single scalar-output snippet with paired `servo_x`/`servo_y` equations, a non-collinearity check, and two held-out check points. Synthetic calibration `(100,100,15,30), (500,100,55,30), (100,400,15,90)` yields `u = 0.1x + 5` and `v = 0.2y + 10`; held-out checks at `(300,250)` and `(700,300)` are model tests, not actuator accuracy.
- Limits: affine maps parallel lines to parallel lines; perspective needs a homography (4+ non-collinear points); servo angle-to-distance may be nonlinear; residual checks at additional independent points decide whether to change the model.
- Calibration procedure and recalibration cost per device.
- Completion feedback replaces fixed sleeps: app state, camera, or sensor, each catching a different failure. More than one signal can help, but “two signals are always required” is not stated as a universal rule.
- Hardware vs source-level hook decision table.
- Unfinished state preserved; no abandonment reason invented; no physical accuracy or latency claim. The article states it is an unfinished test fixture and removes the legal/legitimacy sermon about bypassing security.

### Reader takeaway

Before building the mechanism, verify the coordinate assumption with a residual and replace the fixed wait with a completion signal.

### Verification limits

The affine values pass by hand calculation; root may run the assert. No servo, camera, Arduino, plotter, or payment system was driven. The 2-second wait and 500ms delay are historical code details, not recommendations.

## Visual pass

All seven owned SVGs now use `width="640"` with a matching `height` and `viewBox`, visible text at 22px or larger, `<title>`/`<desc>`, and no scripts or external assets.

- `mobile-automation.svg`: replaced the 720px four-stage grid with the state/UI/evidence/cleanup split.
- `setup-slackbot-initialization.svg`: replaced the setup-only stack with the click → ack → authorize → dedupe → run → status sequence.
- `compare-sounds-automation.svg`: replaced the straight capture chain with the four-question decision boundary and its failure branches.
- `sms-management-system.svg`: replaced the generic architecture with the synthetic two-run timeline and latest-value overwrite.
- `log-view-system.svg`: shows the storage and live paths with the failure annotation on each.
- `mobile-mcp-setup-guide.svg`: shows exploration, the non-evidence model summary, evidence collection, review, and regression.
- `makingAutomationTesterWhoNeverBeTired.svg`: keeps completed vs proposed, adds the mapping gate and the completion-feedback node, keeps the calibration return arrow.

No rasterization or browser inspection was performed in this tier.

## Bounded corrections pass (2026-11-08)

Applied after the seven-post rewrite, from root's campaign findings and the RAG depth review. Only the seven KO/EN/Naver posts, their existing figures where the figure repeated the claim, and the RAG figure/README/ledgers/checklist were touched.

- **mobile-automation** (KO/EN/Naver): “forty UI tests → one API plus five checks” removed or labeled a proposed allocation; “often” removed. Appium’s delayed-feedback cause is qualified as a possible pipeline issue, not a confirmed implementation. The coupon example is a table with consistent values (10,000 before coupon, 9,000 after a 10% coupon), evidence, and cleanup on failure; undefined helpers are gone. API-first verification is labeled recommended by responsibility, with offline/client-only apps acknowledged. Espresso/XCUITest process and runner behavior and the build-integration versus selector-checking axes are stated separately.
- **setup-slackbot-initialization** (KO/EN/Naver): the incomplete handler, undefined `redis`/`run_job`, actor-only allowlist, and one-hour `actor:target` lock are removed. A request/state sequence separates duplicate delivery, double click, and later intentional re-run; authorization covers actor and target/action; durable result and downstream idempotency are required beyond a `SET NX` TTL lock. Exactly-once is not claimed. The reversed “user must not be able to tell” sentence is fixed. `AsyncApp` import is explicit; the synchronous thread-pool claim is corrected. The figure no longer says “one execution.”
- **compare-sounds-automation** (KO/EN/Naver, SVG): overlap means no error-free threshold on those samples, not that no threshold can ever be chosen; threshold-selection and validation samples are separated; “no match” is a diagnostic starting point, not proof of capture failure. The articles now cite root's FFmpeg 8.1 synthetic command check separately from untested real recording and recognition.
- **sms-management-system** (KO/EN/Naver): the `_redis.set` excerpt is gone; the text references the actual `_redis.set_key` calls. `json.loads('1234')`/`('0123')` behavior is stated without a production-failure claim. Receive time and sender are freshness hints, not run correlation; leasing/serialization or provider correlation is required for concurrent runs on one phone.
- **log-view-system** (KO/EN/Naver): UI ping/pong is connection bookkeeping, not a reason WebSocket is required over SSE. The shortened consumer sample is labeled shortened; DB-save-before-publish remains supported.
- **mobile-mcp-setup-guide** (KO/EN/Naver): tool output may be text, images, or structured results; model prose is distinguished from observed tool output. Two runs are a smoke check, not proof of determinism, and a second failure does not prove missing cleanup. Cursor user and project config paths are both stated.
- **makingAutomationTesterWhoNeverBeTired** (KO/EN/Naver): the affine snippet now solves one output per axis, with two held-out check points and an explicit “educational self-check, not actuator validation” note. The legal/legitimacy sermon is removed. “At least two signals” is no longer a universal mandate. The unfinished-fixture and no-physical-accuracy status is explicit.
- **RAG** (KO/EN/Naver, `rag-padding-bug.svg`, README, fact-ledger): F1 corrected (chunk units unknown; illustrative 100-character chunks total far below 3000; no proven historical truncation), F2 applicability added (deliberate `ntotal=2 < k=5`; 2024 HNSW size unknown; IVF `nprobe`, HNSW `efSearch`, and filtered searches can reduce candidates; FAQ/Index links), F3 corrected (`0.0000` is four-decimal display of a float32-max-like distance and a hint, not proof), F4 corrected (the original `if results` branch exists and is bypassed when `-1` resolves with retained metadata). The Naver edition is rewritten as an independent operational evidence checklist. The SVG says “A duplicate chunk in prompt.” The checklist adds “could the original configuration execute this path?” and “keep undefined helpers undefined.”

Not done here: no shell, test, build, browser, rasterization, or publication run. Root owns those checks and final acceptance.

## Unverified items for root

- All shell-based checks: markup/build, link resolution, SVG rendering and PNG export, and execution of the affine assert.
- The SMS `json.loads` behavior on a leading-zero code is inferred from source, not observed.
- The deployed SMS TTL and wrapper units remain unknown.
- The current Mobile MCP tool names and result formats were not exercised.
- No external link in any post was fetched during this write; primary URLs were used as given by the brief and existing drafts.


## Final sentence corrections after Opus campaign review

Root applied bounded prose corrections after all DeepSeek writers exited. These do not implement a Slack job service or change lab logic.

- M1: Slack button repeated clicks, late-ack user errors, HTTP Events API delivery retries and Socket Mode envelope acknowledgement are distinct. Removed claims of automatic late-acked button action redelivery, including the SVG. Root opened primary interactivity docs (acknowledgement response), Events API retries and Socket Mode receive/acknowledge docs on 2026-11-08. A missing promise in a document is not proof that every transport can never redeliver an interaction.
  - https://docs.slack.dev/interactivity/handling-user-interaction/
  - https://docs.slack.dev/apis/events-api/
  - https://docs.slack.dev/apis/events-api/using-socket-mode/
- M2: replaced the stray SMS phrase about approved devices in the Slack post with approved actors and target authorization.
- M3: a low match score against one reference cannot distinguish a different sound from no sound. Removed the unsupported single-cause notification-setting diagnosis. No new recognition accuracy claim.
- LogViewer: original producer send catches/logs exceptions without rethrowing (source lines167–175); caller may return success without proven Kafka delivery. Consumer loop has no inner exception handler (185–198); task supervision/restart is not shown. Updated all three editions and diagnostic tables.
- SMS: original get_code logs data_json (source line255), so Redis TTL does not expire copies in application logs. Added the concrete counterexample and value-free diagnostic advice to all three editions.
- Hardware Naver: replaced copied affine Python blocks with an operator-facing calibration/independent-point decision table. Main KO/EN retain the real executable arithmetic example.
- Mobile Naver: present diagnostic method is explicitly a new revision proposal rather than a claimed historical conclusion.
- MCP: named the upstream Mobilewright example as an unexecuted alternative, and clarified that the no-device-run boundary applies to this revision.

Optional polish not applied: a complete redesign of the SMS timeline arrows and broad shortening of every repeated evidence caveat. Neither changes the reviewed mechanism; no new diagram outcome is claimed.
