__author__ = "Clea Parcerisas"
__version__ = "0.1"
__credits__ = "Clea Parcerisas"
__email__ = "clea.parcerisas@vliz.be"
__status__ = "Development"

import matplotlib.pyplot as plt
import numba as nb
import numpy as np
import pandas as pd
import scipy as sci
import seaborn as sns
import xarray
from mpl_toolkits.axes_grid1 import make_axes_locatable

from pypam import utils
from pypam._event import Event
from pypam import plots

# Apply the default theme
sns.set_theme('paper')
sns.set_style('ticks')
sns.set_palette('colorblind')


class ImpulseDetector:
    """
    Impulse events detector

    Parameters
    ----------
    min_separation : float
        Minimum separation of the event, in seconds
    max_duration : float
        Maxium duration of the event, in seconds
    detection_band : list
        List or tuple of (min_freq, max_freq) of the frequency band used to detect the signals
    analysis_band : list
        List or tuple of (min_freq, max_freq) of the frequency band used to characterize the impulses
    threshold : float
        Threshold above ref value which one it is considered piling, in db
    dt : float
        Window size in seconds for the analysis (time resolution). Has to be smaller han
        min_duration!
    """
    def __init__(self, min_separation, max_duration, detection_band, analysis_band, threshold=150, dt=None):
        self.min_separation = min_separation
        self.max_duration = max_duration
        self.threshold = threshold
        self.dt = dt
        self.detection_band = detection_band
        self.analysis_band = analysis_band

    def detect_events(self, signal, method='dt', verbose=False, save_path=None):
        """
        Detect the events

        Parameters
        ---------
        signal : np.array
            Signal to analyze
        method : str
            Can be dt or envelope
        verbose : bool
            Set to True to see the detection signals
        save_path : string or Path
            Where to save the image. Set to None if it should not be saved
        """
        if method == 'dt':
            df = self.detect_events_dt(signal, verbose, save_path)
        elif method == 'envelope':
            df = self.detect_events_envelope(signal, verbose, save_path)
        elif method == 'snr':
            df = self.detect_events_snr(signal, verbose, save_path)
        else:
            raise Exception('Unknown method: ' + method)

        return df

    def detect_events_dt(self, signal, verbose=False, save_path=None):
        """
        Detection of event times. Events are detected on the basis of the SPL time series
        (channel 1)
        The time resolution is dt

        Parameters
        ----------
        signal : Signal object
            Signal to analyze
        verbose : bool
            Set to True to see the detection signals
        save_path : string or Path
            Where to save the image. Set to None if it should not be saved
        """
        signal.set_band(self.detection_band)
        levels = []
        blocksize = int(self.dt * signal.fs)
        for block in signal.Blocks(blocksize=blocksize):
            level = block.rms(db=True)
            levels.append(level)
        times_events = events_times(np.array(levels), self.dt, self.threshold, self.min_separation)
        events_df = self.load_all_times_events(times_events, signal)

        if verbose:
            self.plot_all_events(signal, events_df, save_path)

        return events_df

    def detect_events_envelope(self, signal, verbose=False, save_path=None):
        """
        Detect events using the envelope approach

        Parameters
        ----------
        signal : Signal object
            Signal to analyze
        verbose : bool
            Set to True to see the detection signals
        save_path : string or Path
            Where to save the image. Set to None if it should not be saved
        """
        signal.set_band(band=self.detection_band)
        envelope = signal.envelope()
        times_events = events_times_diff(signal=envelope, fs=signal.fs, threshold=self.threshold,
                                         max_duration=self.max_duration,
                                         min_separation=self.min_separation)
        events_df = self.load_all_times_events(times_events, signal)

        if verbose:
            self.plot_all_events(signal, events_df, save_path)

        return events_df

    def detect_events_snr(self, signal, verbose=False, save_path=None):
        """
        Detect events using the Signal To Noise approach

        Parameters
        ----------
        signal : Signal object
            Signal to analyze
        verbose : bool
            Set to True to see the detection signals
        save_path : string or Path
            Where to save the image. Set to None if it should not be saved
        """
        signal.set_band(band=self.detection_band)
        envelope = signal.envelope()
        blocksize = int(self.dt * signal.fs)
        times_events = events_times_snr(signal=envelope, blocksize=blocksize, fs=signal.fs,
                                        threshold=self.threshold, max_duration=self.max_duration,
                                        min_separation=self.min_separation)

        events_df = self.load_all_times_events(times_events, signal)

        if verbose:
            self.plot_all_events(signal, events_df, save_path)

        return events_df

    def load_event(self, s, t, duration, removenoise=True):
        """
        Load the event at time t (in seconds), with supplied time before and after the event
        (in seconds)
        return an object event
        Parameters
        ----------
        s : Signal object
            Signal where the event is
        t : float
            Starting time of the event (in seconds)
        duration : float
            Duration of the event, in seconds
        removenoise : bool
            Set to True if noise calculated before and after the event can be removed from the event

        """
        start_n = int(t * s.fs)
        end_n = int((t + duration) * s.fs) + 1
        if removenoise:
            n1 = max(int((t - self.min_separation) * s.fs), 0)
            n2 = min(int((t + duration + self.min_separation) * s.fs), s.signal.shape[0])
            event = Event(s.signal, s.fs, start=n1, end=n2)
            event.reduce_noise(nfft=512, verbose=False)
            event.cut(start_n - n1, end_n - n1)
        else:
            event = Event(s.signal, s.fs, start_n, end_n)

        return event

    def load_all_times_events(self, times_events, signal):
        """
        Load in a dataframe all the events and their parameters

        Parameters
        ----------
        times_events : list of tuples
            Each tuple is (start, duration, end) of the event
        signal : Signal object
            Signal where the events were detected
        """
        signal.set_band(self.analysis_band)
        columns_temp = ['start_seconds', 'end_seconds', 'duration', 'rms', 'sel', 'peak']
        columns_df = pd.DataFrame({'variable': 'temporal', 'value': columns_temp})
        freq = sci.fft.rfftfreq(128) * signal.fs
        columns_df = pd.concat([columns_df, pd.DataFrame({'variable': 'psd', 'value': freq})])
        columns = pd.MultiIndex.from_frame(columns_df)
        events_df = pd.DataFrame(columns=columns)
        for i, e in enumerate(times_events):
            start, duration, end = e
            event = self.load_event(s=signal, t=start, duration=duration)
            rms, sel, peak = event.analyze()
            fbands, psd, _ = event.spectrum(scaling='spectrum', nfft=128)
            events_df.at[i, ('temporal', columns_temp)] = [start, end, duration, rms, sel, peak]
            events_df.at[i, ('psd', fbands)] = psd
        return events_df

    def plot_all_events(self, signal, events_df, save_path=None):
        """
        Plot all the events in the dataframe

        Parameters
        ----------
        signal : Signal object
            Signal where the events were detected
        events_df : DataFrame
            DataFrame output of load_all_times_events
        save_path : string or Path
            Where to save the image. Set to None if it should not be saved
        """
        # Filter signal
        signal.set_band(band=self.detection_band)

        # Compute spectrogram
        fbands, t, sxx = signal.spectrogram(nfft=512, scaling='spectrum', db=True)
        spectr_ds = xarray.DataArray(sxx, coords={'frequency': fbands, 'time': t}, dims=['frequency', 'time'])

        # Create plot
        sns.set_theme('paper')
        sns.set_style('ticks')
        sns.set_palette('colorblind')
        fig, ax = plt.subplots(3, 1, sharex='col')
        divider = make_axes_locatable(ax[0])
        cax = divider.append_axes("right", size="5%", pad=.05)
        plots.plot_2d(spectr_ds, x='time', y='frequency', xlabel='', ylabel='Frequency [Hz]', ylog=True,
                      title='Spectrogram', ax=ax[0], cbar_label='$L_{rms} [dB]$', cbar_ax=cax)

        if len(events_df) > 0:
            l0 = ax[2].scatter(events_df[('temporal', 'start_seconds')], events_df[('temporal', 'rms')],
                          marker='.', label=r'$L_{rms}$ [dB re 1 $\mu Pa$]')
            l1 = ax[2].scatter(events_df[('temporal', 'start_seconds')], events_df[('temporal', 'peak')],
                          marker='x', label=r'$L_{z-p}$ [dB re 1 $\mu Pa$]')
            ax[2].scatter(events_df[('temporal', 'start_seconds')], events_df[('temporal', 'sel')],
                          marker='+', label=r'$SEL_{ss}$ [dB re 1 $\mu Pa^2 s$]')
            color0 = l0.get_facecolors()[0]
            color1 = l1.get_facecolors()[0]
        else:
            color0 = 'blue'
            color1 = 'orange'
        ax[2].legend(bbox_to_anchor=(1, 0), loc="lower left")
        ax[2].set_title('Pulses detected')
        ax[2].set_xlabel('Time [s]')
        ax[2].set_ylabel('[dB]')
        divider2 = make_axes_locatable(ax[2])
        cax2 = divider2.append_axes("right", size="5%", pad=.05)
        cax2.remove()
        ax[1].plot(signal.times, utils.to_db(signal.signal, ref=1.0, square=True), label='Signal', color=color0, zorder=2)
        ylims = ax[1].get_ylim()
        ax[1].vlines(x=events_df[('temporal', 'start_seconds')].astype(np.float).values, ymin=ylims[0], ymax=ylims[1],
                     color=color1, label='Detections', zorder=1)
        ax[1].legend(bbox_to_anchor=(1, 0), loc="lower left")
        ax[1].set_title('Detections')
        ax[1].set_ylabel('[dB]')
        divider1 = make_axes_locatable(ax[1])
        cax1 = divider1.append_axes("right", size="5%", pad=.05)
        cax1.remove()
        plt.tight_layout()
        if save_path is not None:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()


