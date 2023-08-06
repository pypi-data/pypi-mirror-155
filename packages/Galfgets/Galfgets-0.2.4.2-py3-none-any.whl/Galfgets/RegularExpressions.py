import re

# Regular Expressions

_re_words           = re.compile(r"[a-zA-ZáéíóúÁÉÍÓÚ]*")
_re_digits          = re.compile(r"[\d|\d\.]*")