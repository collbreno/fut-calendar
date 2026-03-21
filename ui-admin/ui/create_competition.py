import tkinter as tk
from tkinter import ttk, messagebox
import threading
from services.api import call_api


class CreateCompetition(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=15)
        self.app = app

        self.build_ui()

    def build_ui(self):
        frame = self

        # --- Back button ---
        ttk.Button(
            frame,
            text="← Back",
            command=lambda: self.app.show_frame_by_name("MainMenu")
        ).grid(row=0, column=0, sticky="w")

        # --- Slug ---
        ttk.Label(frame, text="Slug:").grid(row=1, column=0, sticky="w")
        self.slug_input = ttk.Entry(frame)
        self.slug_input.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)

        # --- Checkboxes (2 columns) ---
        options_frame = ttk.LabelFrame(frame, text="Options")
        options_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.create_calendar = tk.BooleanVar()
        self.create_teams = tk.BooleanVar()
        self.create_maps = tk.BooleanVar()
        self.use_mapper = tk.BooleanVar()

        ttk.Checkbutton(options_frame, text="Create Calendar", variable=self.create_calendar).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(options_frame, text="Create Teams", variable=self.create_teams).grid(row=0, column=1, sticky="w")
        ttk.Checkbutton(options_frame, text="Create Maps", variable=self.create_maps).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(options_frame, text="Use Mapper", variable=self.use_mapper).grid(row=1, column=1, sticky="w")

        # --- Flag ---
        ttk.Label(frame, text="Flag (optional):").grid(row=4, column=0, sticky="w")
        self.flag_input = ttk.Entry(frame)
        self.flag_input.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)

        # --- Submit ---
        self.submit_btn = ttk.Button(frame, text="Submit", command=self.on_submit)
        self.submit_btn.grid(row=6, column=0, sticky="ew", pady=10)

        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.grid(row=6, column=1, sticky="ew")
        self.progress.grid_remove()

        self.result_text = tk.Text(frame, height=8)
        self.result_text.grid(row=7, column=0, columnspan=2, sticky="ew")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def on_submit(self):
        slug = self.slug_input.get().strip()
        if not slug:
            messagebox.showerror("Error", "Slug is required")
            return

        options = {
            "create_calendar": self.create_calendar.get(),
            "create_teams": self.create_teams.get(),
            "create_maps": self.create_maps.get(),
            "use_mapper": self.use_mapper.get(),
        }

        self.submit_btn.config(state="disabled")
        self.progress.grid()
        self.progress.start()

        threading.Thread(
            target=self.run_api,
            args=(slug, self.flag_input.get(), options),
            daemon=True
        ).start()

    def run_api(self, slug, flag, options):
        try:
            result = call_api(slug, flag, options)
            self.after(0, self.show_result, result)
        except Exception as e:
            self.after(0, self.show_error, str(e))

    def show_result(self, result):
        self.progress.stop()
        self.progress.grid_remove()
        self.submit_btn.config(state="normal")

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result["text"])

    def show_error(self, msg):
        self.progress.stop()
        self.progress.grid_remove()
        self.submit_btn.config(state="normal")
        messagebox.showerror("Error", msg)