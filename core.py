import unicodedata, re, math
from config import ALPHABET, alpha_index

def preserve_special_characters(s: str) -> str:
    """Preserve Spanish special characters (Ñ, Ç, Á...) in uppercase form."""
    replacements = {
        "á": "Á", "é": "É", "í": "Í", "ó": "Ó", "ú": "Ú", "ü": "Ü",
        "Á": "Á", "É": "É", "Í": "Í", "Ó": "Ó", "Ú": "Ú", "Ü": "Ü",
        "ñ": "Ñ", "Ñ": "Ñ", "ç": "Ç", "Ç": "Ç"
    }
    result = ""
    for ch in s:
        if ch in replacements:
            result += replacements[ch]
        else:
            nfkd = unicodedata.normalize("NFD", ch)
            base = "".join(c for c in nfkd if not unicodedata.combining(c))
            result += base
    return result

def normalize_text(phrase: str) -> str:
    """Uppercase and filter only letters/numbers allowed in the alphabet."""
    s = preserve_special_characters(phrase.upper())
    s = re.sub(r"[^A-ZÑÇÁÉÍÓÚÜ0-9]", "", s)
    return s

def get_letter_position(ch, cx, cy, radius, rotation_deg=0):
    """Position a letter around a circle."""
    idx = alpha_index[ch]
    total_chars = len(ALPHABET)
    angle = (idx / total_chars) * (2 * 3.14159) - 3.14159 / 2
    angle += rotation_deg * 3.14159 / 180
    return cx + radius * math.cos(angle), cy + radius * math.sin(angle)