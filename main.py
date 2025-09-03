import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
from config import VERSION_DESCRIPTIONS, INTENTION_COLORS, KAMEA_SQUARES
from core import normalize_text
from methods import classical, numeric, planetary, kamea, rosicrucian
from draw import generate_sigil

def run_gui():
    root = tk.Tk()
    root.title("Universal Sigil Generator")
    root.configure(bg="#f4f4f4")
    root.geometry("520x640")

    tk.Label(root, text="Universal Sigil Generator", font=("Arial", 18, "bold"), bg="#f4f4f4").pack(pady=10)

    # Phrase input
    tk.Label(root, text="Phrase:", bg="#f4f4f4").pack(anchor="w", padx=20)
    phrase_entry = tk.Entry(root, width=50)
    phrase_entry.pack(padx=20, pady=5)

    # Mode
    tk.Label(root, text="Mode:", bg="#f4f4f4").pack(anchor="w", padx=20)
    mode_var = tk.StringVar(value="modern")
    mode_combo = ttk.Combobox(root, textvariable=mode_var, values=["modern", "traditional"])
    mode_combo.pack(padx=20, pady=5)

    # Intention
    tk.Label(root, text="Intention:", bg="#f4f4f4").pack(anchor="w", padx=20)
    intention_var = tk.StringVar(value="protection")
    ttk.Combobox(root, textvariable=intention_var, values=list(INTENTION_COLORS.keys())).pack(padx=20, pady=5)

    # Method
    tk.Label(root, text="Method:", bg="#f4f4f4").pack(anchor="w", padx=20)
    method_var = tk.StringVar(value="classical")
    methods_map = {
        "classical": classical,
        "numeric": numeric,
        "planetary": planetary,
        "kamea": kamea,
        "rosicrucian": rosicrucian
    }
    method_combo = ttk.Combobox(root, textvariable=method_var, values=list(methods_map.keys()))
    method_combo.pack(padx=20, pady=5)

    # Planet selector (only visible for kamea)
    planet_frame = tk.Frame(root, bg="#f4f4f4")
    tk.Label(planet_frame, text="Planet (for Kamea):", bg="#f4f4f4").pack(anchor="w", padx=20)
    planet_var = tk.StringVar(value="jupiter")
    planet_combo = ttk.Combobox(planet_frame, textvariable=planet_var, values=list(KAMEA_SQUARES.keys()))
    planet_combo.pack(padx=20, pady=5)

    def update_planet_visibility(*args):
        if method_var.get() == "kamea":
            planet_frame.pack(fill="x", pady=5)
        else:
            planet_frame.forget()

    method_var.trace("w", update_planet_visibility)

    # Versions
    tk.Label(root, text="Output Versions:", bg="#f4f4f4").pack(anchor="w", padx=20)
    version_vars = {v: tk.BooleanVar(value=True) for v in VERSION_DESCRIPTIONS}
    for v, desc in VERSION_DESCRIPTIONS.items():
        tk.Checkbutton(root, text=f"{v} - {desc}", variable=version_vars[v], bg="#f4f4f4").pack(anchor="w", padx=30)

    # Show internal guide lines
    show_grid_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        root,
        text="Show internal guide lines",
        variable=show_grid_var,
        bg="#f4f4f4"
    ).pack(anchor="w", padx=20, pady=5)

    # Generate function
    def generate():
        phrase = phrase_entry.get().strip()
        if not phrase:
            messagebox.showerror("Error", "Please enter a phrase.")
            return

        filepath = asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if not filepath:
            return

        selected_versions = [v for v, var in version_vars.items() if var.get()]
        method = method_var.get()
        method_func = methods_map[method]
        norm_text = normalize_text(phrase)

        try:
            if method == "kamea":
                generate_sigil(
                    norm_text,
                    filepath,
                    intention_var.get(),
                    mode_var.get(),
                    selected_versions,
                    lambda **kwargs: method_func(**kwargs, planet=planet_var.get()),
                    method="kamea",
                    planet=planet_var.get(),
                    show_grid=show_grid_var.get()
                )
            else:
                generate_sigil(
                    norm_text,
                    filepath,
                    intention_var.get(),
                    mode_var.get(),
                    selected_versions,
                    method_func,
                    method=method,
                    show_grid=show_grid_var.get()
                )

            messagebox.showinfo("Success", f"Sigil generated:\n{', '.join(selected_versions)}")

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    # Dynamic button color
    def update_button_color(*args):
        if mode_var.get() == "traditional":
            generate_button.config(bg="#222222", fg="white")
        else:
            generate_button.config(bg="#0077b6", fg="white")

    mode_var.trace("w", update_button_color)

    # Generate button
    generate_button = tk.Button(
        root,
        text="Generate Sigil",
        command=generate,
        bg="#0077b6",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat"
    )
    generate_button.pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    run_gui()