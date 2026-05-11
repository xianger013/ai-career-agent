from app.utils.text_splitter import split_text


def test_split_text_with_overlap() -> None:
    text = "a" * 50 + "b" * 50 + "c" * 50
    chunks = split_text(text, chunk_size=80, overlap=20)

    assert len(chunks) == 3
    assert chunks[0].endswith("b" * 30)
    assert chunks[1].startswith("b" * 20)


def test_split_text_rejects_bad_overlap() -> None:
    try:
        split_text("hello", chunk_size=10, overlap=10)
    except ValueError as exc:
        assert "overlap" in str(exc)
    else:
        raise AssertionError("Expected ValueError")

