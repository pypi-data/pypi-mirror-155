"""Define sep_text."""
from typing import Tuple

from fastlid import fastlid
from logzero import logger


def sep_text(text: str, threshold: float = 0.001) -> Tuple[str, ...]:
    """Separate dual-laugnage texts.

    Args:
        text: stuff to work on
        threshold: confidence level to justify the existence of a language, setting to 0.0 may have unpredictable consequences
    Returns:
        2-tuple of separated texts
        sep_text.langs also set to lang pairs
    """
    text = str(text)
    fastlid.set_languages = None

    try:
        lang_pairs, conf = fastlid(text, k=2)
    except Exception as exc:
        logger.exception(exc)
        raise

    # this wont happen? "un" is for polyglot?
    if "un" in lang_pairs:
        # replace 'un' with 'en'
        lang_pairs = [*map(lambda x: "en" if x in ["un"] else x, lang_pairs)]

        # dedup
        lang_pairs = [*dict.fromkeys(lang_pairs)]

    if len(lang_pairs) == 1:
        sep_text.langs = lang_pairs
        sep_text.conf = conf[:1]
        return (text,)

    # confidence too slow
    if conf[1] < threshold:
        sep_text.langs = lang_pairs[:1]
        sep_text.conf = conf[:1]
        return (text,)

    # do separation
    fastlid.set_languages = lang_pairs

    text1 = []
    text2 = []
    lines = [_ for _ in text.splitlines() if _.strip()]
    lang1, lang2 = lang_pairs
    for line in lines:
        lang, _ = fastlid(line)
        if lang in [lang1]:
            text1.append(line)
        else:
            text2.append(line)

    sep_text.langs = lang_pairs
    sep_text.conf = conf

    return "\n".join(text1), "\n".join(text2)
