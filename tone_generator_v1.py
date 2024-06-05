import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ToneGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Tone Generator")
        self.root.geometry("700x500")
        
        self.frequency = 440  # Start with a default frequency
        self.duration = 1  # Duration of the tone in seconds
        self.sample_rate = 44100  # Standard sample rate for audio
        self.volume = 0.5  # Default volume

        self.create_widgets()
        self.update_waveform()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.figure = Figure(figsize=(5, 2), dpi=100)
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

        self.volume_slider = ttk.Scale(frequency_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self.update_volume)
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(fill=tk.X, pady=5)
        self.create_tooltip(self.volume_slider, "Drag to adjust the volume")

        self.play_button = ttk.Button(controls_frame, text="Play Tone", command=self.play_tone)
        self.play_button.pack(side=tk.RIGHT, padx=10)
        self.create_tooltip(self.play_button, "Click to play the tone")

        self.stop_button = ttk.Button(controls_frame, text="Stop Tone", command=self.stop_tone)
        self.stop_button.pack(side=tk.RIGHT, padx=10)
        self.create_tooltip(self.stop_button, "Click to stop the tone")

        self.canvas.mpl_connect("button_press_event", self.on_click)

    def generate_tone(self):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        tone = self.volume * np.sin(2 * np.pi * self.frequency * t)
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
        self.update_waveform()

    def update_volume(self, val):
        self.volume = float(val)

    def on_click(self, event):
        if event.button == 1:  # Left click to increase frequency
            self.frequency += 10
        elif event.button == 3:  # Right click to decrease frequency
            self.frequency -= 10
        self.frequency = max(0, min(self.frequency, 3000))  # Clamp the frequency
        self.frequency_slider.set(self.frequency)
        self.label.config(text=f"Frequency: {self.frequency} Hz")
        self.update_waveform()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = ToneGenerator(root)
    root.mainloop()
