import math
from config import LETTERS_EXT, LETTERS_LATIN, LETTERS_HEBREW, KAMEA_SQUARES, PLANETARY_MAP, ROSE_CROSS_MAP
from core import get_letter_position, clean_spare_text, normalize_text

# ---------------------------
# 1. Classic (Austin Osman Spare)
# ---------------------------
def classical(text, cx, cy, radius, rotation_deg=0):
    """
    Classic sigil method (Austin Osman Spare inspired).
    
    Process:
    - Removes vowels and duplicate letters from the input phrase.
    - Keeps only unique consonants (first occurrence).
    - Places each consonant evenly spaced around a circle.
    
    Parameters:
        text (str): Input phrase.
        cx, cy (float): Circle center coordinates.
        radius (float): Circle radius.
        rotation_deg (float): Optional rotation in degrees.

    Returns:
        list[tuple]: List of (x, y) coordinates for the sigil path.
    """
    cleaned = clean_spare_text(text)
    points = [get_letter_position(ch, cx, cy, radius, rotation_deg) for ch in cleaned]
    if not points:
        raise ValueError("Classic method requires at least one valid consonant after cleaning.")
    return points

# ---------------------------
# 2. Numeric (Pythagorean numerology)
# ---------------------------
def reduce_number(n: int) -> int:
    """
    Reduce a number to a single digit (1–9).
    Example: 14 → 1 + 4 = 5
    """
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def numeric(text, cx, cy, radius, rotation_deg=0):
    """
    Numeric sigil method (Pythagorean numerology).

    Process:
    - Each letter A–Z is mapped cyclically to 1–9.
    - Digits are reduced recursively to a single digit (1–9).
    - Each value corresponds to a radial division of a circle.

    Parameters:
        text (str): Input phrase.
        cx, cy (float): Circle center coordinates.
        radius (float): Circle radius.
        rotation_deg (float): Optional rotation in degrees.

    Returns:
        list[tuple]: List of (x, y) coordinates for the sigil path.
    """
    text = normalize_text(text)
    mapping = {ch: (i % 9) + 1 for i, ch in enumerate(LETTERS_LATIN)}
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
        raise ValueError("Numeric method requires at least one digit or valid A–Z letter.")
    return points

# ---------------------------
# 3. Planetary (Golden Dawn correspondences)
# ---------------------------
def planetary(text, cx, cy, radius, rotation_deg=0):
    """
    Planetary sigil method (Golden Dawn correspondences).

    Process:
    - Each letter A–Z is mapped to one of the 7 classical planets,
      according to the Golden Dawn alphabetic planetary scheme.
    - The circle is divided into 7 equal planetary sectors.
    - Each letter determines a point in the sector of its planet.

    Parameters:
        text (str): Input phrase.
        cx, cy (float): Circle center coordinates.
        radius (float): Circle radius.
        rotation_deg (float): Optional rotation in degrees.

    Returns:
        list[tuple]: List of (x, y) coordinates for the sigil path.
    """
    text = normalize_text(text)
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
        raise ValueError("Planetary method requires valid A–Z letters mapped to a planet.")
    return points

# ---------------------------
# 4. Kamea (planetary magic squares)
# ---------------------------
def kamea(text, cx, cy, radius, rotation_deg=0, planet="jupiter", alphabet="latin"):
    """
    Kamea method:
    - Uses the chosen planet's magic square (e.g. Jupiter 4x4, Saturn 3x3).
    - Supports both Latin and Hebrew alphabets.
    - Each character is mapped to a number, which corresponds to a cell in the square.
    - If no valid characters are found → raises ValueError.
    """
    if planet not in KAMEA_SQUARES:
        raise ValueError(f"Unknown planet: {planet}")

    square = KAMEA_SQUARES[planet]
    size = len(square)

    # Select alphabet string based on user choice
    if alphabet == "latin":
        letters = LETTERS_EXT
    elif alphabet == "hebrew":
        letters = LETTERS_HEBREW
    else:
        raise ValueError(f"Unsupported alphabet: {alphabet}")

    # Map letters to numbers (cycled over square size²)
    mapping = {letters[i]: (i % (size * size)) + 1 for i in range(len(letters))}

    cell_size = (radius * 2) / size
    top_left_x, top_left_y = cx - radius, cy - radius
    points = []

    # Map input text into Kamea coordinates
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
        raise ValueError(
            f"Kamea method requires valid characters in {planet.title()} Kamea with {alphabet} alphabet."
        )

    return points

# ---------------------------
# 5. Rosicrucian (Rose Cross Alphabet inspired)
# ---------------------------
def rosicrucian(text, cx, cy, radius, rotation_deg=0):
    """
    Rosicrucian sigil method (Rose Cross alphabet).

    Process:
    - Letters are grouped into "arms" of a cross (up, down, left, right) and center.
    - Each group of letters corresponds to a linear offset or angular placement.
    - The cross arms radiate outward from the center of the circle.

    Parameters:
        text (str): Input phrase.
        cx, cy (float): Center coordinates.
        radius (float): Circle radius (used to calculate step size).
        rotation_deg (float): Reserved for compatibility.

    Returns:
        list[tuple]: List of (x, y) coordinates for the sigil path.
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
        raise ValueError("Rosicrucian requires valid A–Z letters.")
    return points
