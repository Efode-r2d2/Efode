"""
    < Efode is an an open source audio fingerprinting system>
    Copyright (C) <2019>  <Efriem Desalew Gebie>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import librosa.display


def display_spectrogram(spectrogram, plot_title=""):
    """

    :param spectrogram:
    :param plot_title:
    """
    figure, ax = plt.subplots()
    ax.imshow(spectrogram)
    plt.title(plot_title)
    plt.xlabel("Frame Number")
    plt.ylabel("Frequency Bins")
    plt.show()


def display_audio_waveform(audio_data, sampling_rate, plot_title):
    """

    :param audio_data:
    :param sampling_rate:
    :param plot_title:
    """
    librosa.display.waveplot(audio_data, sr=sampling_rate)
    plt.title(plot_title)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()


def display_scatter_plot(x_axis, y_axis, x_label, y_label, color='r', plot_title=""):
    """

    :param x_axis:
    :param y_axis:
    :param color:
    :param plot_title:
    :param x_label:
    :param y_label:
    """
    plt.scatter(x_axis, y_axis, color=color)
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def display_scatter_plot_2(data, plot_title=""):
    """

    :param data:
    :param plot_title:
    """
    plt.scatter(*zip(*data))
    plt.title(plot_title)
    plt.show()


def display_spectrogram_peaks(spectrogram, spectral_peaks_x, spectral_peaks_y, plot_title=""):
    """

    :param plot_title:
    :param spectrogram:
    :param spectral_peaks_x:
    :param spectral_peaks_y:
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

    :param spectrogram:
    :param spectral_peaks_x:
    :param spectral_peaks_y:
    :param spectral_peaks_x_2:
    :param spectral_peaks_y_2:
    :param plot_title:
    """
    figure, ax = plt.subplots()
    ax.imshow(spectrogram)
    ax.scatter(spectral_peaks_x, spectral_peaks_y, color='r')
    ax.scatter(spectral_peaks_x_2, spectral_peaks_y_2, color='b')
    plt.title(plot_title)
    plt.xlabel("Frame Number")
    plt.ylabel("Frequency Bins")
    plt.show()
