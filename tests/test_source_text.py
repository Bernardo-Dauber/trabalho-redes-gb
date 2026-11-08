from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "data" / "source.txt"


def test_source_text_is_printable_ascii_and_long_enough():
    text = SOURCE.read_bytes().decode("ascii")  # raises if any byte is not ASCII (D17)
    assert len(text) >= 12_500  # >= 100,000 message bits (D6)
    assert all(c == "\n" or " " <= c <= "~" for c in text)
