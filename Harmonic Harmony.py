import tkinter as tk
from tkinter import ttk, filedialog
import pygame
from tkcalendar import Calendar

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.playlist = []
        self.paused = False
        self.paused_pos = 0  # To store the position where music was paused

        self.music_frame = ttk.Frame(root)
        self.music_frame.pack(padx=10, pady=10)

        self.music_label = ttk.Label(self.music_frame, text="Music Player")
        self.music_label.pack(pady=10)

        self.play_button = ttk.Button(self.music_frame, text="Play Music", command=self.play_music)
        self.play_button.pack(pady=5)

        self.pause_button = ttk.Button(self.music_frame, text="Pause Music", command=self.pause_music)
        self.pause_button.pack(pady=5)

        self.stop_button = ttk.Button(self.music_frame, text="Stop Music", command=self.stop_music)
        self.stop_button.pack(pady=5)

        self.add_button = ttk.Button(self.music_frame, text="Add Music", command=self.add_music)
        self.add_button.pack(pady=5)

        # Initialize pygame mixer
        pygame.mixer.init()

    def play_music(self):
        if self.playlist:
            if not self.paused:
                pygame.mixer.music.load(self.playlist[0])
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()  # Resume playback from paused position
                self.paused = False

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True
            self.paused_pos = pygame.mixer.music.get_pos()  # Store the paused position

    def stop_music(self):
        pygame.mixer.music.stop()
        self.paused = False
        self.paused_pos = 0  # Reset paused position when music is stopped

    def add_music(self):
        music_file = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3")])
        if music_file:
            self.playlist.append(music_file)
            if len(self.playlist) == 1:
                self.play_button.config(state="normal")
                self.pause_button.config(state="normal")
                self.stop_button.config(state="normal")



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
