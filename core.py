import unicodedata, re, math
from config import ALPHABET, alpha_index, PLANETARY_ORDER, DECANATES
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun
import swisseph as swe

def preserve_special_characters(s: str) -> str:
    """
    Preserve special characters in extended Latin alphabets.
    Normalizes other letters by removing accents/diacritics.
    """
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

def normalize_text(phrase: str, alphabet="latin") -> str:
    """
    Normalize input text.
    - For Latin: keep A–Z, Ñ, Ç, accented vowels, Ü, and digits.
    - For Hebrew: keep א–ת and digits.
    """
    s = preserve_special_characters(phrase.upper())

    if alphabet == "latin":
        s = re.sub(r"[^A-ZÑÇÁÉÍÓÚÜ0-9]", "", s)
    elif alphabet == "hebrew":
        s = re.sub(r"[^אבגדהוזחטיכלמנסעפצקרשת0-9]", "", s)
    else:
        raise ValueError(f"Unsupported alphabet: {alphabet}")

    return s

def get_letter_position(ch, cx, cy, radius, rotation_deg=0):
    """
    Calculate Cartesian coordinates of a character placed around a circle.
    - ch: character index in ALPHABET
    - cx, cy: circle center
    - radius: circle radius
    - rotation_deg: optional global rotation
    """
    idx = alpha_index[ch]
    total_chars = len(ALPHABET)
    angle = (idx / total_chars) * (2 * math.pi) - math.pi / 2
    angle += rotation_deg * math.pi / 180
    return cx + radius * math.cos(angle), cy + radius * math.sin(angle)

# ---------------------------
# Classic (Spare) cleaning
# ---------------------------
def clean_spare_text(phrase: str) -> str:
    """
    Clean text for Spare's classic sigil method:
    - Remove vowels (including accented).
    - Remove duplicate consonants.
    - Keep only the first occurrence of each consonant.
    """
    vowels = set("AEIOUÁÉÍÓÚÜ")
    seen = set()
    result = []
    for ch in phrase.upper():
        if ch.isalpha() and ch not in vowels and ch not in seen:
            seen.add(ch)
            result.append(ch)
    return "".join(result)

# ---------------------------
# Planetary Hours + Decanates
# ---------------------------
def get_current_planetary_influence(city="Madrid", lat=40.4168, lon=-3.7038):
    """
    Calculate the current planetary hour ruler and solar decan ruler.

    - Uses Astral to compute sunrise and sunset for the given location/date.
    - Divides daytime and nighttime into 12 unequal hours to determine
      the planetary hour ruler, cycling through the Chaldean order.
    - Uses Swiss Ephemeris to calculate the Sun's zodiac position and
      determine the current solar decan ruler (each sign has 3 decans of 10°).

    ⚠️ Timezone is fixed here as "Europe/Madrid".
       If you need another location, change the string in LocationInfo manually.
    """
    # Fixed timezone: Europe/Madrid
    loc = LocationInfo(name=city, 
                       region="Spain", 
                       timezone="Europe/Madrid", 
                       latitude=lat, 
                       longitude=lon)

    today = datetime.now()  # naive datetime (system local time)
    s = sun(loc.observer, date=today)

    # Force naive datetimes for comparison
    sunrise = s["sunrise"].replace(tzinfo=None)
    sunset = s["sunset"].replace(tzinfo=None)

    # Planetary hour calculation
    is_day = sunrise <= today <= sunset
    duration = (sunset - sunrise)/12 if is_day else ((sunrise+timedelta(days=1)) - sunset)/12
    idx = int(((today - (sunrise if is_day else sunset)).total_seconds()) / duration.total_seconds())
    weekday = today.weekday()  # Monday=0
    ruler_index = (weekday + idx) % 7
    planetary_hour_ruler = PLANETARY_ORDER[ruler_index]

    # Solar decan calculation
    jd = swe.julday(today.year, today.month, today.day,
                    today.hour + today.minute/60.0)

    xx, _ = swe.calc_ut(jd, swe.SUN)  # xx[0] = longitude, xx[1] = latitude, xx[2] = distance
    lon_sun = xx[0]

    sign_idx = int(lon_sun // 30)           # zodiac sign index (0=Aries … 11=Pisces)
    degree_in_sign = lon_sun % 30           # degree inside current sign
    decan_idx = int(degree_in_sign // 10)   # 0, 1, or 2 (first, second, third decan)
    signs = list(DECANATES.keys())
    sign_name = signs[sign_idx]
    decan_ruler = DECANATES[sign_name][decan_idx]

    return {
        "planetary_hour": planetary_hour_ruler,
        "sign": sign_name,
        "decan_ruler": decan_ruler
    }