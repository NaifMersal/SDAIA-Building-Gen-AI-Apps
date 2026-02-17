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
    assert analysis is not None, "Should return results"
    assert all(r['hit'] is not None for r in analysis), "Hit should be calculated"
    assert all(r['precision'] is not None for r in analysis), "Precision should be calculated"
    print("✅ Per-query analysis working!")

def check_lab_5_6(suite_results):
    assert suite_results is not None
    assert all(r['faithfulness'] is not None for r in suite_results), "Calculate faithfulness"
    assert all(r['passed'] is not None for r in suite_results), "Determine pass/fail"
    print("✅ Eval suite working!")

# Lab 6
def check_lab_6_3(optimal):
    assert optimal is not None, "Should return a config"
    # We now accept M=32 or 64 as optimal depending on the real hardware speed
    assert optimal['M'] in [32, 64], f"Expected M=32 or 64, got {optimal['M']}"
    assert 'ef_construction' in optimal or 'ef_search' in optimal, "Should include an EF parameter"
    print("✅ Configuration optimizer working!")
