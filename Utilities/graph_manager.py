import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import librosa.display


def display_spectrogram(spectrogram, plot_title="Spectrogram"):
    """
    A function to plot the spectrogram of an audio.

    Parameters:
        spectrogram (numpy.ndarray): Time-Frequency representation of an audio.
        plot_title (String): Title for the graph.

    """
    figure, ax = plt.subplots()
    ax.imshow(spectrogram)
    plt.title(plot_title)
    plt.xlabel("Frame Number")
    plt.ylabel("Frequency Bins")
    plt.show()


def display_audio_waveform(audio_data, sr, plot_title):
    """
    A function to display monophonic time series representation of an audio.

    Parameters:
          audio_data(numpy.ndarray): Monophonic time series audio data.
          sr (int): A sampling rate at which the given audio data is sampled.
          plot_title (String): A title for the plot.

    """
    librosa.display.waveplot(audio_data, sr=sr)
    plt.title(plot_title)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()


def display_scatter_plot(x_axis, y_axis, x_label, y_label, color='r', plot_title=""):
    """
    A function to draw scatter plot of spectral peaks.

    Parameters:
        x_axis (List): x values of the plot.
        y_axis (List): y values of the plot.
        x_label (String): Label for x-axis.
        y_label (String): Label for y-axis.
        color (char): Color of the plot.
        plot_title: Title of the plot.

    """
    plt.scatter(x_axis, y_axis, color=color)
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def display_scatter_plot_2(data, plot_title=""):
    """
    A function to draw scatter plot of spectral peaks.

    Parameters:
        data (List): list of spectral peaks.
        plot_title (String): Title of the plot.

    """
    plt.scatter(*zip(*data))
    plt.title(plot_title)
    plt.show()


def display_spectrogram_peaks(spectrogram, spectral_peaks_x, spectral_peaks_y, plot_title=""):
    """
    A function  to display spectrogram of the audio along with spectral peaks extracted from it.

    Parameters:
        spectrogram (numpy.ndarray): Time-frequency representation of an audio.
        spectral_peaks_x (List): Tempo information of peaks.
        spectral_peaks_y (List): Pitch information of peaks.
        plot_title (String): Title of the plot.

    """
    figure, ax = plt.subplots()
    ax.imshow(spectrogram)
    ax.scatter(spectral_peaks_x, spectral_peaks_y, color='r')
    plt.title(plot_title)
    plt.xlabel("Frame Number")
    plt.ylabel("Frequency Bins")
    plt.show()


def display_spectrogram_peaks_2(spectrogram, spectral_peaks_x, spectral_peaks_y,
                                spectral_peaks_x_2, spectral_peaks_y_2, plot_title=""):
    """
    A function to display spectrogram of an audio along with its original and modified spectral peaks.

    Parameters:
        spectrogram (numpy.ndarray): Time-Frequency representation of an audio.
        spectral_peaks_x (List): Tempo information for peaks extracted from original audio.
        spectral_peaks_y (List): Pitch information for peaks extracted from original audio.
        spectral_peaks_x_2 (List): Tempo information for peaks extracted from modified audio.
        spectral_peaks_y_2 (List): Pitch information for peaks extracted form modified audio.
        plot_title (String): Title of the plot.

    """
    figure, ax = plt.subplots()
    ax.imshow(spectrogram)
    ax.scatter(spectral_peaks_x, spectral_peaks_y, color='r')
    ax.scatter(spectral_peaks_x_2, spectral_peaks_y_2, color='b')
    plt.title(plot_title)
    plt.xlabel("Frame Number")
    plt.ylabel("Frequency Bins")
    plt.show()
