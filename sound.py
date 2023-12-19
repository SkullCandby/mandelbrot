import wave
import numpy as np

samplerate = 44100

# Amplitudes
amp_x = 0.589986 # Left channel
amp_y = 0.523647 # Right channel
# Frequency
freq_x = 350.0 # Left channel
freq_y = 350.0 # Right channel
# Number of seconds
secs = 3

# Generate some audio data for the left channel
time = np.linspace(0, secs, secs*samplerate)
audio_left = amp_x * np.sin(2 * np.pi * freq_x * time)
audio_left = (audio_left * (2 ** 15 - 1)).astype("<h")

# Generate some audio data for the right channel
time = np.linspace(0, secs, secs*samplerate)
audio_right = amp_y * np.sin(2 * np.pi * freq_y * time)
audio_right = (audio_right * (2 ** 15 - 1)).astype("<h")

# Combine the two audio data arrays into a single array with two columns
audio = np.column_stack((audio_left, audio_right))

# Open the wave file
with wave.open("../../Downloads/Mandelbrot (1)/Mandelbrot/sound.wav", "w") as f:
  # Set the number of channels and sample width
  f.setnchannels(2) # Change to 2 for stereo
  f.setsampwidth(2)
  f.setframerate(samplerate)
  # Set the number of frames
  f.setnframes(len(audio))
  # Write the audio data to the wave file
  f.writeframes(audio.tobytes())
  f.close()