from typing import List

from src.ranker import textrank


def test_ranker_works_correctly() -> None:
    expected_output: List[str] = []
    documents = ["hello", "goodbye"]
    output = textrank(documents)
    assert expected_output == output, f"Expected empty output but got {output}"
