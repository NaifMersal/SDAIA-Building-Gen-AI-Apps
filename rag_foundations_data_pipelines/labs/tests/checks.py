import numpy as np

# Lab 1
def check_lab_1_1(scenario_1, scenario_2, scenario_3, scenario_4):
    assert scenario_1.lower() == "pymupdf", "Scenario 1: Which framework processes at <1ms/page?"
    assert scenario_2.lower() == "docling", "Scenario 2: Which has 97.9% table accuracy?"
    assert scenario_3.lower() == "unstructured", "Scenario 3: Which supports the most formats?"
    assert scenario_4.lower() == "docling", "Scenario 4: Which runs locally with best table extraction?"
    print("✅ All correct!")

def check_lab_1_4(result):
    assert "info@example.com" not in result, "Emails should be removed"
    assert "https://" not in result, "URLs should be removed"
    assert result.strip().endswith("keep."), f"Content should be preserved. Got: {result}"
    print("✅ All cleaning rules working!")

def check_lab_1_5(doc):
    assert doc is not None, "Function should return a Document"
    assert doc.doc_type == "markdown", f"Expected 'markdown', got '{doc.doc_type}'"
    assert "RAG" in doc.content, "Content should contain the markdown text"
    assert doc.title == "My Research Notes", f"Title should be extracted from # heading, got: {doc.title}"
    print("✅ Markdown extractor working!")

# Lab 2
def check_lab_2_4(chunker1, chunker2, chunker3):
    from abc import ABC
    # We can't easily import the classes from the notebook, but we can check the class names or types if they are passed
    assert chunker1.__class__.__name__ == "RecursiveChunker", f"Expected RecursiveChunker, got {type(chunker1)}"
    assert chunker2.__class__.__name__ == "FixedSizeChunker", f"Expected FixedSizeChunker, got {type(chunker2)}"
    assert chunker3.__class__.__name__ == "FixedSizeChunker"
    print("✅ ChunkerFactory working correctly!")

def check_lab_2_5(result):
    assert result["total_tokens"] == 1_500_000, "Check your token calculation"
    assert abs(result["cost_usd"] - 0.03) < 0.001, "Check your cost calculation"
    print("✅ Cost calculator working!")

def check_lab_2_6(summary):
    # Deterministic fixed example so the check is independent of the embedding model:
    #   retrieved = ["d3", "d1", "d7", "d2", "d9"]  (best-first),  relevant = {"d1", "d2"}
    assert summary is not None, "Build the summary dict from your metric functions"
    assert abs(summary["recall_at_2"] - 0.5) < 1e-9, \
        "recall@2 should be 0.5 — only 1 of the 2 relevant ids is in the top 2"
    assert abs(summary["recall_at_5"] - 1.0) < 1e-9, \
        "recall@5 should be 1.0 — both relevant ids are in the top 5"
    assert abs(summary["hit_rate_at_3"] - 1.0) < 1e-9, "hit_rate@3 should be 1.0"
    assert abs(summary["mrr"] - 0.5) < 1e-9, "MRR should be 0.5 — first relevant id is at rank 2"
    print("✅ Recall@K / Hit Rate / MRR working!")

# Lab 3
def check_lab_3_3(filtered_results):
    assert filtered_results is not None, "Call store.search with filter_conditions"
    assert len(filtered_results) > 0, "Should find at least one result"
    assert all(r['metadata']['section'] == 'architecture' for r in filtered_results), \
        "All results should be from 'architecture' section"
    print("✅ Metadata filtering working!")

def check_lab_3_4(result):
    assert result is not None, "Should return a result dict"
    assert "answer" in result, "Result should have an 'answer' key"
    assert "sources" in result, "Result should have a 'sources' key"
    print("✅ Score threshold filtering working!")

def check_lab_3_4_dedup(initial_count, final_count):
    assert initial_count == final_count, f"Count changed from {initial_count} to {final_count}. Check your dedup logic."
    print("✅ Dedup check complete!")

# Lab 4
def check_lab_4_2(result):
    assert result is not None and len(result) > 0, "Should return fused results"
    print("✅ Weighted RRF working!")

def check_lab_4_5(variations):
    assert len(variations) >= 4, f"Expected at least 4 variations, got {len(variations)}"
    assert variations[0] == "What is chunking in RAG?", "First should be original query"
    print("✅ Query expansion working!")

# Lab 5
def check_lab_5_4(analysis):
    # Retrieval is scored with DeepEval's Contextual* metrics (LLM-as-judge),
    # so we only assert the per-query summary was populated, not exact scores.
    assert analysis is not None, "Should return results"
    assert len(analysis) > 0, "Should analyze at least one query"
    assert all(r.get('contextual_precision') is not None for r in analysis), \
        "Run ContextualPrecisionMetric for each query"
    assert all(r.get('passed') is not None for r in analysis), \
        "Determine pass/fail for each query"
    print("✅ Per-query retrieval analysis working!")

def check_lab_5_6(suite_results):
    # Generation is scored with DeepEval's Faithfulness + AnswerRelevancy metrics.
    assert suite_results is not None
    assert len(suite_results) > 0, "Should evaluate at least one response"
    assert all(r.get('faithfulness') is not None for r in suite_results), \
        "Run FaithfulnessMetric for each response"
    assert all(r.get('relevancy') is not None for r in suite_results), \
        "Run AnswerRelevancyMetric for each response"
    assert all(r.get('passed') is not None for r in suite_results), \
        "Determine pass/fail for each response"
    print("✅ Generation eval suite working!")

# Lab 6
def check_lab_6_3(optimal):
    assert optimal is not None, "Should return a config"
    # We now accept M=32 or 64 as optimal depending on the real hardware speed
    assert optimal['M'] in [32, 64], f"Expected M=32 or 64, got {optimal['M']}"
    assert 'ef_construction' in optimal or 'ef_search' in optimal, "Should include an EF parameter"
    print("✅ Configuration optimizer working!")

def check_lab_6_4(results):
    assert results is not None, "Should return a results dict"
    for k in ("flat", "hnsw", "sq8"):
        assert k in results, f"Missing index type: {k}"
        assert results[k].get("recall") is not None, f"{k}: compute recall@10"
        assert results[k].get("search_ms") is not None, f"{k}: measure search latency"
    # Flat is exact => it IS the ground truth, so recall@10 must be 1.0.
    # HNSW/SQ8 recall is checked for presence only (hardware/seed variance).
    assert abs(results["flat"]["recall"] - 1.0) < 1e-6, "Flat (exact) recall@10 must be 1.0"
    print("✅ FAISS quantization benchmark working!")
