from src.ranker import textrank


def test_ranker_works_correctly():
    expected_output = []
    documents = ["hello", "goodbye"]
    output = textrank(documents)
    assert expected_output == output, f"Expected empty output but got {output}"
