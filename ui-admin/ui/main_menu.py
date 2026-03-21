import tkinter as tk
from tkinter import ttk
from ui.create_competition import CreateCompetition
from ui.manage_competitions import ManageCompetitions


class MainMenu(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=20)
        self.app = app

        container = ttk.Frame(self)
        container.pack(expand=True)

        ttk.Button(
            container,
            text="Create Competition",
            command=lambda: app.show_frame(CreateCompetition),
            width=30
        ).pack(pady=10)

        ttk.Button(
            container,
            text="Manage Competitions",
            command=lambda: app.show_frame(ManageCompetitions),
            width=30
        ).pack(pady=10)