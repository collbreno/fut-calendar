import tkinter as tk
from tkinter import ttk, messagebox
import threading
from services.api import get_competitions, toggle_competition


class ManageCompetitions(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=15)
        self.app = app

        self.build_ui()

    def build_ui(self):
        # --- Top bar ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x")

        ttk.Button(
            top_frame,
            text="← Back",
            command=lambda: self.app.show_frame_by_name("MainMenu")
        ).pack(side="left")

        ttk.Button(
            top_frame,
            text="Refresh",
            command=self.load_data
        ).pack(side="right")

        # --- Progress ---
        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", pady=5)
        self.progress.pack_forget()

        # --- Treeview ---
        columns = (
            "slug",
            "name",
            "flag",
            "calendar_id",
            "teams",
            "use_mapper",
            "last_update",
            "disabled",
            "action"
        )

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("slug", text="Slug")
        self.tree.heading("name", text="Name")
        self.tree.heading("flag", text="Flag")
        self.tree.heading("calendar_id", text="Calendar ID")
        self.tree.heading("teams", text="Teams")
        self.tree.heading("use_mapper", text="Mapper")
        self.tree.heading("last_update", text="Last Update")
        self.tree.heading("disabled", text="Enabled")
        self.tree.heading("action", text="Action")

        # Optional: column widths
        self.tree.column("slug", width=120)
        self.tree.column("name", width=150)
        self.tree.column("teams", width=200)
        self.tree.column("action", width=100, anchor="center")
        self.tree.column("disabled", anchor="center", width=80)

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Button-1>", self.on_tree_click)

        # Load data initially
        self.load_data()

    def load_data(self):
        self.progress.pack(fill="x", pady=5)
        self.progress.start()

        threading.Thread(target=self._load_data_thread, daemon=True).start()

    def _load_data_thread(self):
        try:
            data = get_competitions()
            self.after(0, self.populate_table, data)
        except Exception as e:
            self.after(0, self.show_error, str(e))

    def populate_table(self, competitions):
        self.progress.stop()
        self.progress.pack_forget()

        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        for comp in competitions:
            teams = ", ".join(comp["teams"]) if comp["teams"] else ""

            is_enabled = not comp["disabled"]

            enabled_text = "✅" if is_enabled else ""
            action_text = "Disable" if is_enabled else "Enable"

            self.tree.insert(
                "",
                "end",
                values=(
                    comp["slug"],
                    comp["name"],
                    comp["flag"] or "",
                    comp["calendar_id"] or "",
                    teams,
                    "Yes" if comp["use_mapper"] else "No",
                    comp["last_update"].strftime("%Y-%m-%d %H:%M"),
                    enabled_text,
                    action_text,
                ),
            )

    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        col = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)

        if not row:
            return

        # Check if it's the last column (Action)
        if col != f"#{len(self.tree['columns'])}":
            return

        values = self.tree.item(row, "values")
        slug = values[0]
        is_disabled = values[6] == "Yes"

        threading.Thread(
            target=self._toggle_thread,
            args=(slug, is_disabled),
            daemon=True
        ).start()


    def _toggle_thread(self, slug, is_disabled):
        try:
            self.after(0, self.show_loading)

            toggle_competition(slug, enable=is_disabled)

            self.after(0, self.load_data)

        except Exception as e:
            self.after(0, self.show_error, str(e))

    def show_loading(self):
        self.progress.pack(fill="x", pady=5)
        self.progress.start()

    def show_error(self, msg):
        self.progress.stop()
        self.progress.pack_forget()
        messagebox.showerror("Error", msg)