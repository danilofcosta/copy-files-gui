from tkinter import filedialog, messagebox
import os, shutil
import tkinter as tk
import threading, queue


class core_Copy:
    def __init__(self):
        self.files_to_parse: list | None = None
        self.folder_to_parse: list | None = None
        self._events: queue.Queue | None = queue.Queue()
        self._copy_thread: threading.Thread | None = None

    def select_dest_active(self):

        self.Bt_start_copy.config(state="active")

    def select_source_files(self):
        files_to_parse = list(
            filedialog.askopenfilenames(
                title="Selecione arquivos", filetypes=(("Todos os arquivos", "*.*"),)
            )
        )
        if len(files_to_parse) == 0:
            return
        self.files_to_parse = files_to_parse
        if hasattr(self, "label_status_file"):
            self.label_status_file.config(
                text=f"Arquivos selecionados: {len(files_to_parse)}"
            )
            self.select_dest_active()
        print("Arquivos selecionados:", files_to_parse)

    def select_source_folders(self):
        folders = []
        while True:
            folder = filedialog.askdirectory(
                title="Selecione uma pasta", mustexist=True
            )
            if not folder:
                break
            folders.append(folder)

            continuar = messagebox.askyesno(
                "Selecionar mais pastas", "Deseja selecionar outra pasta?"
            )
            if not continuar:
                break

        if not folders:
            return
        self.folder_to_parse = folders
        if hasattr(self, "label_status_folder"):
            self.label_status_folder.config(text=f"Pastas selecionadas: {len(folders)}")
            self.select_dest_active()
        print("Pastas selecionadas:", folders)

    def select_dest(self):
        dest = filedialog.askdirectory()
        if not dest:
            return
        self.select_dest_folder = dest
        if hasattr(self, "label_status_dest_folder"):
            self.label_status_dest_folder.config(text=self.select_dest_folder)

    # def s(self, *kwarg):
    #     self.progress_atual["value"] += 1
    #     self.update_idletasks()

    def start_copy_async(self):
        total_items = len(self.folder_to_parse or []) + len(self.files_to_parse or [])
        if hasattr(self, "status_copy_total"):
            self.status_copy_total.config(text=str(total_items))
        if hasattr(self, "progress_atual"):
            # Initialize as continuous percent bar (0-100)
            self.progress_atual["maximum"] = 100
            self.progress_atual["value"] = 0
        if hasattr(self, "Bt_start_copy"):
            self.Bt_start_copy.config(state="disabled")

        # Start worker thread
        self._copy_thread = threading.Thread(target=self._copy_worker, daemon=True)
        self._copy_thread.start()
        # Start polling UI for events
        self._poll_events()

    def _post_event(self, etype: str, data=None):
        if self._events is not None:
            self._events.put((etype, data))

    def _copy_worker(self):
        # Build groups per top-level item (each folder = one group of many files; each file = one group)
        groups = []  # list[list[(src, dst, size)]]
        try:
            # Folders
            if self.folder_to_parse:
                for source_dir_path in self.folder_to_parse:
                        if os.path.isdir(source_dir_path):
                            base_name = os.path.basename(source_dir_path)
                            dest_root = os.path.join(self.select_dest_folder, base_name)
                            group = []
                            for root, _, files in os.walk(source_dir_path):
                                rel_root = os.path.relpath(root, source_dir_path)
                                dest_dir = (
                                    os.path.join(dest_root, rel_root)
                                    if rel_root != "."
                                    else dest_root
                                )
                                os.makedirs(dest_dir, exist_ok=True)
                                for fname in files:
                                    src_path = os.path.join(root, fname)
                                    dst_path = os.path.join(dest_dir, fname)
                                    try:
                                        size = os.path.getsize(src_path)
                                    except Exception:
                                        size = 0
                                    group.append((src_path, dst_path, size))
                            groups.append(group)

                # Individual files
            if self.files_to_parse:
                for file in self.files_to_parse:
                    if os.path.isfile(file):
                            dst_path = os.path.join(
                                self.select_dest_folder, os.path.basename(file)
                            )
                            try:
                                size = os.path.getsize(file)
                            except Exception:
                                size = 0
                            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                            groups.append([(file, dst_path, size)])
        except Exception as e:
            self._post_event("log", f"Error building copy plan: {e}")

        # Update total items label after planning (in case of invalid selections)
        self._post_event("set_total_label", len(groups))
        total_bytes = sum(sz for group in groups for _, _, sz in group) or 1
        bytes_copied = 0

        # Initialize totals and timers
        import time

        start_time = time.time()
        self._post_event("progress", 0)
        self._post_event("total_percent", 0)

        # Iterate per top-level item
        for item_index, group in enumerate(groups, start=1):
            # Show current item index (does not change within the folder)
            self._post_event("index", item_index)

            for src, dst, size in group:
                # per-file progress init
                self._post_event("file_name", os.path.basename(src))
                self._post_event("file_progress", 0)
                try:
                    copied_this_file = 0
                    with open(src, "rb") as rf, open(dst, "wb") as wf:
                        while True:
                            chunk = rf.read(1024 * 1024)
                            if not chunk:
                                break
                            wf.write(chunk)
                            copied_this_file += len(chunk)
                            # per-file percent
                            file_percent = int((copied_this_file / (size or 1)) * 100)
                            self._post_event("file_progress", file_percent)
                            # total percent and ETA
                            bytes_copied += len(chunk)
                            total_percent = int((bytes_copied / total_bytes) * 100)
                            elapsed = time.time() - start_time
                            speed = bytes_copied / elapsed if elapsed > 0 else 0
                            remaining = max(total_bytes - bytes_copied, 0)
                            eta_seconds = int(remaining / speed) if speed > 0 else -1
                            self._post_event("total_percent", total_percent)
                            self._post_event("eta", eta_seconds)
                    # try to preserve metadata
                    try:
                        shutil.copystat(src, dst)
                    except Exception:
                        pass
                    self._post_event("log", f"Copied file: {src}")
                except PermissionError as e:
                    bytes_copied += size
                    self._post_event("file_progress", 100)
                    total_percent = int((bytes_copied / total_bytes) * 100)
                    elapsed = time.time() - start_time
                    speed = bytes_copied / elapsed if elapsed > 0 else 0
                    remaining = max(total_bytes - bytes_copied, 0)
                    eta_seconds = int(remaining / speed) if speed > 0 else -1
                    self._post_event("total_percent", total_percent)
                    self._post_event("eta", eta_seconds)
                    self._post_event(
                        "log", f"Permission denied copying file '{src}': {e}. Skipping."
                    )
                except Exception as e:
                    bytes_copied += size
                    self._post_event("file_progress", 100)
                    total_percent = int((bytes_copied / total_bytes) * 100)
                    elapsed = time.time() - start_time
                    speed = bytes_copied / elapsed if elapsed > 0 else 0
                    remaining = max(total_bytes - bytes_copied, 0)
                    eta_seconds = int(remaining / speed) if speed > 0 else -1
                    self._post_event("total_percent", total_percent)
                    self._post_event("eta", eta_seconds)
                    self._post_event(
                        "log", f"Error copying file '{src}': {e}. Skipping."
                    )

            # After finishing the whole top-level item, update item progress once
            self._post_event("progress", item_index)

        self._post_event("done", None)

    def _poll_events(self):
        # Drain queue and update UI
        drained_any = False
        while self._events is not None and not self._events.empty():
            etype, data = self._events.get()
            drained_any = True
            if etype == "index" and hasattr(self, "status_copy_index"):
                self.status_copy_index.config(text=str(data))
            elif etype == "progress":
                # Item-level progress no longer drives the bar; percentage does
                pass
            # set_max no longer adjusts the bar; we keep it only for compatibility
            elif etype == "set_total_label" and hasattr(self, "status_copy_total"):
                self.status_copy_total.config(text=str(data))
            elif etype == "log":
                print(data)
            elif etype == "file_name" and hasattr(self, "label_file_name"):
                self.label_file_name.config(text=str(data))
            elif etype == "file_progress" and hasattr(self, "progress_file"):
                self.progress_file["maximum"] = 100
                self.progress_file["value"] = max(0, min(100, int(data)))
                if hasattr(self, "label_file_percent"):
                    self.label_file_percent.config(
                        text=f"{max(0, min(100, int(data)))}%"
                    )
            elif etype == "total_percent":
                pct = max(0, min(100, int(data)))
                if hasattr(self, "label_total_percent"):
                    self.label_total_percent.config(text=f"{pct}%")
                if hasattr(self, "progress_atual"):
                    self.progress_atual["maximum"] = 100
                    self.progress_atual["value"] = pct
            elif etype == "eta" and hasattr(self, "label_eta"):
                sec = int(data)
                if sec < 0 or sec > 24 * 3600:
                    self.label_eta.config(text=f"ETA: --:--")
                else:
                    m, s = divmod(sec, 60)
                    h, m = divmod(m, 60)
                    if h > 0:
                        self.label_eta.config(text=f"ETA: {h:02d}:{m:02d}:{s:02d}")
                    else:
                        self.label_eta.config(text=f"ETA: {m:02d}:{s:02d}")
            elif etype == "done":
                if hasattr(self, "Bt_start_copy"):
                    self.Bt_start_copy.config(state="active")
                messagebox.showinfo(
                    "Process Complete", "Files and directories copied successfully."
                )
        # Keep polling if work still ongoing
        if self._copy_thread is not None and self._copy_thread.is_alive():
            self.after(50, self._poll_events)
        else:
            # If no thread, but we just drained residual events, poll one more time
            if drained_any:
                self.after(50, self._poll_events)
