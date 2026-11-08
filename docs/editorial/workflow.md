# Editorial workflow

A short runbook for producing and publishing KFlowLabs posts. The order matters: facts and confidentiality are settled before prose polish, and the rendered page is reviewed before publication.

## Pipeline

1. **Source packet from the author.** Collect notes, logs, screenshots, links, and the actual commands used. Record what was observed, what was inferred, and what was never tested.
2. **Source and fact ledger.** For every claim, note the source: personal observation, upstream documentation, repository code, or an unverified assumption. Mark historical tools and versions.
3. **Confidentiality review.** Apply `content-policy.md`. Remove or generalize customer data, credentials, internal addresses, contract terms, and unapproved screenshots. If the exact material is not cleared, do not publish it.
4. **Korean draft.** Write 4–6 meaningful sections. Separate historical observations from general advice. Label untested code as a sketch.
5. **Explanatory diagram.** Create an SVG under `assets/img/posts/renewal/`. Use English node labels, a `viewBox`, no scripts or external resources, and include title/desc. Add clear alt text and one caption in the post.
6. **Korean prose edit.** Use the pstack `unslop` edit if it is available in the provided skills tree. Preserve numbers, names, quotes, and technical terms. `im-not-ai` is a candidate, not installed or applied here; do not claim its gates ran. AI-detector evasion is not a success criterion.
7. **Fact comparison.** Re-read the edited draft against the ledger. Fix invented details, changed numbers, and new promises.
8. **English adaptation.** Write `en/posts/<slug>.md` with its own canonical URL and reciprocal `translation_url` front matter. Do not canonicalize the English page to the Korean page.
9. **Channel version.** Adapt, do not copy, for Naver. Keep the source link and contact CTA. Store under `docs/editorial/distribution/naver/`, which Jekyll excludes.
10. **Rendered review.** Build with an isolated bundle, open the page in a browser at desktop and mobile widths, check diagrams, links, canonical, hreflang, and the contact path.
11. **Approved publication.** Codex or the author approves the exact revision. Commit the reviewed files.
12. **URL and ID ledger.** Record the public URL, publication date, channel IDs, and canonical URL in the distribution manifest.
13. **Check index, traffic, and enquiries.** Register or check Search Console and Naver Search Advisor where authorized. Review traffic and enquiries without inventing attribution.

## Rules

- Never fabricate personal anecdotes, customers, metrics, pricing, or performance results.
- Do not copy a long third-party translation. Link and attribute instead.
- Do not claim a 301 redirect from a Jekyll redirect plugin on GitHub Pages; it produces a static redirect document.
- Do not treat employer names in public career history as secrets by default. Do review customer names, internal systems, and non-public numbers.
- Do not publish exact internal operating numbers unless they are necessary and explicitly justified.
- Do not run unattended scrapes of internal repositories or customer systems.
- Do not claim a channel was posted until the public URL exists and is recorded.

## Scheduled rebuild

The GitHub Actions workflow keeps the existing push and manual triggers and adds a Monday 01:00 UTC schedule. That is 09:00 Asia/Manila and 10:00 Asia/Seoul. GitHub may delay scheduled runs.

Scheduled workflows run only from the default branch. In a public repository, GitHub can disable a scheduled workflow after 60 days without repository activity; see [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

The schedule only rebuilds the site from `_posts` already tracked in Git. `future: false` in `_config.yml` is a date gate, not a review or approval gate: at build time it hides posts whose date is in the future. It does not verify that anything was reviewed or approved.

As of 2026-11-08, no future-dated post is queued in Git. The weekly rebuild therefore publishes zero new posts today. This workflow is configured for future use; it is not proof of ongoing weekly AI production.

The weekly rebuild schedules Korean `_posts` only. English companion pages live under `en/` as Jekyll pages with their own dates, so a future date on an English page is not an embargo and is not date-gated by `_posts` scheduling. Do not merge an English companion page before its intended public date.

The schedule does not create new AX experiences, log in to Naver or Medium, or verify publication on those channels. Merge and deploy the workflow change before expecting the schedule to run.

Naver's native scheduling has been observed to allow dates up to one year ahead in ten-minute increments. That can serve as a weekly distribution queue after copy approval, but no Naver post is scheduled until the real platform IDs and dates are recorded in the distribution manifest. Do not change the configured times or claim a scheduled run before then.
