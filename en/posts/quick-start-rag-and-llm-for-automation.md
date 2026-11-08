---
layout: post
title: "Debugging RAG Retrieval: When Two Chunks Become Five Results"
author: KimKitae
date: 2024-08-02 12:00:00 +0900
last_modified_at: 2026-11-08
lang: en
permalink: /en/posts/quick-start-rag-and-llm-for-automation/
translation_url: /posts/quick-start-rag-and-llm-for-automation/
description: A reproduced FAISS padding bug, the bounded fix, a diagnostic table for retrieval versus generation failures, and when deterministic keyword lookup beats RAG.
categories: [Automation, Testing, AI]
tags: [Testing, AI]
---

Rerunning the retrieval example from my 2024 post with two synthetic vectors produced five mapped results. The last document appeared four times. The filter had accepted FAISS's missing-neighbor label, `-1`, as a Python list index.

This is a diagnostic reproduction run while revising the article in 2026, not a documented production incident from 2024. It shows how incorrect evidence can enter a prompt before a model generates an answer. Changing the prompt would leave that path intact.

![Script collection, chunking, embeddings, vector search, and LLM response](/assets/img/posts/renewal/quick-start-rag-and-llm-for-automation.svg)

*Figure 1. Indexing and querying are separate paths. Failures happen in each path and in prompt construction.*

## The 2024 constraints and the choice

We needed to avoid sending data outside the environment, so we ran locally. The model was Llama 3, embeddings came from `mxbai-embed-large`, and the vector index was FAISS HNSW via `faiss-cpu`. Team members asked questions through a Slackbot instead of a separate WebUI, and the bot showed the retrieval results the model used alongside the answer.

We also considered fine-tuning. The original records 130GB of memory use when trying LoRA training with `Mlx-lm`. That number is an observation from one hardware and settings combination, not a general requirement for RAG. The more important judgment was different: because function signatures and examples changed often, rebuilding training data cost more than rebuilding a search index. That is why we chose RAG.

One invariant in the original code is worth preserving. `create_index` appends embeddings and chunk metadata in the same loop:

```python
embedding = get_embedding(chunk)
if embedding is not None:
    script_embeddings.append(embedding)
    script_chunks.append({"path": script["path"], "content": chunk})
```

If embedding fails, the chunk is not added either. If it succeeds, both are added. Vector order and metadata order therefore stay aligned. Filtering or sorting one side separately later produces a much harder bug: the retrieved content is relevant, but its file path points somewhere else. Any reindexing should keep this pairing.

Chunk parameters were `chunk_size=100`, `overlap=25`, capped per script by `[:max_chunks_per_script]` at the default 10. However, the original never defines `chunk_text`. The article cannot prove whether 100 and 25 are characters, tokens, or something else, or exactly how overlap is computed. What is certain is the cap. A long script can lose its later code from the index, and a function that exists only there will never be retrieved.

For illustration, suppose `chunk_text` produced only complete 100-character windows and advanced them by 75 characters. The original does not define this, so the assumption is an example only and does not establish the original's exact window count. A 1,100-character script would produce 14 complete windows starting at offsets 0, 75, …, 975. The cap of 10 keeps the first 10, which cover characters 0–775, leaving the remaining 325 characters out of the index. The original does not define partial-tail handling, so this calculation excludes it. Whether the real unit is tokens or characters, the cap creates a code region that cannot be retrieved.

## Searching with k=5 when only two neighbors exist

Here is the bug. The original search function defaulted to `k=10`; the reproduction uses `k=5` so the padding is visible with a small result set. The 2026 reproduction used `faiss-cpu==1.15.1`, `numpy==2.5.4`, and Python 3.12 with the original filter. It used two synthetic 2-D vectors and two chunk records, with no embedding model and no business data. The experiment proves label handling, not retrieval quality.

