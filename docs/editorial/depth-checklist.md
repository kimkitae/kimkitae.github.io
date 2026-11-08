# Editorial depth checklist

Publication bar for substantive campaign rewrites. Apply it before an article is treated as finished. A post passes only when every item has a concrete answer in the draft; extra length is not a substitute. Short reference or reading notes are exempt from the rewrite effort but still need accurate attribution and an honest summary.

## 1. Concrete reader problem

- The opening names a real task, failure, or decision, not a topic.
- The problem is specific enough that the reader can tell whether it applies to them.
- The article states what the reader will be able to do afterward.

Fail: “RAG is important” or a definition-led introduction with no task.

## 2. Source-backed constraints

- Every historical claim traces to the source post, an observed run, or a cited upstream document.
- Versions, dates, hardware, and institution-specific observations are labeled as such.
- Unknowns are stated as unknowns instead of being filled in for narrative flow.
- Confidential material is removed or generalized; no invented customers, metrics, approvals, or anecdotes.

Fail: a plausible motivation paragraph with no evidence, or a 2024 detail presented as a universal requirement.

## 3. A nontrivial choice and its rejected alternative

- The article identifies a decision point.
- It names at least one alternative that was considered or is reasonable.
- It explains the constraint that made the chosen option win, including its cost.
- “We used X” without a tradeoff is not a choice.

Fail: a tool list, or a recommendation with no rejected option.

## 4. Implementation detail or example

- At least one section shows the actual mechanism: code, config, command, data shape, or interface.
- The example is small enough to read but specific enough to reproduce.
- Code is explained; a wall of code without commentary does not count.
- Abbreviated code is labeled as abbreviated.

Fail: pseudocode that hides the detail the article is supposed to teach.

## 5. Failure or edge case, and how to detect it

- The article covers at least one way the approach fails or degrades.
- It shows the symptom and the evidence that distinguishes the cause.
- A diagnostic step or table tells the reader what to inspect next.
- If the failure was reproduced, the input, expected output, and observed output are included.
- Each diagnostic path is checked against the original configuration: could it actually execute with the stated values? Under a 100-character chunk assumption, for example, three chunks cannot reach a 3000-character cut. A plausible failure is not an observed one.
- Undefined helper semantics stay undefined. Do not infer units, return shapes, or behavior the source never shows.

Fail: only the happy path, or “test carefully” with no observable check.

## 6. Verification boundary

- The article says what was actually run, in which versions, with which data.
- Synthetic, mocked, or illustrative results are labeled and not presented as production quality.
- Claims that were not tested are marked as unverified or omitted.
- No test-pass claim is made without an observed run.

Fail: a benchmark-shaped sentence with no method, or “works well” after a synthetic check.

## 7. Transferable outcome

- The reader leaves with a checklist, decision rule, diagnostic order, or reproducible experiment.
- The takeaway is not reducible to “use the right tool” or “data matters.”
- The article does not end with a sales teaser instead of a lesson.

Fail: a summary that repeats the introduction.

## Review procedure

1. Read the draft and write the reader outcome in one sentence. If it is vague, the draft is not ready.
2. Check each item above against a specific line or block. Missing evidence means rewrite, not padding.
3. Re-read the fact ledger and confirm every number, version, and historical claim.
4. Run the reproduction or command if the article includes one; record what happened.
5. Check the visual: it must carry the lesson, not decorate the page.
6. Confirm the Korean, English, and channel editions teach the same facts with the same limits. Channel copy may be shorter, but it must stand on its own.
