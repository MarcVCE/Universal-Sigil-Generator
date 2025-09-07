# ✨ Universal Sigil Generator

A desktop application to generate magical sigils in different traditional styles.  
Built with **Python + Tkinter + Pillow**, this tool allows you to create, visualize and save your personal sigils, with optional synchronization to **planetary hours and solar decanates**.

---

## 🔮 Features

- Multiple **sigil generation methods**:
  - **Classical (Austin Osman Spare)** → Removes vowels and duplicates, places unique consonants around a circle.
  - **Numeric (Pythagorean numerology)** → A–Z reduced to numbers 1–9, digits also reduced.
  - **Planetary (Golden Dawn)** → Letters mapped to the 7 classical planets.
  - **Kamea (planetary magic squares)** → Path traced on planetary squares (3×3 to 9×9), supports **Latin** and **Hebrew** alphabets.
  - **Rosicrucian (Rose Cross)** → Based on the Rose Cross Lamen layout.
- Two visual **modes**:
  - *Modern* → colored glow according to chosen intention.
  - *Traditional* → black & white.
- Optional **internal guide lines**:
  - Kamea → full planetary grid.
  - Numeric → 9 radial divisions.
  - Planetary → 7 radial divisions.
  - Rosicrucian → 4 arms of the cross.
  - Classical → alphabetic divisions.
- Choose from different **intentions** (prosperity, passion, protection, creativity, healing).
- **Planetary influence support**:
  - Automatically detects **planetary hour ruler** and **solar decan ruler** (via Astral + Swiss Ephemeris).
  - Flexible mode → preselects decan planet but allows manual override.
  - Strict mode → locks the Kamea planet to the decan ruler.
- Export in multiple **versions**:
  - Normal
  - Inverted (⚠ guide lines may not be visible, faithful to ritual inversion)
  - Black & White
  - Transparent background
- Clean, cross-platform **GUI** built with Tkinter.

---

## 📦 Installation

1. Clone this repository or download the project files:

   ```bash
   git clone https://github.com/MarcVCE/universal-sigil-generator.git
   cd universal-sigil-generator

2. (Optional) Create a virtual environment:
   
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   
3. Install the requirements:
   
   ```bash
   pip install -r requirements.txt
   sudo apt-get install python3-tk  # ⚠ On Linux you may also need the Tkinter system package

---

## ▶️ Usage

Run the main program:
python main.py

This will open the graphical interface where you can:

    * Enter your phrase/intention.

    * Select method, mode, and intention.

    * Choose which versions to generate.

    * Save your sigil(s) as PNG images.

## ⚠️ Warning
By default, the program is configured for Madrid, Spain.
If you want to adapt it to your own location, open the file core.py and update the values for:


    * City

    * Country

    * Latitude

    * Longitude
    
This will ensure planetary hours and solar decan calculations match your timezone.