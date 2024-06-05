import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import square, sawtooth
import wave
import os

class ToneGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Tone Generator")
        self.root.geometry("800x600")
        
        self.frequency = 440  # Start with a default frequency
        self.duration = 1  # Duration of the tone in seconds
        self.sample_rate = 44100  # Standard sample rate for audio
        self.volume = 0.5  # Default volume
        self.waveform = 'sine'  # Default waveform

        self.frequency_entry = None  # Initialize frequency_entry
        self.info_label = None  # Initialize info_label

        self.create_widgets()
        self.update_waveform()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.figure = Figure(figsize=(6, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)

        self.label = ttk.Label(controls_frame, text=f"Frequency: {self.frequency} Hz", font=("Arial", 16))
        self.label.pack(side=tk.LEFT, padx=10)

        frequency_frame = ttk.Frame(controls_frame)
        frequency_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(frequency_frame, text="Adjust Frequency:", font=("Arial", 12)).pack(side=tk.TOP)

        self.frequency_slider = ttk.Scale(frequency_frame, from_=0, to=3000, orient=tk.HORIZONTAL, command=self.update_frequency)
        self.frequency_slider.set(self.frequency)
        self.frequency_slider.pack(fill=tk.X, pady=5)
        self.create_tooltip(self.frequency_slider, "Drag to adjust the frequency")

        volume_frame = ttk.Frame(controls_frame)
        volume_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(volume_frame, text="Adjust Volume:", font=("Arial", 12)).pack(side=tk.TOP)

        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self.update_volume)
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(fill=tk.X, pady=5)
        self.create_tooltip(self.volume_slider, "Drag to adjust the volume")

        duration_frame = ttk.Frame(controls_frame)
        duration_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(duration_frame, text="Adjust Duration:", font=("Arial", 12)).pack(side=tk.TOP)

        self.duration_slider = ttk.Scale(duration_frame, from_=0.1, to=10, orient=tk.HORIZONTAL, command=self.update_duration)
        self.duration_slider.set(self.duration)
        self.duration_slider.pack(fill=tk.X, pady=5)
        self.create_tooltip(self.duration_slider, "Drag to adjust the duration")

        self.frequency_entry = ttk.Entry(controls_frame, font=("Arial", 12), width=10)
        self.frequency_entry.insert(0, str(self.frequency))
        self.frequency_entry.pack(side=tk.LEFT, padx=10)
        self.frequency_entry.bind("<Return>", self.update_frequency_from_entry)
        self.create_tooltip(self.frequency_entry, "Enter frequency and press Enter")

        waveform_frame = ttk.Frame(controls_frame)
        waveform_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(waveform_frame, text="Select Waveform:", font=("Arial", 12)).pack(side=tk.TOP)

        self.waveform_combobox = ttk.Combobox(waveform_frame, values=["sine", "square", "triangle", "sawtooth"], state="readonly")
        self.waveform_combobox.set(self.waveform)
        self.waveform_combobox.pack(fill=tk.X, pady=5)
        self.waveform_combobox.bind("<<ComboboxSelected>>", self.update_waveform_selection)
        self.create_tooltip(self.waveform_combobox, "Select waveform")

        self.play_button = ttk.Button(controls_frame, text="Play Tone", command=self.play_tone)
        self.play_button.pack(side=tk.RIGHT, padx=10)
        self.create_tooltip(self.play_button, "Click to play the tone")

        self.stop_button = ttk.Button(controls_frame, text="Stop Tone", command=self.stop_tone)
        self.stop_button.pack(side=tk.RIGHT, padx=10)
        self.create_tooltip(self.stop_button, "Click to stop the tone")

        self.record_button = ttk.Button(controls_frame, text="Record Tone", command=self.record_tone)
        self.record_button.pack(side=tk.RIGHT, padx=10)
        self.create_tooltip(self.record_button, "Click to record the tone")

        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.root.bind("<space>", lambda event: self.play_tone())
        self.root.bind("<Escape>", lambda event: self.stop_tone())

        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=10)

        self.info_label = ttk.Label(info_frame, text=self.get_tone_info(), font=("Arial", 14))
        self.info_label.pack(side=tk.LEFT, padx=10)

    def generate_tone(self):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        if self.waveform == 'sine':
            tone = self.volume * np.sin(2 * np.pi * self.frequency * t)
        elif self.waveform == 'square':
            tone = self.volume * square(2 * np.pi * self.frequency * t)
        elif self.waveform == 'triangle':
            tone = self.volume * sawtooth(2 * np.pi * self.frequency * t, 0.5)
        elif self.waveform == 'sawtooth':
            tone = self.volume * sawtooth(2 * np.pi * self.frequency * t)
        return t, tone

    def play_tone(self):
        if 0 <= self.frequency <= 3000:
            tone = self.generate_tone()[1]
            sd.play(tone, samplerate=self.sample_rate)
        else:
            print("Frequency must be between 0 and 3000 Hz.")

    def stop_tone(self):
        sd.stop()

    def update_waveform(self):
        t, tone = self.generate_tone()
        self.ax.clear()
        self.ax.plot(t[:1000], tone[:1000])  # Plot a small portion of the wave for visualization
        self.ax.set_title(f"Waveform of {self.frequency} Hz Tone")
        self.canvas.draw()

    def update_frequency(self, val):
        self.frequency = int(float(val))
        self.label.config(text=f"Frequency: {self.frequency} Hz")
        self.frequency_entry.delete(0, tk.END)
        self.frequency_entry.insert(0, str(self.frequency))
        self.update_waveform()
        self.update_info()

    def update_frequency_from_entry(self, event):
        try:
            freq = int(self.frequency_entry.get())
            self.frequency = max(0, min(freq, 3000))
            self.frequency_slider.set(self.frequency)
            self.label.config(text=f"Frequency: {self.frequency} Hz")
            self.update_waveform()
            self.update_info()
        except ValueError:
            pass

    def update_volume(self, val):
        self.volume = float(val)
        self.update_info()

    def update_duration(self, val):
        self.duration = float(val)
        self.update_waveform()
        self.update_info()

    def update_waveform_selection(self, event):
        self.waveform = self.waveform_combobox.get()
        self.update_waveform()

    def on_click(self, event):
        if event.button == 1:  # Left click to increase frequency
            self.frequency += 10
        elif event.button == 3:  # Right click to decrease frequency
            self.frequency -= 10
        self.frequency = max(0, min(self.frequency, 3000))  # Clamp the frequency
        self.frequency_slider.set(self.frequency)
        self.label.config(text=f"Frequency: {self.frequency} Hz")
        self.update_waveform()
        self.update_info()

    def get_tone_info(self):
        return f"Current Tone: Frequency = {self.frequency} Hz, Volume = {self.volume:.2f}, Duration = {self.duration} s, Waveform = {self.waveform}"

    def update_info(self):
        self.info_label.config(text=self.get_tone_info())

    def create_tooltip(self, widget, text):
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        label = ttk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
        label.pack()
        tooltip.withdraw()

        def show_tooltip(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def hide_tooltip(event):
            tooltip.withdraw()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def record_tone(self):
        tone = self.generate_tone()[1]
        file_path = 'tone.wav'
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes((tone * 32767).astype(np.int16).tobytes())
        print(f"Tone recorded to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToneGenerator(root)
    root.mainloop()
