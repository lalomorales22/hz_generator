# Hz Generator

A Python application for generating audio tones with customizable frequency, volume, duration, and waveform. The application uses Tkinter for the GUI, Numpy for tone generation, and SoundDevice for audio playback.

## Features

- **Frequency Adjustment:** Adjust the frequency of the generated tone using a slider or input field.
- **Volume Control:** Change the volume of the tone using a slider.
- **Duration Control:** Modify the duration of the tone with a slider.
- **Waveform Selection:** Choose between different waveforms (sine, square, triangle, sawtooth).
- **Play/Stop Tone:** Play and stop the generated tone.
- **Record Tone:** Record the generated tone and save it as a .wav file.
- **Real-time Visualization:** View the waveform of the generated tone.
- **Tooltips:** Tooltips for better user guidance.
- **Keyboard Shortcuts:** Space to play the tone and Escape to stop the tone.

## Installation

### Prerequisites

- Python 3.6 or higher
- Anaconda (optional, but recommended for managing dependencies)

### Step-by-Step Guide

1. **Clone the repository:**

   git clone https://github.com/yourusername/tone-generator.git
   cd tone-generator
   
Create a virtual environment:

python -m venv venv
Activate the virtual environment:

On Windows:
.\venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

Install the required packages:

numpy
sounddevice
matplotlib
scipy
Usage

Run the application:

python tone_generator_v1.py or tone_generator_v2.py

Interact with the GUI:

Adjust the frequency using the slider or enter a specific value in the input field and press Enter.
Change the volume and duration using the respective sliders.
Select the desired waveform from the dropdown menu.
Click "Play Tone" to generate and play the tone.
Click "Stop Tone" to stop the tone.
Click "Record Tone" to save the generated tone as a .wav file.


Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements:
Numpy
SoundDevice
Matplotlib
Scipy
Tkinter

Contact
For any questions or suggestions, please open an issue or contact laloadrianmorales@gmail.com
