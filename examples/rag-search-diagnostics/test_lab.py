import unittest

import faiss

import lab


class SearchPaddingTests(unittest.TestCase):
    def test_flat_search_pads_missing_neighbours_with_minus_one(self):
        index = lab.build_index("flat")
        _, labels = lab.search(index)
        self.assertEqual(labels, [0, 1, -1, -1, -1])

    def test_hnsw_search_pads_missing_neighbours_with_minus_one(self):
        index = lab.build_index("hnsw")
        _, labels = lab.search(index)
        self.assertEqual(labels, [0, 1, -1, -1, -1])

    def test_original_filter_repeats_last_chunk(self):
        _, labels = lab.search(lab.build_index("flat"))
        self.assertEqual(
            lab.paths_original_filter(labels),
            [
                "cancel_order.py",
                "archive_order.py",
                "archive_order.py",
                "archive_order.py",
                "archive_order.py",
            ],
        )

    def test_bounded_filter_returns_only_real_chunks(self):
        _, labels = lab.search(lab.build_index("hnsw"))
        self.assertEqual(
            lab.paths_bounded_filter(labels),
            ["cancel_order.py", "archive_order.py"],
        )

    def test_bounded_filter_rejects_positive_metadata_index(self):
        labels = [0, 7, -1]
        self.assertEqual(lab.paths_original_filter(labels), ["cancel_order.py", "archive_order.py"])
        self.assertEqual(lab.paths_bounded_filter(labels), ["cancel_order.py"])

    def test_empty_index_with_retained_metadata_repeats_last_chunk(self):
        """Deliberately inconsistent fixture: zero vectors, two metadata records.

        Not a normal path of `create_index`, which returns (None, None) when no
        embedding succeeds; with empty metadata the original filter would raise
        IndexError instead of inventing a chunk. It models loading an index and
        metadata separately.
        """
        empty = faiss.IndexFlatL2(lab.VECTORS.shape[1])
        _, labels = lab.search(empty)
        self.assertEqual(labels, [-1, -1, -1, -1, -1])
        self.assertEqual(
            lab.paths_original_filter(labels),
            ["archive_order.py"] * 5,
        )
        self.assertEqual(lab.paths_bounded_filter(labels), [])

    def test_metric_demo_shows_squared_l2_not_confidence(self):
        metric = lab.metric_demo()
        self.assertEqual(metric["cosine"], 0.6)
        self.assertEqual(metric["l2_squared"], 0.8)
        self.assertEqual(metric["identity_2_minus_2cos"], 0.8)
        self.assertAlmostEqual(metric["score_1_over_1_plus_l2_squared"], 0.5556)
        self.assertLess(metric["score_1_over_1_plus_l2_squared"], 0.6)


if __name__ == "__main__":
    unittest.main()
