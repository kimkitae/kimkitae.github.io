# RAG search diagnostics lab

Offline reproduction of one retrieval bug from the 2024 RAG prototype: FAISS
returns fewer than `k` neighbours when the index is small, pads the missing
labels with `-1`, and the original Python filter `if i < len(chunks)` accepts
`-1` and reads `chunks[-1]`.

Two synthetic 2-D vectors and two chunk records are enough. No embedding model,
LLM, network, or API key is involved. This proves label handling, not semantic
retrieval quality or generation quality.

The fixture deliberately sets `ntotal = 2 < k = 5`. The original HNSW index
size in 2024 is unknown, so this is not evidence that the bug triggered in
production. A large index is not automatically safe: IVF with a small `nprobe`
can search too few candidates, and HNSW with a small `efSearch` or a filter
that removes candidates can also pad. See the [FAISS
FAQ](https://github.com/facebookresearch/faiss/wiki/FAQ) and the
[Index API](https://faiss.ai/cpp_api/struct/structfaiss_1_1Index.html).
Filtered-search behavior depends on the index and filter implementation and is
not measured here.

## Run

From the repository root, with Python 3.12:

```bash
python3 -m venv /tmp/rag-lab-venv
source /tmp/rag-lab-venv/bin/activate
pip install -r examples/rag-search-diagnostics/requirements.txt
python -m unittest discover -s examples/rag-search-diagnostics -v
python examples/rag-search-diagnostics/lab.py
```

The pins match the 2026 reproduction: `faiss-cpu==1.15.1`, `numpy==2.5.4`.

## Expected results

Both `IndexFlatL2(2)` and `IndexHNSWFlat(2, 32)` return five labels for `k=5`:

```text
labels = [0, 1, -1, -1, -1]
```

The original filter maps that to the last chunk four times total: one real hit
plus three copies from the `-1` labels.

```text
original_filter = [cancel_order.py, archive_order.py, archive_order.py,
                   archive_order.py, archive_order.py]
bounded_filter  = [cancel_order.py, archive_order.py]
```

The empty-index case is a deliberately inconsistent fixture: the index holds
zero vectors while the two chunk metadata records are retained. It is not a
normal path of the original code. `create_index` returns `(None, None)` when no
embedding succeeds, and with empty metadata the original filter would raise
`IndexError` instead of inventing a chunk. This fixture models loading an index
and its metadata separately, where all five `-1` labels pass `i < len(chunks)`
and resolve to `chunks[-1]`.

```text
labels          = [-1, -1, -1, -1, -1]
original_filter = [archive_order.py, archive_order.py, archive_order.py,
                   archive_order.py, archive_order.py]
bounded_filter  = []
```

A mismatch between index and metadata should be checked before search; a
bounds check alone does not detect same-length reordered metadata.

`metric` compares cosine and squared L2 on two unit vectors:

```text
cosine = 0.6
l2_squared = 0.8
identity_2_minus_2cos = 0.8
score_1_over_1_plus_l2_squared = 0.5556
```

The last value is an arbitrary transform, not a probability that the answer is
correct.

## Limitations

- The vectors and chunks are synthetic, not actual embeddings. `faiss-cpu`
  returns the same sentinel behavior for real embeddings, but this lab does not
  measure recall or answer quality.
- The test asserts behavior observed with the pinned versions. Other FAISS
  builds may change warning text or distance formatting, not the `-1` contract.
- The original source does not define `chunk_text`, so chunk units and the
  effect of `[:max_chunks_per_script]` are not reproduced here. The original
  also joins the top three chunk contents and truncates at 3000 characters;
  whether those chunks could reach that limit is unknown, and this lab does not
  reproduce truncation.
- Padded distances are near the float32 maximum (about `3.4028e38`). The
  article's `1 / (1 + d²)` transform printed to four decimals shows `0.0000`,
  which is not proof of padding: a genuinely low score can round the same way.
  Check the raw `-1` labels.
- The tests are executed by the reviewing environment. This README records the
  expected output, not a claim that a run already happened.
