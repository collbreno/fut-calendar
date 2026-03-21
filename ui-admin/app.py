import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO
import sv_ttk


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("API GUI")

        sv_ttk.set_theme("dark")

        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=15)
        frame.pack(fill="both", expand=True)

        # --- Slug Input ---
        ttk.Label(frame, text="Slug:").grid(row=0, column=0, sticky="w")
        self.slug_input = ttk.Entry(frame, width=40)
        self.slug_input.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        # --- Checkboxes ---
        checkbox_frame = ttk.LabelFrame(frame, text="Options")
        checkbox_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.create_calendar = tk.BooleanVar()
        self.create_teams = tk.BooleanVar()
        self.create_maps = tk.BooleanVar()
        self.use_mapper = tk.BooleanVar()

        ttk.Checkbutton(
            checkbox_frame, text="Create Calendar", variable=self.create_calendar
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        ttk.Checkbutton(
            checkbox_frame, text="Create Teams", variable=self.create_teams
        ).grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Checkbutton(
            checkbox_frame, text="Create Maps", variable=self.create_maps
        ).grid(row=1, column=0, sticky="w", padx=5, pady=2)

        ttk.Checkbutton(
            checkbox_frame, text="Use Mapper", variable=self.use_mapper
        ).grid(row=1, column=1, sticky="w", padx=5, pady=2)

        # Make columns expand nicely
        checkbox_frame.columnconfigure(0, weight=1)
        checkbox_frame.columnconfigure(1, weight=1)       
        
         # --- Flag Input (Optional) ---
        ttk.Label(frame, text="Flag (optional):").grid(row=3, column=0, sticky="w")
        self.flag_input = ttk.Entry(frame, width=40)
        self.flag_input.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        # --- Submit Button ---
        self.submit_btn = ttk.Button(frame, text="Submit", command=self.on_submit)
        self.submit_btn.grid(row=5, column=0, pady=10, sticky="ew")

        # --- Progress Bar ---
        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.grid(row=5, column=1, pady=10, sticky="ew")
        self.progress.grid_remove()  # 👈 hide initially

        # --- Result Text ---
        self.result_text = tk.Text(frame, height=8, wrap="word")
        self.result_text.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

        # --- Image Display ---
        self.image_label = ttk.Label(frame)
        self.image_label.grid(row=7, column=0, columnspan=2)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def on_submit(self):
        slug = self.slug_input.get().strip()
        flag = self.flag_input.get().strip()

        if not slug:
            messagebox.showerror("Error", "Slug is required")
            return

        options = {
            "create_calendar": self.create_calendar.get(),
            "create_teams": self.create_teams.get(),
            "create_maps": self.create_maps.get(),
            "use_mapper": self.use_mapper.get(),
        }

        # Disable UI + start loading
        self.submit_btn.config(state="disabled")
        self.progress.grid()   # 👈 show
        self.progress.start()

        thread = threading.Thread(
            target=self.run_api,
            args=(slug, flag, options),
            daemon=True
        )
        thread.start()

    def run_api(self, slug, flag, options):
        try:
            result = self.call_api(slug, flag, options)
            self.root.after(0, self.show_result, result)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))

    def call_api(self, slug, flag, options):
        """
        Replace with your real API call
        """
        import time
        time.sleep(2)

        # Example image
        response = requests.get("https://a.espncdn.com/i/leaguelogos/soccer/500/4.png")
        image_url = response.url

        return {
            "text": f"Calendar created! https://calendar.google.com/calendario",
            "image_url": image_url
        }

    def show_result(self, result):
        self.progress.stop()
        self.progress.grid_remove()  # 👈 hide again
        self.submit_btn.config(state="normal")

        # Text
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result["text"])

        # Image
        try:
            response = requests.get(result["image_url"])
            img = Image.open(BytesIO(response.content))
            img.thumbnail((300, 300))

            self.tk_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_image, text="")
        except Exception:
            self.image_label.config(text="Failed to load image", image="")

    def show_error(self, msg):
        self.progress.stop()
        self.progress.grid_remove()  # 👈 hide again
        self.submit_btn.config(state="normal")
        messagebox.showerror("API Error", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()