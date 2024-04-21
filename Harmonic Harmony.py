import tkinter as tk
from tkinter import ttk, filedialog
import pygame
from tkcalendar import Calendar

class MusicPlayer:
    def __init__(self, root):
        self.root = root

        self.music_frame = ttk.Frame(root)
        self.music_frame.pack(padx=10, pady=10)

        self.music_label = ttk.Label(self.music_frame, text="Music Player")
        self.music_label.pack(pady=10)

        self.play_button = ttk.Button(self.music_frame, text="Play Music", command=self.toggle_music)
        self.play_button.pack(pady=5)

        self.stop_button = ttk.Button(self.music_frame, text="Stop Music", command=self.stop_music)
        self.stop_button.pack(pady=5)

        self.pause_button = ttk.Button(self.music_frame, text="Pause Music", command=self.pause_music)
        self.pause_button.pack(pady=5)

        self.add_button = ttk.Button(self.music_frame, text="Add Music", command=self.add_music)
        self.add_button.pack(pady=5)

        self.progress_label = ttk.Label(self.music_frame, text="Progress: ")
        self.progress_label.pack(pady=5)

        self.music_slider = ttk.Scale(self.music_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_music_position)
        self.music_slider.pack(pady=5)

        self.total_length_label = ttk.Label(self.music_frame, text="Total Length: ")
        self.total_length_label.pack(pady=5)

        self.playlist = []
        self.current_music = None
        self.paused = False

        # Initialize pygame mixer
        pygame.mixer.init()

    def toggle_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        elif self.current_music:
            pygame.mixer.music.load(self.current_music)
            pygame.mixer.music.play()
        elif self.playlist:
            self.current_music = self.playlist[0]
            pygame.mixer.music.load(self.current_music)
            pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def add_music(self):
        music_file = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3")])
        if music_file:
            self.playlist.append(music_file)
            if not self.current_music:
                self.play_button.config(state="normal")
            self.update_music_info()

    def set_music_position(self, value):
        if self.current_music:
            slider_value = float(value)
            total_length = pygame.mixer.Sound(self.current_music).get_length()
            pygame.mixer.music.set_pos(slider_value * total_length / 100)

    def update_music_info(self):
        if self.current_music:
            total_length = pygame.mixer.Sound(self.current_music).get_length()
            self.total_length_label.config(text=f"Total Length: {total_length}")
            self.music_slider.config(to=total_length)
            self.progress_label.config(text="Progress: ")
        else:
            self.total_length_label.config(text="Total Length: ")
            self.music_slider.config(to=100)
            self.progress_label.config(text="Progress: ")

class CalendarApp:
    def __init__(self, root):
        self.root = root

        self.calendar_frame = ttk.Frame(root)
        self.calendar_frame.pack(padx=10, pady=10)

        self.calendar_label = ttk.Label(self.calendar_frame, text="Calendar")
        self.calendar_label.pack(pady=10)

        self.calendar = Calendar(self.calendar_frame, selectmode="day")
        self.calendar.pack(pady=10)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrated App")

        self.tabControl = ttk.Notebook(root)

        self.music_tab = ttk.Frame(self.tabControl)
        self.calendar_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.music_tab, text="Music Player")
        self.tabControl.add(self.calendar_tab, text="Calendar")

        self.tabControl.pack(expand=1, fill="both")

        self.music_player = MusicPlayer(self.music_tab)
        self.calendar_app = CalendarApp(self.calendar_tab)

root = tk.Tk()
app = App(root)
root.mainloop()
