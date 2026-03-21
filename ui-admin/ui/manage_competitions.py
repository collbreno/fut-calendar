from tkinter import ttk


class ManageCompetitions(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=20)

        ttk.Label(self, text="Manage Competitions (coming soon)").pack()