```python
import faiss
import numpy as np

vectors = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=np.float32)
query = np.array([[0.1, 0.0]], dtype=np.float32)

for make_index in (
    lambda: faiss.IndexFlatL2(2),
    lambda: faiss.IndexHNSWFlat(2, 32),
):
    index = make_index()
    index.add(vectors)
    distances, labels = index.search(query, 5)
    print(labels[0].tolist())
```

Both index types produce the same labels:

```text
[0, 1, -1, -1, -1]
[0, 1, -1, -1, -1]
```

The index contains two vectors but the query asks for five. FAISS returns the two real neighbors and pads the rest with `-1`. The [IndexFlat documentation](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexFlat.html) states that labels are padded with -1 when fewer neighbors exist. HNSW follows the same contract. For these synthetic inputs, the two real squared L2 distances compute to 0.01 and 0.81. The padded distance is near the float32 maximum, about 3.4028e38, so `1 / (1 + d²)` printed to four decimals shows `0.0000`. That is not mathematically exact zero.

This reproduction deliberately makes the vector count smaller than `k`. The original HNSW index size in production is unknown, so this article does not claim the bug occurred in 2024. A large index is not automatically safe: IVF with a low `nprobe` can search fewer than `k` candidates, and HNSW with a low `efSearch` or a filter that removes candidates can behave the same way ([FAISS FAQ](https://github.com/facebookresearch/faiss/wiki/FAQ), [Index API](https://faiss.ai/cpp_api/struct/structfaiss_1_1Index.html)). Generalizing to filtered search depends on the index and filter implementation, which this experiment did not measure.

The original filter looked like this:

```python
results = [
    (scripts[i], 1 / (1 + distances[0][j]))
    for j, i in enumerate(indices[0])
    if i < len(scripts)
]
```

`i < len(scripts)` does not reject negatives. `-1 < 2` is true, so `-1` passes, and `scripts[-1]` means the last element in Python. The mapping becomes:

```text
labels          = [0, 1, -1, -1, -1]
original filter = [cancel_order.py, archive_order.py,
                   archive_order.py, archive_order.py,
                   archive_order.py]
bounded filter  = [cancel_order.py, archive_order.py]
```

![Two chunks searched with k=5, -1 labels repeated as the last chunk, and the bounded fix](/assets/img/posts/renewal/rag-padding-bug.svg)

*Figure 2. The reproduced path. A passing `-1` becomes Python's last element, repeating the last chunk.*

Two real results inflate to five. The three padding labels copy the last chunk, so `archive_order.py` appears four times in total: one real hit and three copies. The original caller passes the top three into the context, so the prompt receives two real documents and one duplicated last document. The model can read that duplication as relevance. The log still reports “5 results,” so the output looks healthy.

The fix is one explicit bound:

```python
if 0 <= i < len(scripts)
```

The original caller already has an `if results: ... else: "no relevant scripts found"` branch. But once `-1` becomes the last chunk, the result list does not become empty while metadata remains, so that existing branch is never reached. The boundary cases split into three.

Fixing that bug still does not establish “no relevant document.” The original removes its score threshold with `filtered_results = results`. With a successful search and vectors in the index, even an unrelated question can return nearest neighbors. Handling an empty list differs from refusing an answer for insufficient evidence. Include unrelated questions as negative controls and validate an abstention rule separately.

- **Empty index, retained metadata**: `ntotal` is 0, but the search still fills the result with `-1`. If metadata remains, the original filter returns the last chunk. `create_index` returns `(None, None)` when no embedding succeeds, so this is not a normal historical path; it models loading an index and its metadata separately. To treat an empty index as “no results,” check `index.ntotal` before searching, or refuse to answer when the bounded list is empty.
- **Positive label out of range**: if the index and metadata list are updated separately, a label can exceed `len(scripts)`. The bounded check rejects that too.
- **Same-length reordering**: a bounds check cannot detect it. Verify the index-to-metadata correspondence before searching.

Log at least `index.ntotal`, the raw `labels`, the count after the bounded filter, and the context length that reached the prompt. A single “5 results” line cannot expose this bug. A difference between the original and bounded counts is itself a signal. A score of `0.0000` whose path repeats an earlier result is a hint of padding, but a genuinely low score can round the same way at four decimals, so confirm the raw `-1` labels instead of treating the score as proof.

The reproduction and tests live in [examples/rag-search-diagnostics](https://github.com/kimkitae/kimkitae.github.io/tree/main/examples/rag-search-diagnostics). The tests cover real Flat and HNSW padding, the original filter's repeated last chunk, the bounded filter, an empty index with retained metadata, an out-of-range positive label, and the difference between distance and score. Install `requirements.txt` and run them to compare the behavior yourself.

## Distance, score, and threshold are not the same thing

The original exposes `1 / (1 + distance)` as a relevance score. That transform only makes a smaller distance produce a larger number. It does not turn the value into a probability of correctness. FAISS L2 indexes return **squared** L2 distance. The [MetricType and distances](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances) documentation states this. The transform is therefore `1 / (1 + d²)`.

| Squared L2 distance | `1 / (1 + d²)` |
|---|---|
| 0.01 | 0.9901 |
| 0.81 | 0.5525 |
| 100 | 0.0099 |

The table shows only the arithmetic transformation. A value of 0.99 does not mean a 99% chance of a correct answer: change the embedding model, normalization, or data distribution, and the meaning of the same distance changes. Whether a value is useful depends on the index metric, model, data distribution, and what you measure, so do not read it as a universal threshold, calibrated confidence, or statistical quality claim. Instead, keep the index metric and the score transform consistent, then measure both ranking and whether the retrieved set contains the true answer.

Cosine similarity has the same trap. For normalized vectors, cosine 0.6 equals squared L2 distance 0.8, because `d² = 2 - 2·cos`. To use cosine, normalize both queries and documents and use a dot-product index, or convert the returned value correctly. Reading an unnormalized FAISS L2 distance as if it were cosine is the common mistake. A dot product of normalized vectors is cosine, but it is still not a probability.

## A table for separating retrieval from generation failures

When a RAG answer is wrong, tuning the prompt first often hides the cause. Check the evidence in this order.

| Symptom | Evidence to inspect first | Next action |
|---|---|---|
| The repository contains the answer, but retrieval misses it | index `ntotal`, chunk count, embedding failure logs, files cut by `[:max_chunks]` | Reindex and record chunks per file. Adjust the cap and chunk boundaries. |
| The relevant chunk appears only below the top results | returned labels and distances, `k`, whether query and documents use the same embedding model | Increase `k` to test reachability, then inspect query wording and chunk shape. |
| Top results are unrelated to the question | chunk previews, file paths, repeated results for the same query | Check whether chunks split functions. Include path and symbol names in the chunk. |
| The right function is retrieved, but the answer is wrong | the exact prompt context, chunk length, length after `truncate_context` | First check whether the chunk includes a path and signature; if needed, trim by tokens. |
| The answer names a function that does not exist | citations in the answer, mapping back to retrieved chunks | Require citations and check generated symbols against the repository. |
| The model answers when nothing was retrieved | result count after the bounded filter, empty-index state | Return “not found” when the bounded list is empty. |

Context truncation needs to be checked against the original configuration first. The original uses `max_chunk_size=100`, joins the `content` strings of the top three results with spaces, then cuts at 3000 characters. However, the article has no definition of `chunk_text`, so the chunk unit and its real length are unknown. If a chunk is 100 characters, three chunks plus two separators total at most 302 characters, so the 3000-character limit cannot explain a missing signature. The source also does not prove that a truncation event actually ran.

Another possible cause sits earlier. If chunks are smaller than a function, or `content` is joined without a file path, the model cannot tell which file or function it is reading. Inspect the actual retrieved chunks and the joined prompt before changing it. With larger chunks, the 3000-character limit can become the bottleneck again; in that case count both the real characters and the target model's tokens.

Index coverage and retrieval quality are also different. If a file is absent from the index, no amount of retrieval tuning will help. If the file is present but chunks cross function boundaries, retrieval becomes unstable. Check, in order: did the file enter the index, did the chunk appear in search results, did the chunk enter the prompt, and is the answer grounded in that evidence? This sequence reduces diagnostic cost.

## When RAG is overkill: a prebuilt keyword lookup

The last paragraph of the original describes another choice. A separate test-case Q&A service had the LLM extract keywords from a question and returned pre-generated data for those keywords, reducing context cost. That is closer to deterministic lookup than vector search.

The conditions for that design are clear. The answer is narrowed by a specific test-case name or identifier, a human can maintain the keyword-to-record mapping, and minimizing context is the goal. When the key is exact, a dictionary or an SQL equality lookup (`WHERE name = ?`) is enough. SQLite FTS is lexical ranked retrieval, not deterministic unique-record lookup; exact-key lookup, full-text lexical search, and semantic vector search are different tools. The keyword extraction in the original service still used an LLM. Making the downstream lookup exact does not make the whole service deterministic unless the extracted key is validated against an allowlist or schema. The cost is maintaining synonyms and phrasing variants, and handling expressions the keyword map has never seen. Embedding search takes the opposite tradeoff: it can find semantically similar text despite different wording, but exact versioning and explainability are harder.

In practice, combining them is a common design. Query by exact keys such as name, identifier, or tag first. Fall back to lexical or vector search only when no record matches. Or combine both result sets and rerank. A hybrid is not automatically cheaper and more accurate; that improvement has to be measured. The important decision is not “RAG is always better,” but whether the question is an identifier lookup or a semantic search.

A short decision list is enough:

- Is the answer identified by a unique name or ID? Try exact-key lookup (dictionary or SQL equality) first.
- Do many expressions refer to the same thing while the document set keeps growing? Embedding search has an advantage.
- Are exact versions and citations required? Apply keyword or metadata filters first.
- Does the answer require synthesizing several documents? That is where retrieval plus an LLM fits.
- Can the system refuse when retrieval is empty? The original already had a “not found” branch, but a `-1` that becomes the last chunk keeps the result list non-empty, so that branch is never reached.

## An illustrative AX decision table

Consider these illustrative requests when planning AI transformation (AX) in an academy.

| Request | Correct path | Why |
|---|---|---|
| How many students attended today? | authorized query against the current database | The answer needs current state; a generative model should not guess the number. |
| How does the make-up class rule work? | retrieval from a versioned, approved policy document with citation | The answer needs both the rule and the version it came from. |
| Approve this leave request. | permissioned state-changing workflow | Approval is an auditable exercise of authority, not a grant of judgment to an LLM. |

Collapsing all three into “ask the LLM” is the mistake. A current count belongs in a DB query, a policy explanation in approved retrieval with citations, and an approval action in a workflow with permissions and an audit log.

## What changes if you build this today

The original Ollama call put `temperature`, `top_p`, and `max_tokens` at the top level of the request. This article cannot establish how an unknown 2024 server handled those fields. The current official [/api/generate documentation](https://docs.ollama.com/api/generate) places runtime controls under `options` and names the generation limit `num_predict`. New code should separate them:

```python
data = {
    "model": model_name,
    "prompt": prompt,
    "system": system_prompt,
    "stream": False,
    "options": {
        "temperature": 0.0,
        "top_p": 0.5,
        "num_predict": 500,
    },
}
```

Temperature near zero favors grounded answers over creative ones. It does not guarantee factual correctness. Verifying that generated functions and parameters exist in the repository is still a separate step.

The scope of the reproduction is explicit. Two synthetic 2-D vectors prove the combination of FAISS label padding and Python negative indexing. They do not measure real embedding recall, LLM answer quality, or production performance. The 130GB figure is one environment's observation. The units behind chunk size 100 and overlap 25 are not defined in the original, so any character-window example is illustrative, not the 2024 production behavior.

What a reader can do immediately: log returned labels, discard `-1` and out-of-range labels, and test the path that refuses to answer when the index is empty. Then confirm that the retrieved context actually reached the prompt. Only after those two checks does comparing embedding models and prompts make sense.
