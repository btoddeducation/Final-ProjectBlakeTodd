import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
from mutagen.mp3 import MP3
from datetime import datetime, timedelta
from datetime import date as dt_date
from tkcalendar import Calendar


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.current_music = None
        self.paused = False  # Add paused attribute
        
        # Initialize pygame mixer
        pygame.mixer.init()

        self.music_frame = ttk.Frame(root)
        self.music_frame.pack(padx=10, pady=10)

        self.music_label = ttk.Label(self.music_frame, text="Music Player")
        self.music_label.pack(pady=10)

        # Create custom image buttons
        self.play_icon = tk.PhotoImage(file="play_icon.png")
        self.pause_icon = tk.PhotoImage(file="pause_icon.png")
        self.stop_icon = tk.PhotoImage(file="stop_icon.png")
        self.prev_icon = tk.PhotoImage(file="prev_icon.png")
        self.next_icon = tk.PhotoImage(file="next_icon.png")

        # Buttons with custom images and labels
        self.play_button = ttk.Button(self.music_frame, image=self.play_icon, command=self.toggle_music, text="Play/Pause")
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.play_button.image = self.play_icon  # Keep reference to the image

        self.prev_button = ttk.Button(self.music_frame, image=self.prev_icon, command=self.previous_music, text="Previous")
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.prev_button.image = self.prev_icon  # Keep reference to the image

        self.next_button = ttk.Button(self.music_frame, image=self.next_icon, command=self.next_music, text="Next")
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.next_button.image = self.next_icon  # Keep reference to the image

        self.stop_button = ttk.Button(self.music_frame, image=self.stop_icon, command=self.stop_music, text="Stop")
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.stop_button.image = self.stop_icon  # Keep reference to the image
        
        # Volume control
        self.volume_label = ttk.Label(self.music_frame, text="Volume:")
        self.volume_label.pack(side=tk.LEFT, padx=5)
        self.volume_scale = ttk.Scale(self.music_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(pygame.mixer.music.get_volume())  # Set initial volume to current volume
        self.volume_scale.pack(side=tk.LEFT, padx=5)

        # Add Music button
        self.add_music_button = ttk.Button(self.music_frame, text="Add Music", command=self.add_music)
        self.add_music_button.pack(side=tk.LEFT, padx=5)

        # Remove Music button
        self.remove_music_button = ttk.Button(self.music_frame, text="Remove Music", command=self.remove_music)
        self.remove_music_button.pack(side=tk.LEFT, padx=5)

        # Playlist display
        self.playlist_label = ttk.Label(self.music_frame, text="Playlist:")
        self.playlist_label.pack(pady=5)

        self.playlist_text = tk.Listbox(self.music_frame, width=50, height=10, selectmode=tk.SINGLE)
        self.playlist_text.pack(pady=5)

        self.playlist = []
        self.current_index = 0
        self.paused = False
        
        # Metadata display
        self.metadata_label = ttk.Label(self.music_frame, text="Metadata:")
        self.metadata_label.pack(pady=5)

        self.metadata_display = tk.Text(self.music_frame, width=50, height=5)
        self.metadata_display.pack(pady=5)
        
        # Bind event handler for playlist selection change
        self.playlist_text.bind("<<ListboxSelect>>", self.show_metadata)

    def add_music(self):
        music_files = filedialog.askopenfilenames(filetypes=[("Music Files", "*.mp3")])
        for music_file in music_files:
            self.playlist.append(music_file)
            # Extracting the song title from the file path
            song_title = music_file.split("/")[-1]  # Assuming Unix-like path separator
            self.playlist_text.insert(tk.END, song_title)

    def remove_music(self):
        selection = self.playlist_text.curselection()
        if selection:
            index = selection[0]
            self.playlist.pop(index)
            self.playlist_text.delete(index)

    def toggle_music(self):
        if self.playlist:
            if pygame.mixer.music.get_busy():  # Check if music is currently playing
                if self.paused:
                    pygame.mixer.music.unpause()  # Unpause the music
                    self.paused = False
                    self.play_button.config(image=self.pause_icon, text="Pause")  # Change button image and label to pause
                else:
                    pygame.mixer.music.pause()  # Pause the music
                    self.paused = True
                    self.play_button.config(image=self.play_icon, text="Play")  # Change button image and label to play
            else:  # If music is not playing, start playing from the current index
                if self.current_index < len(self.playlist):
                    self.current_music = self.playlist[self.current_index]
                    pygame.mixer.music.load(self.current_music)
                    pygame.mixer.music.play()
                    self.play_button.config(image=self.pause_icon, text="Pause")  # Change button image and label to pause
        else:
            print("Playlist is empty.")
            
    
    def set_volume(self, volume):
        volume_level = float(volume)
        pygame.mixer.music.set_volume(volume_level)


    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None
        self.paused = False
        self.play_button.config(image=self.play_icon)  # Change button image to play

    def show_metadata(self, event):
        selection = self.playlist_text.curselection()
        if selection:
            index = selection[0]
            music_file = self.playlist[index]
            try:
                audio = MP3(music_file)
                metadata_text = f"Title: {audio.get('title', 'Unknown Title')}\n" \
                                f"Artist: {audio.get('artist', 'Unknown Artist')}\n" \
                                f"Album: {audio.get('album', 'Unknown Album')}\n" \
                                f"Duration: {round(audio.info.length, 2)} seconds"
                self.metadata_display.delete("1.0", tk.END)  # Clear previous metadata
                self.metadata_display.insert(tk.END, metadata_text)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading metadata: {e}")
                
    def previous_music(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.toggle_music()
        else:
            # Restart the current song if it's the first in the playlist
            if self.current_music:
                pygame.mixer.music.rewind()

    def next_music(self):
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.toggle_music()
        else:
            # If we are at the end of the playlist, loop back to the beginning
            self.current_index = 0
            self.toggle_music()

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.appointments = {}  # Dictionary to store appointments

        self.calendar_frame = ttk.Frame(root)
        self.calendar_frame.pack(padx=10, pady=10)

        self.calendar_label = ttk.Label(self.calendar_frame, text="Calendar")
        self.calendar_label.pack(pady=10)

        self.calendar = Calendar(self.calendar_frame, selectmode="day", date_pattern="mm/dd/yy")
        self.calendar.pack(pady=10)

        self.notes_label = ttk.Label(self.calendar_frame, text="Notes:")
        self.notes_label.pack(pady=5)

        self.notes_entry = ttk.Entry(self.calendar_frame, width=50)
        self.notes_entry.pack(pady=5)

        self.add_appointment_button = ttk.Button(self.calendar_frame, text="Add Appointment", command=self.add_appointment)
        self.add_appointment_button.pack(pady=5)

        self.remove_appointment_button = ttk.Button(self.calendar_frame, text="Remove Appointment", command=self.remove_appointment)
        self.remove_appointment_button.pack(pady=5)

        self.calendar.bind("<<CalendarSelected>>", self.display_appointment_details)
        
        self.appointments_listbox = tk.Listbox(self.calendar_frame, width=50, height=10)
        self.appointments_listbox.pack(pady=5)

    def add_appointment(self):
        selected_date_str = self.calendar.get_date()
        notes = self.notes_entry.get()
        if selected_date_str:
            selected_date = datetime.strptime(selected_date_str, '%m/%d/%y').date()
            if selected_date not in self.appointments:
                self.appointments[selected_date] = []  # Initialize list for the date if not exists
            # Remove numbering prefix from notes
            stripped_notes = notes.split(". ", 1)[-1]
            self.appointments[selected_date].append(stripped_notes)  # Add notes to the list for the date
            print("Appointment saved successfully!")
            self.update_calendar_text(selected_date)
            self.clear_notes_entry()


    def remove_appointment(self):
        selected_date_str = self.calendar.get_date()
        notes = self.notes_entry.get()
        print("Selected Date:", selected_date_str)
        print("Notes:", notes)
        if selected_date_str:
            selected_date = datetime.strptime(selected_date_str, '%m/%d/%y').date()
            print("Appointments for Selected Date:", self.appointments.get(selected_date))
            stripped_notes = notes.split(". ", 1)[-1]  # Remove the prefix "1. " from notes
            if selected_date in self.appointments and stripped_notes in self.appointments[selected_date]:
                self.appointments[selected_date].remove(stripped_notes)
                print("Appointment removed successfully!")
                self.update_calendar_text(selected_date)
            else:
                print("Appointment not found for removal.")


    def display_appointment_details(self, event):
        selected_date_str = self.calendar.get_date()
        if selected_date_str:
            selected_date = datetime.strptime(selected_date_str, '%m/%d/%y').date()
            appointment_text = ""
            if selected_date in self.appointments:
                appointment_text = "\n".join(str(i + 1) + ". " + note for i, note in enumerate(self.appointments[selected_date]))
            self.notes_entry.delete(0, tk.END)
            self.notes_entry.insert(tk.END, appointment_text)
            self.display_appointments_list(selected_date)

    def display_appointments_list(self, selected_date):
            self.appointments_listbox.delete(0, tk.END)  # Clear the listbox
            if selected_date in self.appointments:
                appointments = self.appointments[selected_date]
                if appointments:
                    for appointment in appointments:
                        self.appointments_listbox.insert(tk.END, appointment)
                else:
                    self.appointments_listbox.insert(tk.END, "No appointments for this date")
            else:
                self.appointments_listbox.insert(tk.END, "No appointments for this date")

    def update_calendar_text(self, date):
        if hasattr(self.calendar, '_calevent_dates'):
            # Check if the selected date is within the displayed range
            display_range = self.calendar.get_displayed_month()
            if isinstance(display_range, tuple) and len(display_range) == 2:
                month, year = display_range  # Extract month and year from the tuple
                first_day = datetime(year, month, 1).date()
                last_day = (datetime(year, month, 1) + timedelta(days=32)).date() - timedelta(days=1)

                if isinstance(date, dt_date):  # Ensure date is an instance of datetime.date
                    date = date

                if first_day <= date <= last_day:
                    # Get the day of the week for the selected date
                    day = date.weekday()

                    # Get the date button widget corresponding to the selected date
                    if date in self.calendar._calevent_dates:
                        date_button = self.calendar._calendar[(date.day - 1) + day][0]

                        # Concatenate appointment text for the same date
                        if date in self.appointments:
                            appointment_text = "\n".join(str(i + 1) + ". " + note for i, note in enumerate(self.appointments[date]))
                            date_button.config(text=f"{date.day}\n{appointment_text}", foreground="blue")
                        else:
                            date_button.config(text=f"{date.day}", foreground="black")
                else:
                    print("Selected date is not in the displayed calendar range.")
            else:
                print("Display range is not valid.")


    def clear_notes_entry(self):
        self.notes_entry.delete(0, tk.END)



class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Harmonic Harmony")

        self.tabControl = ttk.Notebook(root)

        self.music_tab = ttk.Frame(self.tabControl)
        self.calendar_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.music_tab, text="Music Player")
        self.tabControl.add(self.calendar_tab, text="Calendar")

        self.tabControl.pack(expand=1, fill="both")

        self.music_player = MusicPlayer(self.music_tab)
        self.calendar_app = CalendarApp(self.calendar_tab)


try:
    root = tk.Tk()
    app = App(root)
    root.mainloop()
except Exception as e:
    print("An error occurred:", e)

