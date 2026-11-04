import os
import sys
import json
import uuid
import re
import shutil
import string
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Try DPI awareness on Windows
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

APP_TITLE = "HeadRush NAM Block Manager"
APP_VERSION = "2.0 (Win11 Edition)"

class HeadRushBlockManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_TITLE} v{APP_VERSION}")
        self.geometry("860x720")
        self.minsize(780, 600)

        # Apply dark theme styling
        self.bg_color = "#18181b"
        self.card_bg = "#27272a"
        self.card_border = "#3f3f46"
        self.fg_color = "#f4f4f5"
        self.fg_muted = "#a1a1aa"
        self.accent_color = "#0284c7"
        self.accent_hover = "#0369a1"
        self.success_color = "#10b981"
        self.warning_color = "#f59e0b"

        self.configure(bg=self.bg_color)
        self.setup_styles()

        self.detected_models = []
        self.current_drive = tk.StringVar(value="")
        self.custom_nam_path = tk.StringVar(value="")
        self.custom_blocks_path = tk.StringVar(value="")

        self.opt_anxiety1 = tk.BooleanVar(value=True)
        self.opt_anxiety2 = tk.BooleanVar(value=True)
        self.opt_amp = tk.BooleanVar(value=True)
        self.opt_clean_old = tk.BooleanVar(value=True)
        self.opt_backup = tk.BooleanVar(value=True)
        self.opt_prefix_idx = tk.BooleanVar(value=True)
        self.val_level = tk.IntVar(value=50)
        self.val_tone = tk.IntVar(value=50)

        self.build_ui()
        self.detect_headrush_drives()

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Configure generic styles
        self.style.configure(".", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_bg, relief="flat")
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        self.style.configure("Card.TLabel", background=self.card_bg, foreground=self.fg_color, font=("Segoe UI", 10))
        self.style.configure("Muted.TLabel", background=self.card_bg, foreground=self.fg_muted, font=("Segoe UI", 9))
        self.style.configure("Title.TLabel", background=self.bg_color, foreground="#38bdf8", font=("Segoe UI", 16, "bold"))
        self.style.configure("CardHeader.TLabel", background=self.card_bg, foreground="#38bdf8", font=("Segoe UI", 11, "bold"))

        # Combobox
        self.style.configure("TCombobox", fieldbackground="#3f3f46", background="#3f3f46", foreground="#ffffff")
        self.style.map("TCombobox", fieldbackground=[("readonly", "#3f3f46")], foreground=[("readonly", "#ffffff")])

        # Checkbutton
        self.style.configure("TCheckbutton", background=self.card_bg, foreground=self.fg_color, font=("Segoe UI", 10))
        self.style.map("TCheckbutton", background=[("active", self.card_bg)])

        # Treeview (Models List)
        self.style.configure("Treeview",
                             background="#1e1e24",
                             foreground="#f4f4f5",
                             fieldbackground="#1e1e24",
                             rowheight=26,
                             font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading",
                             background="#33333d",
                             foreground="#38bdf8",
                             relief="flat",
                             font=("Segoe UI", 9, "bold"))
        self.style.map("Treeview", background=[("selected", self.accent_color)], foreground=[("selected", "#ffffff")])

        # Progressbar
        self.style.configure("Horizontal.TProgressbar", background="#0ea5e9", troughcolor="#27272a")

    def build_ui(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        title_lbl = ttk.Label(header_frame, text="⚡ HeadRush NAM Block Manager", style="Title.TLabel")
        title_lbl.pack(anchor="w")
        subtitle_lbl = ttk.Label(header_frame, text="Sincronizador inteligente de perfiles NAM a Presets de Bloque táctiles con nombre real", foreground=self.fg_muted)
        subtitle_lbl.pack(anchor="w")

        # Card 1: Drive Detection
        drive_card = ttk.Frame(self, style="Card.TFrame", padding=12)
        drive_card.pack(fill="x", padx=20, pady=6)

        c1_head = ttk.Frame(drive_card, style="Card.TFrame")
        c1_head.pack(fill="x", pady=(0, 6))
        ttk.Label(c1_head, text="1. Unidad HeadRush / Rutas de Almacenamiento", style="CardHeader.TLabel").pack(side="left")

        drive_row = ttk.Frame(drive_card, style="Card.TFrame")
        drive_row.pack(fill="x", pady=4)

        ttk.Label(drive_row, text="Unidad detectada:", style="Card.TLabel").pack(side="left", padx=(0, 8))
        self.drive_combo = ttk.Combobox(drive_row, textvariable=self.current_drive, state="readonly", width=35)
        self.drive_combo.pack(side="left", padx=(0, 8))
        self.drive_combo.bind("<<ComboboxSelected>>", lambda e: self.on_drive_selected())

        btn_rescan = tk.Button(drive_row, text="🔄 Re-escanear Unidades", bg="#3f3f46", fg="#ffffff",
                               activebackground="#52525b", activeforeground="#ffffff", relief="flat",
                               font=("Segoe UI", 9), command=self.detect_headrush_drives, padx=8, pady=2)
        btn_rescan.pack(side="left", padx=4)

        btn_browse = tk.Button(drive_row, text="📁 Elegir Carpeta Manual...", bg="#3f3f46", fg="#ffffff",
                               activebackground="#52525b", activeforeground="#ffffff", relief="flat",
                               font=("Segoe UI", 9), command=self.browse_custom_folder, padx=8, pady=2)
        btn_browse.pack(side="left", padx=4)

        # Paths status row
        self.path_info_lbl = ttk.Label(drive_card, text="Buscando unidad HeadRush...", style="Muted.TLabel")
        self.path_info_lbl.pack(anchor="w", pady=(4, 0))

        # Card 2: Detected Models Table
        models_card = ttk.Frame(self, style="Card.TFrame", padding=12)
        models_card.pack(fill="both", expand=True, padx=20, pady=6)

        c2_head = ttk.Frame(models_card, style="Card.TFrame")
        c2_head.pack(fill="x", pady=(0, 6))
        ttk.Label(c2_head, text="2. Modelos NAM Detectados", style="CardHeader.TLabel").pack(side="left")
        self.models_count_lbl = ttk.Label(c2_head, text="0 modelos", style="Muted.TLabel")
        self.models_count_lbl.pack(side="right")

        tree_frame = ttk.Frame(models_card, style="Card.TFrame")
        tree_frame.pack(fill="both", expand=True)

        columns = ("idx", "knob", "name", "filesize")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        self.tree.heading("idx", text="#")
        self.tree.heading("knob", text="Paso Drive")
        self.tree.heading("name", text="Nombre del Modelo / Preset")
        self.tree.heading("filesize", text="Tamaño")

        self.tree.column("idx", width=45, anchor="center")
        self.tree.column("knob", width=80, anchor="center")
        self.tree.column("name", width=450, anchor="w")
        self.tree.column("filesize", width=90, anchor="e")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Card 3: Options & Actions
        opts_card = ttk.Frame(self, style="Card.TFrame", padding=12)
        opts_card.pack(fill="x", padx=20, pady=6)

        c3_head = ttk.Frame(opts_card, style="Card.TFrame")
        c3_head.pack(fill="x", pady=(0, 6))
        ttk.Label(c3_head, text="3. Opciones de Sincronización", style="CardHeader.TLabel").pack(side="left")

        opts_row = ttk.Frame(opts_card, style="Card.TFrame")
        opts_row.pack(fill="x", pady=2)

        ttk.Checkbutton(opts_row, text="Generar para ANXIETY OD", variable=self.opt_anxiety1).pack(side="left", padx=(0, 15))
        ttk.Checkbutton(opts_row, text="Generar para ANXIETY OD V2", variable=self.opt_anxiety2).pack(side="left", padx=(0, 15))
        ttk.Checkbutton(opts_row, text="Generar para 82 LEAD 800 (NAM)", variable=self.opt_amp).pack(side="left", padx=(0, 15))
        ttk.Checkbutton(opts_row, text="Limpiar bloques obsoletos en HeadRush", variable=self.opt_clean_old).pack(side="left", padx=(0, 15))
        ttk.Checkbutton(opts_row, text="Hacer copia de seguridad previa", variable=self.opt_backup).pack(side="left")

        # Big Action Button
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=20, pady=(6, 15))

        self.progress = ttk.Progressbar(action_frame, orient="horizontal", mode="determinate", style="Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(0, 8))

        btn_row = ttk.Frame(action_frame)
        btn_row.pack(fill="x")

        self.status_lbl = ttk.Label(btn_row, text="Listo para sincronizar.", foreground=self.fg_muted)
        self.status_lbl.pack(side="left", anchor="w")

        self.sync_btn = tk.Button(btn_row, text="⚡ SINCRONIZAR BLOQUES EN HEADRUSH", bg="#0284c7", fg="#ffffff",
                                  activebackground="#0369a1", activeforeground="#ffffff", relief="flat",
                                  font=("Segoe UI", 11, "bold"), command=self.run_synchronization,
                                  padx=20, pady=8, cursor="hand2")
        self.sync_btn.pack(side="right")

    def get_available_drives(self):
        drives = []
        bitmask = 0
        try:
            bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        except Exception:
            pass

        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drive_str = f"{letter}:\\"
                drives.append(drive_str)
            bitmask >>= 1
        return drives

    def detect_headrush_drives(self):
        drives = self.get_available_drives()
        options = []
        default_choice = ""

        # Specifically prioritize D:\ and drives with NAM / Blocks folder
        for d in drives:
            try:
                has_nam = (Path(d) / "NAM").is_dir()
                has_blocks = (Path(d) / "Blocks").is_dir()
                label = d
                if has_nam and has_blocks:
                    label = f"{d} (HeadRush Gigboard detectada ★)"
                    if not default_choice or d.upper().startswith("D:"):
                        default_choice = label
                elif d.upper().startswith("D:"):
                    label = f"{d} (Unidad D:)"
                    if not default_choice:
                        default_choice = label
                options.append((label, d))
            except Exception:
                continue

        if not options:
            options = [("D:\\ (Unidad D por defecto)", "D:\\")]
            default_choice = options[0][0]

        self.drive_options = options
        self.drive_combo["values"] = [opt[0] for opt in options]

        if default_choice:
            self.drive_combo.set(default_choice)
        elif options:
            self.drive_combo.set(options[0][0])

        self.on_drive_selected()

    def get_selected_drive_root(self):
        sel = self.drive_combo.get()
        for label, root in self.drive_options:
            if label == sel:
                return root
        # Fallback
        if len(sel) >= 2 and sel[1] == ":":
            return sel[:3]
        return "D:\\"

    def browse_custom_folder(self):
        folder = filedialog.askdirectory(title="Selecciona la carpeta raíz de tu HeadRush o carpeta con archivos NAM")
        if folder:
            path = Path(folder)
            # Check if this is a NAM folder itself or the root containing NAM
            if path.name.upper() == "NAM":
                root = str(path.parent)
            else:
                root = str(path)

            custom_label = f"{root} (Carpeta seleccionada)"
            self.drive_options.insert(0, (custom_label, root))
            self.drive_combo["values"] = [opt[0] for opt in self.drive_options]
            self.drive_combo.set(custom_label)
            self.on_drive_selected()

    def on_drive_selected(self):
        root = Path(self.get_selected_drive_root())
        nam_dir = root / "NAM"
        blocks_dir = root / "Blocks"

        status_text = []
        if nam_dir.is_dir():
            status_text.append(f"✓ Carpeta NAM: {nam_dir}")
        else:
            status_text.append(f"⚠ Carpeta NAM no encontrada en {nam_dir} (puedes crearla o elegir otra carpeta)")

        if blocks_dir.is_dir():
            status_text.append(f"✓ Carpeta Blocks: {blocks_dir}")
        else:
            status_text.append(f"• Carpeta Blocks se creará automáticamente en {blocks_dir}")

        self.path_info_lbl.config(text="  |  ".join(status_text))
        self.scan_models(nam_dir)

    def scan_models(self, nam_dir: Path):
        self.detected_models.clear()
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not nam_dir.is_dir():
            self.models_count_lbl.config(text="0 modelos (carpeta no encontrada)", foreground=self.warning_color)
            return

        files = []
        try:
            for item in nam_dir.iterdir():
                if not item.is_file():
                    continue
                name = item.name
                # Skip AppleDouble sidecars
                if name.startswith("._") or name.startswith("."):
                    continue
                ext = item.suffix.lower()
                if ext in [".nam", ".nam2"]:
                    files.append(item)
        except Exception as e:
            self.models_count_lbl.config(text=f"Error al leer: {e}", foreground=self.warning_color)
            return

        # Sort strictly alphabetically, identically to C++ nam_hook.cpp
        files.sort(key=lambda p: p.name)
        self.detected_models = files

        count = len(files)
        if count == 0:
            self.models_count_lbl.config(text="0 modelos encontrados en D:\\NAM", foreground=self.warning_color)
            self.status_lbl.config(text="Copia tus archivos .nam en la carpeta NAM de la Gigboard.")
        elif count <= 101:
            self.models_count_lbl.config(text=f"{count} modelos encontrados (todos caben en Drive 0%..{count-1}%)", foreground=self.success_color)
            self.status_lbl.config(text=f"{count} modelos listos para sincronizar.")
        else:
            self.models_count_lbl.config(text=f"{count} modelos (Atención: los primeros 101 cubrirán 0%..100%)", foreground=self.warning_color)
            self.status_lbl.config(text=f"Atención: {count} archivos. Los primeros 101 se asignarán a Drive 0%..100%.")

        for idx, fpath in enumerate(files):
            stem = fpath.stem
            # Clean possible duplicate index if present
            clean_name = re.sub(r'^\d+\s*[-_.]\s*', '', stem)
            if self.opt_prefix_idx.get():
                display_name = f"{idx:03d} - {clean_name}"
            else:
                display_name = clean_name

            knob_str = f"{idx}%" if idx <= 100 else "Fuera de rango (>100%)"
            size_kb = f"{fpath.stat().st_size / 1024:.1f} KB"

            tag = "warn" if idx > 100 else "ok"
            self.tree.insert("", "end", values=(f"{idx:03d}", knob_str, display_name, size_kb), tags=(tag,))

        self.tree.tag_configure("warn", foreground="#f87171")
        self.tree.tag_configure("ok", foreground="#f4f4f5")

    def run_synchronization(self):
        if not self.detected_models:
            messagebox.showwarning("Sin Modelos", "No hay archivos .nam en la carpeta seleccionada.\n\nAsegúrate de conectar la Gigboard en modo USB Transfer y que existan archivos .nam en la carpeta NAM.")
            return

        root = Path(self.get_selected_drive_root())
        blocks_dir = root / "Blocks"

        targets = []
        if self.opt_anxiety1.get():
            targets.append(("ANXIETY OD", "Anxiety OD", "pedal"))
        if self.opt_anxiety2.get():
            targets.append(("ANXIETY OD V2", "Anxiety OD V2", "pedal"))
        if self.opt_amp.get():
            targets.append(("AMP", "82 LEAD 800 Bright", "amp"))

        if not targets:
            messagebox.showwarning("Sin Destino", "Debes seleccionar al menos un tipo de bloque (Anxiety OD, Anxiety OD V2 o 82 LEAD 800).")
            return

        confirm_msg = f"Se van a sincronizar {len(self.detected_models)} modelos en:\n"
        for t_folder, _, _ in targets:
            confirm_msg += f"  - {blocks_dir / t_folder}\n"

        if self.opt_clean_old.get():
            confirm_msg += "\nSe eliminarán presets obsoletos para evitar desajustes con los archivos eliminados."
        if self.opt_backup.get():
            confirm_msg += "\nSe creará una copia de seguridad automática antes de limpiar."

        confirm_msg += "\n\n¿Deseas continuar?"

        if not messagebox.askyesno("Confirmar Sincronización", confirm_msg):
            return

        self.sync_btn.config(state="disabled")
        self.progress["value"] = 0
        total_steps = len(targets) * min(len(self.detected_models), 101)
        step = 0

        created_count = 0
        backup_created = False

        try:
            for t_folder, target_key, kind in targets:
                dest = blocks_dir / t_folder
                dest.mkdir(parents=True, exist_ok=True)

                # Backup if requested
                if self.opt_backup.get() and dest.exists():
                    existing_blocks = list(dest.glob("*.block"))
                    if existing_blocks:
                        backup_dir = blocks_dir / f"_backup_{t_folder}"
                        backup_dir.mkdir(parents=True, exist_ok=True)
                        for b in existing_blocks:
                            try:
                                shutil.copy2(b, backup_dir / b.name)
                            except Exception:
                                pass
                        backup_created = True

                # Clean old presets if requested
                if self.opt_clean_old.get() and dest.exists():
                    for old_b in dest.glob("*.block"):
                        try:
                            old_b.unlink()
                        except Exception:
                            pass

                # Generate new blocks
                for idx, fpath in enumerate(self.detected_models):
                    if idx > 100:
                        break  # Maximum 101 models (0%..100%)

                    stem = fpath.stem
                    clean_name = re.sub(r'^\d+\s*[-_.]\s*', '', stem)
                    block_filename = f"{idx:03d} - {clean_name}.block"
                    block_path = dest / block_filename

                    if kind == "amp":
                        inner_dict = {
                            "data": {
                                "Amp": {
                                    "childorder": [
                                        "TremSync", "DoubleStates", "Type", "Bright", "Treble",
                                        "Mid", "MidFreq", "Bass", "Presence", "GainA", "GainB",
                                        "TremSpeed", "TremDepth", "Master", "Tremolo"
                                    ],
                                    "children": {
                                        "Bass": {"type": 0, "value": 50},
                                        "Bright": {"state": False, "type": 1},
                                        "DoubleStates": {"state": False, "type": 3},
                                        "GainA": {"type": 0, "value": 50},
                                        "GainB": {"type": 0, "value": 50},
                                        "Master": {"type": 0, "value": 50},
                                        "Mid": {"type": 0, "value": 50},
                                        "MidFreq": {"type": 0, "value": 1610},
                                        "Presence": {"type": 0, "value": 50},
                                        "Treble": {"type": 0, "value": 50},
                                        "TremDepth": {"type": 0, "value": idx},
                                        "TremSpeed": {"type": 0, "value": 6},
                                        "TremSync": {"state": False, "type": 1},
                                        "Tremolo": {"state": False, "type": 1},
                                        "Type": {"string": "82 LEAD 800 Bright", "type": 4}
                                    }
                                }
                            },
                            "info": {"version": "1.0.9"}
                        }
                    else:
                        inner_dict = {
                            "data": {
                                target_key: {
                                    "childorder": ["Level", "Drive", "Tone", "Hi-Lo"],
                                    "children": {
                                        "Drive": {"type": 0, "value": idx},
                                        "Hi-Lo": {"state": False, "type": 1},
                                        "Level": {"type": 0, "value": self.val_level.get()},
                                        "Tone": {"type": 0, "value": self.val_tone.get()}
                                    }
                                }
                            },
                            "info": {"version": "1.0.9"}
                        }

                    outer_dict = {
                        "content": json.dumps(inner_dict, separators=(',', ':')),
                        "id": str(uuid.uuid4()),
                        "readonly": False,
                        "type": t_folder
                    }

                    with open(block_path, "w", encoding="utf-8") as out_f:
                        json.dump(outer_dict, out_f, indent=2)

                    created_count += 1
                    step += 1
                    self.progress["value"] = (step / total_steps) * 100
                    self.status_lbl.config(text=f"Generando: {block_filename}...")
                    self.update_idletasks()

            self.status_lbl.config(text="¡Sincronización completada con éxito!", foreground=self.success_color)
            self.progress["value"] = 100

            success_text = f"¡Operación finalizada con éxito!\n\n"
            success_text += f"• Se generaron {created_count} archivos de bloque en HeadRush.\n"
            if backup_created:
                success_text += f"• Se creó copia de seguridad en {blocks_dir / '_backup_*'}\n"
            success_text += "\nYa puedes expulsar con seguridad el USB desde Windows y usar tus amplificadores por su nombre real en la Gigboard."

            messagebox.showinfo("Completado", success_text)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la sincronización:\n{e}")
            self.status_lbl.config(text=f"Error: {e}", foreground=self.warning_color)
        finally:
            self.sync_btn.config(state="normal")

if __name__ == "__main__":
    app = HeadRushBlockManager()
    app.mainloop()

