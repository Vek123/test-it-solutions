__all__ = ()

from transliterate import translit
from transliterate.base import registry, TranslitLanguagePack


class RusToEngSameLettersLanguagePack(TranslitLanguagePack):
    language_code = 'ru-en-same'
    language_name = 'Russian Translit'
    mapping = (
        'абвгеёикмнорстухшщъья0123569',
        'abbreenkmhopctyxwwbbrolzзsbq',
    )


registry.register(RusToEngSameLettersLanguagePack, force=True)


def normalize_str(s: str) -> str:
    s = s.lower()
    s = ''.join(filter(lambda x: x.isalnum(), s))
    return translit(s, 'ru-en-same')