class PilingDetector(ImpulseDetector):
    def __init__(self, min_separation, max_duration, threshold, dt, detection_band=None, analysis_band=None):
        if detection_band is None:
            detection_band = [500, 1000]
        if analysis_band is None:
            analysis_band = [100, 20000]
        super().__init__(min_separation=min_separation, max_duration=max_duration,
                         detection_band=detection_band, analysis_band=analysis_band, threshold=threshold, dt=dt)


@nb.jit
def events_times(levels, dt, threshold, min_separation):
    # diff_levels = np.diff(levels)
    indices = np.where(levels >= threshold)[0]
    times_th = indices * dt
    times = []
    for i, t in enumerate(times_th):
        if i == 0:
            times.append(t)
        else:
            if (t - times[-1]) >= min_separation:
                times.append(t)
    return times


@nb.jit
def events_times_diff(signal, fs, threshold, max_duration, min_separation):
    times_events = []
    min_separation_samples = int(min_separation * fs - 1)
    event_on = False
    event_start = 0
    event_max_val = 0
    last_xi = 0
    i = 0
    threshold_upa = 10 ** (threshold/20.0)
    while i < len(signal):
        xi = signal[i]

        if event_on:
            duration = (i - event_start) / fs
            if duration >= max_duration or (event_max_val - xi) >= threshold_upa:
                # Event finished, too long! Or event end detected
                event_on = False
                event_end = i
                times_events.append([event_start / fs, duration, event_end / fs])
                i += min_separation_samples
                event_max_val = 0
            elif xi > event_max_val:
                event_max_val = xi
        else:
            if i != 0 and (xi - last_xi) >= threshold_upa:
                # There is a big jump, start event!
                event_on = True
                event_start = i
                event_max_val = xi
        last_xi = xi
        i += 1
    return times_events


