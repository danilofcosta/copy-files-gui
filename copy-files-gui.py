import os, json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from core.core import core_Copy


class Copy_py(tk.Tk, core_Copy):
    def __init__(self, title: str = "Copy_py", geometry: tuple = (400, 500)):
        tk.Tk.__init__(self)
        core_Copy.__init__(self)

        # pre definiçãoes
        self.title(title)
        self.geometry("{}x{}".format(*geometry))
        self.configs: None | dict = None
        self.lang = "en"
        self.select_dest_folder = os.path.expanduser("~Downloads")
        self.load_lang()
        self.init_UI()

    def load_lang(self, LC_MESSAGES="CONFIGS.json"):
        LANG = os.getenv("LANG")
        with open(LC_MESSAGES, "r", encoding="utf-8") as lang:
            l = json.load(lang)
        self.configs = l

    def get_message(self, key: str):
        return self.configs.get("messages").get(self.lang).get(key)

    def init_UI(self):
        # Language button at top
        lang_frame = tk.Frame(self)
        lang_frame.pack(pady=5, fill="x")

        self.lang_button = tk.Button(
            lang_frame,
            text=self.get_message("switch_lang"),
            command=self.switch_language,
        )
        self.lang_button.pack(side="right", padx=5)

        tk.Label(self, text=self.get_message("info_bt")).pack(pady=10)
        # Slight UI styling
        try:
            self.style = ttk.Style()
            self.style.theme_use(self.style.theme_use())
        except Exception:
            pass
        # select files
        select_source_lin = tk.Frame(self)
        select_source_lin.pack(pady=10, fill="x")

        self.label_status_file = tk.Label(
            select_source_lin, text=self.get_message("select_source_not_select")
        )
        self.label_status_file.pack(side="left", padx=5)
        tk.Button(
            select_source_lin,
            text=self.get_message("select_source"),
            command=self.select_source_files,
        ).pack(side="left", padx=5)
        tk.Button(
            select_source_lin,
            text=self.get_message("clear_files"),
            command=self.clear_selected_files,
        ).pack(side="left", padx=5)

        # select folders
        select_source_lin_folder = tk.Frame(self)
        select_source_lin_folder.pack(pady=10, fill="x")
        self.label_status_folder = tk.Label(
            select_source_lin_folder,
            text=self.get_message("select_source_folder_not_select"),
        )
        self.label_status_folder.pack(side="left", padx=5)

        tk.Button(
            select_source_lin_folder,
            text=self.get_message("select_source_folder"),
            command=self.select_source_folders,
        ).pack(side="left", padx=5)
        tk.Button(
            select_source_lin_folder,
            text=self.get_message("clear_folders"),
            command=self.clear_selected_folders,
        ).pack(side="left", padx=5)

        # select dir deford
        dest_folder_lin = tk.Frame(self)
        dest_folder_lin.pack(pady=10, fill="x")

        self.label_status_dest_folder = tk.Label(
            dest_folder_lin, text=self.select_dest_folder
        )
        self.label_status_dest_folder.pack(side="left", padx=5)

        tk.Button(
            dest_folder_lin,
            text=self.get_message("select_dest"),
            command=self.select_dest,
        ).pack(side="left", padx=5)

        # bt start copy
        Bt_start_copy = tk.Frame(self)
        Bt_start_copy.pack(pady=10)

        self.Bt_start_copy = tk.Button(
            Bt_start_copy,
            text=self.get_message("start_copy"),
            command=self.start_copy_async,
            state="disabled",
        )
        self.Bt_start_copy.pack(side="left", padx=5)

        status_copy = tk.Frame(self)
        status_copy.pack(pady=10, fill="x")

        self.status_copy_index = tk.Label(status_copy, text="0")
        self.status_copy_index.pack(side="left", padx=5)

        tk.Label(status_copy, text="-").pack(side="left", padx=5)

        self.status_copy_total = tk.Label(status_copy, text="0")
        self.status_copy_total.pack(side="left", padx=5)

        # --- Progresso por arquivo ---
        file_progress_frame = tk.Frame(self)
        file_progress_frame.pack(pady=10, fill="x")

        self.label_file_name = tk.Label(file_progress_frame, text="-")
        self.label_file_name.pack(side="left", padx=5)

        self.label_file_percent = tk.Label(file_progress_frame, text="0%")
        self.label_file_percent.pack(side="right", padx=1)

        self.progress_file = ttk.Progressbar(
            self, orient="horizontal", length=400, mode="determinate"
        )
        self.progress_file.pack(pady=5)

        # --- Progresso total ---
        total_progress_frame = tk.Frame(self)
        total_progress_frame.pack(pady=10, fill="x")

        self.progress_atual = ttk.Progressbar(
            total_progress_frame, orient="horizontal", length=400, mode="determinate"
        )
        self.progress_atual.pack(pady=1)

        status_end = tk.Frame(self)
        status_end.pack(pady=1, fill="x")

        # Alinha os textos à direita
        self.label_total_percent = tk.Label(status_end, text="0%")
        self.label_total_percent.pack(side="right", padx=1)

        self.label_eta = tk.Label(status_end, text=f"ETA: --:--")
        self.label_eta.pack(side="right", padx=5)



    def clear_selected_files(self):
        self.files_to_parse = None
        if hasattr(self, "label_status_file"):
            self.label_status_file.config(
                text=self.get_message("select_source_not_select")
            )
        if hasattr(self, "Bt_start_copy"):
            self.Bt_start_copy.config(state="disabled")

    def clear_selected_folders(self):
        self.folder_to_parse = None
        if hasattr(self, "label_status_folder"):
            self.label_status_folder.config(
                text=self.get_message("select_source_folder_not_select")
            )
        if hasattr(self, "Bt_start_copy"):
            self.Bt_start_copy.config(state="disabled")

    def switch_language(self):
        # Toggle between en and pt
        self.lang = "pt" if self.lang == "en" else "en"
        self.refresh_ui_texts()

    def refresh_ui_texts(self):
        # Update all UI texts with new language
        if hasattr(self, "lang_button"):
            self.lang_button.config(text=self.get_message("switch_lang"))

        # Update main info label
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") in [
                "Click the button to copy files and directories",
                "Clique no botão para copiar arquivos e diretórios",
            ]:
                widget.config(text=self.get_message("info_bt"))
                break

        # Update file selection labels
        if hasattr(self, "label_status_file"):
            if self.files_to_parse:
                self.label_status_file.config(
                    text=(
                        f"Arquivos selecionados: {len(self.files_to_parse)}"
                        if self.lang == "pt"
                        else f"Files selected: {len(self.files_to_parse)}"
                    )
                )
            else:
                self.label_status_file.config(
                    text=self.get_message("select_source_not_select")
                )

        # Update folder selection labels
        if hasattr(self, "label_status_folder"):
            if self.folder_to_parse:
                self.label_status_folder.config(
                    text=(
                        f"Pastas selecionadas: {len(self.folder_to_parse)}"
                        if self.lang == "pt"
                        else f"Folders selected: {len(self.folder_to_parse)}"
                    )
                )
            else:
                self.label_status_folder.config(
                    text=self.get_message("select_source_folder_not_select")
                )

        # Update buttons
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                text = widget.cget("text")
                if text in ["Select files", "Selecionar arquivos"]:
                    widget.config(text=self.get_message("select_source"))
                elif text in ["Clear files", "Limpar arquivos"]:
                    widget.config(text=self.get_message("clear_files"))
                elif text in ["Select folders", "Selecionar pastas"]:
                    widget.config(text=self.get_message("select_source_folder"))
                elif text in ["Clear folders", "Limpar pastas"]:
                    widget.config(text=self.get_message("clear_folders"))
                elif text in ["Select destination", "Selecionar destino"]:
                    widget.config(text=self.get_message("select_dest"))
                elif text in ["Start copy", "Iniciar cópia"]:
                    widget.config(text=self.get_message("start_copy"))


Copy = Copy_py()
Copy.mainloop()
