import librosa
import numpy as np
import matplotlib.pyplot as plt

# Load audio file
y, sr = librosa.load("data/audio/om.wav")

# Parameters
frame_length = 2048
hop_length = 512

# Extract fundamental frequency using pyin
f0, voiced_flag, voiced_probs = librosa.pyin(
    y, 
    fmin=librosa.note_to_hz('C2'), 
    fmax=librosa.note_to_hz('C7'), 
    frame_length=frame_length, 
    hop_length=hop_length
)

# Extract RMS amplitude
rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

# Time array
times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)

# Print frequency and amplitude for voiced frames
for t, freq, amp in zip(times, f0, rms):
    if freq is not None and not np.isnan(freq):
        print(f"Time: {t:.2f}s | Frequency: {freq:.2f} Hz | Amplitude: {amp:.4f}")

# Plotting the results
plt.figure(figsize=(10, 4))

plt.subplot(2, 1, 1)
plt.plot(times, f0, label="Fundamental Frequency")
plt.ylabel("Frequency (Hz)")
plt.title("Fundamental Frequency")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(times, rms, label="RMS Amplitude")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (RMS)")
plt.title("Amplitude Envelope")
plt.legend()

plt.tight_layout()
plt.savefig('sound_analysis.png', dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()