# ✨ Universal Sigil Generator

A desktop application to generate magical sigils in different traditional styles.  
Built with **Python + Tkinter + Pillow**, this tool allows you to create, visualize and save your personal sigils.

---

## 🔮 Features

- Multiple **sigil generation methods**:
  - **Classical** → Letters placed around a circle.
  - **Numeric** → Based on Pythagorean numerology (A=1…9).
  - **Planetary** → Letters mapped to the 7 classical planets.
  - **Kamea** → Path traced on planetary magic squares (3×3 to 9×9).
  - **Rosicrucian** → Based on the Rose Cross alphabet layout.
- Two visual **modes**:
  - *Modern* (colored glow according to intention).
  - *Traditional* (black & white).
- Optional **internal guide lines**:
  - Kamea → shows the full grid of the chosen magic square.
  - Numeric → 9 radial divisions.
  - Planetary → 7 radial divisions.
  - Rosicrucian → 4 arms of the cross.
  - Classical → 26 radial divisions for the alphabet.
- Choose from different **intentions** (prosperity, passion, protection, creativity, healing).
- Export in multiple **versions**:
  - Normal
  - Inverted (⚠ guide lines may not be visible, faithful to ritual inversion)
  - Black & White
  - Transparent background
- Clean **GUI** built with Tkinter.

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
