# Importing required libraries
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import sounddevice as sd

class RFIBlocker:
    def __init__(self, sample_rate, interference_band):
        """
        Initialize the RFIBlocker.

        Parameters:
        sample_rate: Sampling rate of the signal (Hz)
        interference_band: Tuple specifying the frequency range of the interference (Hz)
        """
        self.sample_rate = sample_rate
        self.interference_band = interference_band

    def bandstop_filter(self, data):
        """
        Apply a bandstop filter to remove interference.

        Parameters:
        - data: Input signal (1D numpy array)

        Returns:
        - Filtered signal (1D numpy array)
        """
        nyquist = 0.5 * self.sample_rate
        low = self.interference_band[0] / nyquist
        high = self.interference_band[1] / nyquist

        # Design a bandstop filter
        b, a = signal.butter(4, [low, high], btype='bandstop')
        filtered_data = signal.filtfilt(b, a, data)

        return filtered_data

    def record_audio(self, duration):
        """
        Record audio from microphone.

        Parameters:
        - duration: Duration of the recording (seconds)

        Returns:
        - Recorded signal (1D numpy array)
        """
        print("Kindly speak into the microphone.")
        recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='float64')
        sd.wait()  # Wait until recording is finished
        print("Filtering out the noises....")
        print("Noise reduced !")
        
        return recording.flatten()
    

# Main execution
if __name__ == "__main__":
    # Parameters
    sample_rate = 44100  # CD quality
    interference_band = (3000, 3500)  # Example: Removing small high-pitch noise
    duration = 5  # Record for 5 seconds

    rfi_blocker = RFIBlocker(sample_rate, interference_band)

    # Record live audio
    original_signal = rfi_blocker.record_audio(duration)

    # Apply RFI blocking (bandstop filtering)
    filtered_signal = rfi_blocker.bandstop_filter(original_signal)

    # Plot results
    t = np.linspace(0, duration, len(original_signal), endpoint=False)

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(t, original_signal)
    plt.title("Original Signal (Time Domain)")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")

    plt.subplot(2, 2, 2)
    plt.plot(t, filtered_signal)
    plt.title("Filtered Signal (Time Domain)")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")

    plt.subplot(2, 2, 3)
    plt.magnitude_spectrum(original_signal, Fs=sample_rate, scale='dB', color='r')
    plt.title("Original Signal Spectrum")

    plt.subplot(2, 2, 4)
    plt.magnitude_spectrum(filtered_signal, Fs=sample_rate, scale='dB', color='g')
    plt.title("Filtered Signal Spectrum")

    plt.tight_layout()
    plt.show()
