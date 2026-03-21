import tkinter as tk
import sv_ttk

from ui.main_menu import MainMenu
from ui.create_competition import CreateCompetition
from ui.manage_competitions import ManageCompetitions


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Competition Manager")

        # Load theme
        sv_ttk.set_theme("dark")

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for FrameClass in (MainMenu, CreateCompetition, ManageCompetitions):
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def show_frame_by_name(self, name):
        for cls, frame in self.frames.items():
            if cls.__name__ == name:
                frame.tkraise()
                return