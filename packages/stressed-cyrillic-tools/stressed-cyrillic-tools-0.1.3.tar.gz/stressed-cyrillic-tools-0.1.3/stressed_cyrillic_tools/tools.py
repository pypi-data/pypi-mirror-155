import re
import unicodedata

def is_accented(word: str):
    """Returns True if the word has an accent (also detects if the word has a grave accent."""
    return unaccentify(word) != word

def is_acute_accented(phrase: str):
    """Returns True if the phrase has an acute accent."""
    return '\u0301' in phrase

def has_only_one_syllable(word: str):
    """Returns True if the word has only one syllable ( == at most one vowel)
    Accepts only one word without spaces."""
    assert " " not in word

    word_lower = word.lower()
    vowels = 0
    for char in word_lower:
        if char in "аоэуыяеёюи":
            vowels += 1
    return vowels <= 1

def has_acute_accent_or_only_one_syllable(word: str):
    """Returns True if the word (probably) has been stressed or does not need to be stressed:
    This is the case if it has an acute accent or only one syllable"""
    return is_acute_accented(word) or has_only_one_syllable(word)

# Unaccentifier written by Roman Susi
# Taken from https://stackoverflow.com/questions/35942129/remove-accent-marks-from-characters-while-preserving-other-diacritics
ACCENT_MAPPING = {
    '́': '',
    '̀': '',
    'а́': 'а',
    'а̀': 'а',
    'е́': 'е',
    'ѐ': 'е',
    'и́': 'и',
    'ѝ': 'и',
    'о́': 'о',
    'о̀': 'о',
    'у́': 'у',
    'у̀': 'у',
    'ы́': 'ы',
    'ы̀': 'ы',
    'э́': 'э',
    'э̀': 'э',
    'ю́': 'ю',
    '̀ю': 'ю',
    'я́́': 'я',
    'я̀': 'я',
}

ACCENT_MAPPING = {unicodedata.normalize(
    'NFKC', i): j for i, j in ACCENT_MAPPING.items()}


def unaccentify(s):
    source = unicodedata.normalize('NFKC', s)
    for old, new in ACCENT_MAPPING.items():
        source = source.replace(old, new)
    return source

def remove_accent_if_only_one_syllable(s: str):
    """Removes the accent from words like что́, which are usually not set in texts.
    Also works with complete texts (splits by space)"""
    if " " in s:
        words = s.split(" ")
        fixed_words = []
        for word in words:
            fixed_words.append(remove_accent_if_only_one_syllable(word))
        return " ".join(fixed_words)

    s_unaccented = unaccentify(s)
    if has_only_one_syllable(s_unaccented):
        return s_unaccented
    else:
        return s

def has_cyrillic_letters(s: str):
    """Returns True if the string has at least one Cyrillic letter."""
    m = re.findall(r'[А-я]+', s)
    return m != []

def convert_ap_accent_to_real(word: str) -> str:
    """This replaces the accents marked with apostrophes with a real acute accent."""
    return word.replace("'", "\u0301")

def remove_apostrophes(word: str) -> str:
    """Removes apostrophes from words like удар'ения."""
    return word.replace("'", "")

def remove_yo(word: str) -> str:
    """This replaces ё with the letter е (also works for upper case)."""
    return word.replace("ё", "е").replace("Ё", "Е")

def get_lower_and_without_yo(word: str) -> str:
    """Returns the lower case version of the word and the version without yo."""
    return remove_yo(unaccentify(word)).lower()

def has_two_accent_stress_marks(word: str) -> bool:
    """Returns True if the word has at least two accent marks."""
    return word.count("\u0301") >= 2

def is_unhelpfully_unstressed(word: str) -> bool:
    """Returns True if the word would be of no use in a stress dictionary."""

    if " " in word:
        # Return True if all of the words in the phrase are unhelpfully unstressed
        return all(is_unhelpfully_unstressed(word) for word in word.split(" "))

    if "ё" in word or "Ё" in word:
        return False
    if ("е" in word or "Е" in word) and has_only_one_syllable(word):
        # The word лес tells us that it is not written like "лёс"
        return False
    return not is_accented(word)