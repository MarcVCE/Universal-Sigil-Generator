import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
from config import VERSION_DESCRIPTIONS, INTENTION_COLORS, KAMEA_SQUARES, PLANET_NAMES
from core import normalize_text, get_current_planetary_influence
from methods import classical, numeric, planetary, kamea, rosicrucian
from draw import generate_sigil

def run_gui():
    """
    Launch the Tkinter graphical interface for the Universal Sigil Generator.

    GUI Features:
    - Text input for phrase/intention.
    - Dropdowns for:
        * Mode: "modern" (colored glow) or "traditional" (black & white).
        * Intention: color theme (protection, passion, prosperity, etc.).
        * Method: classical, numeric, planetary, kamea, rosicrucian.
    - Kamea-specific options:
        * Planet selector (3x3 Saturn … 9x9 Moon).
        * Alphabet selector (Latin or Hebrew).
    - Planetary influence options:
        * Checkbox: "Use current planetary influence (hour & decan)".
        * Checkbox: "Strict mode" → locks Kamea to the decan’s planet.
    - Output controls:
        * Checkboxes for export versions (normal, inverted, b/w, transparent).
        * Checkbox to show/hide guide lines.
    - Generate button: saves PNG(s) to chosen file path.
    """
    root = tk.Tk()
    root.title("Universal Sigil Generator")
    root.configure(bg="#f4f4f4")
    root.geometry("600x850")

    # --- Title ---
    tk.Label(root, text="Universal Sigil Generator",
             font=("Arial", 18, "bold"), bg="#f4f4f4").pack(pady=10)

    # --- Phrase input ---
    tk.Label(root, text="Phrase:", bg="#f4f4f4").pack(anchor="w", padx=20)
    phrase_entry = tk.Entry(root, width=50)
    phrase_entry.pack(padx=20, pady=5)

    # --- Mode selection ---
    tk.Label(root, text="Mode:", bg="#f4f4f4").pack(anchor="w", padx=20)
    mode_var = tk.StringVar(value="modern")
    ttk.Combobox(root, textvariable=mode_var,
                 values=["modern", "traditional"]).pack(padx=20, pady=5)

    # --- Intention selection ---
    tk.Label(root, text="Intention:", bg="#f4f4f4").pack(anchor="w", padx=20)
    intention_var = tk.StringVar(value="protection")
    ttk.Combobox(root, textvariable=intention_var,
                 values=list(INTENTION_COLORS.keys())).pack(padx=20, pady=5)

    # --- Method selection ---
    tk.Label(root, text="Method:", bg="#f4f4f4").pack(anchor="w", padx=20)
    method_var = tk.StringVar(value="classical")
    methods_map = {
        "classical": classical,
        "numeric": numeric,
        "planetary": planetary,
        "kamea": kamea,
        "rosicrucian": rosicrucian
    }
    ttk.Combobox(root, textvariable=method_var,
                 values=list(methods_map.keys())).pack(padx=20, pady=5)

    # --- Kamea options ---
    planet_frame = tk.Frame(root, bg="#f4f4f4")
    tk.Label(planet_frame, text="Planet (for Kamea):",
             bg="#f4f4f4").pack(anchor="w", padx=20)
    planet_var = tk.StringVar(value="jupiter")
    planet_combo = ttk.Combobox(planet_frame, textvariable=planet_var,
                                values=list(KAMEA_SQUARES.keys()))
    planet_combo.pack(padx=20, pady=5)

    alphabet_frame = tk.Frame(root, bg="#f4f4f4")
    tk.Label(alphabet_frame, text="Alphabet (for Kamea):",
             bg="#f4f4f4").pack(anchor="w", padx=20)
    alphabet_var = tk.StringVar(value="latin")
    ttk.Combobox(alphabet_frame, textvariable=alphabet_var,
                 values=["latin", "hebrew"]).pack(padx=20, pady=5)

    # --- Influence checkboxes ---
    influence_var = tk.BooleanVar(value=False)
    tk.Checkbutton(root, text="Use current planetary influence (hour & decan)",
                   variable=influence_var, bg="#f4f4f4").pack(anchor="w", padx=20, pady=5)

    strict_var = tk.BooleanVar(value=False)
    tk.Checkbutton(root, text="Strict mode (lock to decan planet)",
                   variable=strict_var, bg="#f4f4f4").pack(anchor="w", padx=40, pady=2)

    # --- Influence updater ---
    def update_influence_info(*args):
        if influence_var.get():
            try:
                influence_info = get_current_planetary_influence()
                hour_symbol = influence_info['planetary_hour']
                hour_name = PLANET_NAMES.get(hour_symbol, "?")
                sign_name = influence_info['sign'].title()
                decan_ruler = influence_info['decan_ruler']
                info_text = (
                    "Astrological Influence\n"
                    "----------------------\n"
                    f"Hour ruler: {hour_symbol} {hour_name} (affects ritual timing, not the sigil itself)\n"
                    f"Sun in {sign_name} → Decan ruler: {decan_ruler} "
                    "(this is used in Kamea if Strict mode is enabled)"
                )
                messagebox.showinfo("Planetary Influence", info_text)

                # Apply strict mode immediately if enabled
                if method_var.get() == "kamea" and strict_var.get():
                    planet_var.set(decan_ruler.lower())
                    planet_combo.configure(state="disabled")
            except Exception as e:
                messagebox.showerror("Error", f"Could not calculate planetary influence:\n{e}")
        else:
            planet_combo.configure(state="normal")

    influence_var.trace("w", update_influence_info)

    # --- Strict mode updater ---
    def update_strict_mode(*args):
        if strict_var.get() and influence_var.get() and method_var.get() == "kamea":
            influence_info = get_current_planetary_influence()
            planet_var.set(influence_info['decan_ruler'].lower())
            planet_combo.configure(state="disabled")
        else:
            planet_combo.configure(state="normal")

    strict_var.trace("w", update_strict_mode)

    # --- Method visibility ---
    def update_planet_visibility(*args):
        if method_var.get() == "kamea":
            planet_frame.pack(fill="x", pady=5)
            alphabet_frame.pack(fill="x", pady=5)
        else:
            planet_frame.forget()
            alphabet_frame.forget()

    method_var.trace("w", update_planet_visibility)

    # --- Output versions ---
    tk.Label(root, text="Output Versions:", bg="#f4f4f4").pack(anchor="w", padx=20)
    version_vars = {v: tk.BooleanVar(value=True) for v in VERSION_DESCRIPTIONS}
    for v, desc in VERSION_DESCRIPTIONS.items():
        tk.Checkbutton(root, text=f"{v} - {desc}", variable=version_vars[v],
                       bg="#f4f4f4").pack(anchor="w", padx=30)

    # --- Guide lines ---
    show_grid_var = tk.BooleanVar(value=False)
    tk.Checkbutton(root, text="Show internal guide lines",
                   variable=show_grid_var, bg="#f4f4f4").pack(anchor="w", padx=20, pady=5)

    # --- Generate sigil ---
    def generate():
        phrase = phrase_entry.get().strip()
        if not phrase:
            messagebox.showerror("Error", "Please enter a phrase.")
            return

        filepath = asksaveasfilename(defaultextension=".png",
                                     filetypes=[("PNG files", "*.png")])
        if not filepath:
            return

        selected_versions = [v for v, var in version_vars.items() if var.get()]
        method = method_var.get()
        method_func = methods_map[method]
        norm_text = normalize_text(phrase, alphabet=alphabet_var.get())

        try:
            if method == "kamea":
                generate_sigil(
                    norm_text, filepath,
                    intention_var.get(), mode_var.get(),
                    selected_versions,
                    lambda **kwargs: method_func(**kwargs, planet=planet_var.get(),
                                                 alphabet=alphabet_var.get()),
                    method="kamea",
                    planet=planet_var.get(),
                    show_grid=show_grid_var.get()
                )
                messagebox.showinfo(
                    "Success",
                    f"Sigil generated with {planet_var.get().title()} Kamea:\n{', '.join(selected_versions)}"
                )
            else:
                generate_sigil(
                    norm_text, filepath,
                    intention_var.get(), mode_var.get(),
                    selected_versions,
                    method_func,
                    method=method,
                    show_grid=show_grid_var.get()
                )
                messagebox.showinfo("Success", f"Sigil generated:\n{', '.join(selected_versions)}")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    tk.Button(root, text="Generate Sigil", command=generate,
              bg="#0077b6", fg="white",
              font=("Arial", 12, "bold"), relief="flat").pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