@nb.jit
def events_times_snr(signal, fs, blocksize, threshold, max_duration, min_separation):
    """
    Signal must be an envelope

    :param signal:
    :param fs:
    :param blocksize:
    :param threshold:
    :param max_duration:
    :param min_separation:
    :return:
    """
    signal_db = 10 * np.log10(signal**2)
    times_events = []
    min_separation_samples = int(min_separation * fs)
    event_on = False
    event_start = 0
    event_end = 0
    j = 0
    while j < len(signal):
        if j + blocksize > len(signal):
            blocksize = len(signal) - j
        noise = 10 * np.log10(np.mean(signal[j:j + blocksize] ** 2))
        max_value = noise
        for i in np.arange(blocksize - 1) + j:
            xi = signal_db[i]
            if event_on:
                duration = (i - event_start) / fs
                if duration >= max_duration or (xi - noise) < 3.0:
                    # Event finished, too long! Or event detected!
                    event_on = False
                    event_end = i
                    times_events.append([event_start / fs, duration, event_end / fs])
                if xi > max_value:
                    max_value = xi
            else:
                if (xi - noise) >= threshold:
                    if len(times_events) == 0 or (i - event_end) >= min_separation_samples:
                        event_on = True
                        event_start = i
                        max_value = xi
        j += blocksize

    return times_events
