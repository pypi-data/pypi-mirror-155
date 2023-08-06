_language = 'en'

LANGUAGES = [ENG := 'en',
             ESP := 'es',
             ]


def lang() -> str:
    return _language


def define_lang(language: str) -> None:
    global _language
    if language not in LANGUAGES:
        raise ValueError('Invalid language')
    _language = language


def all_langs() -> str:
    return LANGUAGES
