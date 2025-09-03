import math
from config import LETTERS_EXT, KAMEA_SQUARES, alpha_index, PLANETARY_MAP, ROSE_CROSS_MAP
from core import get_letter_position


# ---------------------------
# 1. Classic (Austin Osman Spare)
# ---------------------------
def classical(text, cx, cy, radius, rotation_deg=0):
    """
    Classic method:
    - Places each LETTER of the phrase around a circle.
    - Works ONLY with letters (A–Z, Ñ, etc.).
    - Digits are ignored.
    """
    points = [get_letter_position(ch, cx, cy, radius, rotation_deg) for ch in text if ch.isalpha()]
    if not points:
        raise ValueError("Classic method requires at least one valid letter (A–Z).")
    return points


# ---------------------------
# 2. Numeric (Pythagorean numerology)
# ---------------------------
def reduce_number(n: int) -> int:
    """Reduce a number to a single digit (1–9)."""
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def numeric(text, cx, cy, radius, rotation_deg=0):
    """
    Numeric method:
    - Converts each letter to a number (A=1 ... I=9, J=1 ... R=9, S=1 ... Z=8).
    - Digits in the text are reduced directly to 1–9.
    - If input is empty or has no valid characters → raises ValueError.
    """
    mapping = {ch: (i % 9) + 1 for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
    points = []

    for ch in text:
        if ch.isdigit():
            value = reduce_number(int(ch))
        elif ch in mapping:
            value = mapping[ch]
        else:
            continue
        angle = (value / 9) * (2 * math.pi) - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))

    if not points:
        raise ValueError("Numeric method requires at least one digit (0–9) or valid letter (A–Z).")

    return points


# ---------------------------
# 3. Planetary (Golden Dawn correspondences)
# ---------------------------
def planetary(text, cx, cy, radius, rotation_deg=0):
    """
    Planetary method:
    - Each letter is assigned to a planet based on Golden Dawn correspondences.
    - Works ONLY with letters (A–Z). Digits are ignored.
    - If input has only digits → raises ValueError.
    """
    planets = list(PLANETARY_MAP.keys())
    points = []

    for ch in text:
        for idx, planet in enumerate(planets):
            if ch in PLANETARY_MAP[planet]:
                angle = (idx / len(planets)) * (2 * math.pi) - math.pi / 2
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                points.append((x, y))

    if not points:
        raise ValueError("Planetary method requires at least one valid letter mapped to a planet (A–Z).")

    return points


# ---------------------------
# 4. Kamea (planetary magic squares)
# ---------------------------
def kamea(text, cx, cy, radius, rotation_deg=0, planet="jupiter"):
    """
    Kamea method:
    - Uses the chosen planet's magic square (e.g. Jupiter 4x4, Saturn 3x3).
    - Works with both letters and digits.
    - If no valid characters are found → raises ValueError.
    """
    if planet not in KAMEA_SQUARES:
        raise ValueError(f"Unknown planet: {planet}")

    square = KAMEA_SQUARES[planet]
    size = len(square)
    mapping = {LETTERS_EXT[i]: (i % (size*size)) + 1 for i in range(len(LETTERS_EXT))}
    cell_size = (radius * 2) / size
    top_left_x, top_left_y = cx - radius, cy - radius
    points = []

    for ch in text:
        if ch in mapping:
            target = mapping[ch]
        elif ch.isdigit():
            target = int(ch)
        else:
            continue

        for row in range(size):
            for col in range(size):
                if square[row][col] == target:
                    x = top_left_x + col * cell_size + cell_size/2
                    y = top_left_y + row * cell_size + cell_size/2
                    points.append((x, y))

    if not points:
        raise ValueError(f"Kamea method requires valid letters or digits that fit in the {planet.title()} Kamea.")

    return points


# ---------------------------
# 5. Rosicrucian (Rose Cross Alphabet inspired)
# ---------------------------
def rosicrucian(text, cx, cy, radius, rotation_deg=0):
    """
    Rosicrucian method:
    - Inspired by the Rose Cross Lamen.
    - Works ONLY with letters A–Z.
    - If input has only digits → raises ValueError.
    """
    points = []
    step = radius / 6

    for ch in text:
        if ch in ROSE_CROSS_MAP["up"]:
            idx = ROSE_CROSS_MAP["up"].index(ch)
            points.append((cx, cy - (idx+1) * step))
        elif ch in ROSE_CROSS_MAP["down"]:
            idx = ROSE_CROSS_MAP["down"].index(ch)
            points.append((cx, cy + (idx+1) * step))
        elif ch in ROSE_CROSS_MAP["right"]:
            idx = ROSE_CROSS_MAP["right"].index(ch)
            points.append((cx + (idx+1) * step, cy))
        elif ch in ROSE_CROSS_MAP["left"]:
            idx = ROSE_CROSS_MAP["left"].index(ch)
            points.append((cx - (idx+1) * step, cy))
        elif ch in ROSE_CROSS_MAP["center"]:
            idx = ROSE_CROSS_MAP["center"].index(ch)
            angle = (idx / len(ROSE_CROSS_MAP["center"])) * 2 * math.pi
            points.append((cx + (step * math.cos(angle)), cy + (step * math.sin(angle))))

    if not points:
        raise ValueError("Rosicrucian method requires at least one valid letter (A–Z). Digits are not supported.")

    return points
