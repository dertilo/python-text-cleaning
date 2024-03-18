import pytest

from python_text_cleaning.asr_text_cleaning import Casing, VocabCasingAwareTextCleaner
from python_text_cleaning.character_mappings.text_cleaning import (
    CHARACTER_MAPPINGS,
    TextCleaner,
)

bad_dash = "–"  # noqa: RUF001


@pytest.mark.parametrize(
    "lang_input_output",
    [
        ("en", (f"Jon-Do{bad_dash}e's"), "Jon-Do-e's"),
        ("en", (f'Jon-Do{bad_dash}e"s'), "Jon-Do-e s"),
        ("de", f"Jon-Do{bad_dash}e's", "Jon-Do-e s"),
        ("de", "...der, die; das!?", " der die das "),
        ("ru", "this is a test", "дис ис а тест"),  # noqa: RUF001
        ("ru", "dwaja mat, pisdez", "дwая мат писдец"),  # noqa: RUF001
        ("es", "migüel mañanä", "migüel mañana"),
    ],
)
def test_text_character_mappings(lang_input_output: tuple[str, str, str]) -> None:
    lang, input_, output = lang_input_output
    assert CHARACTER_MAPPINGS[lang](input_) == output


@pytest.mark.parametrize(
    ("cleaner", "input_", "expected"),
    [
        (
            VocabCasingAwareTextCleaner(
                casing=Casing.lower,
                text_cleaner_name="de_no_sz",
                letter_vocab="bcds",
            ),
            "Daß ABC",
            "dss bc",
        ),
    ],
)
def test_text_cleaning(cleaner: TextCleaner, input_: str, expected: str) -> None:
    assert cleaner(input_) == expected
