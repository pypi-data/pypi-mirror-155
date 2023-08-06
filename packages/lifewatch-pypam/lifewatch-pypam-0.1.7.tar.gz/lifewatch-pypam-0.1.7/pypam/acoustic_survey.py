__author__ = "Clea Parcerisas"
__version__ = "0.1"
__credits__ = "Clea Parcerisas"
__email__ = "clea.parcerisas@vliz.be"
__status__ = "Development"

import datetime
import operator
import os
import pathlib
import zipfile

import dateutil.parser as parser
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xarray
from tqdm import tqdm

from pypam import acoustic_file
from pypam import loud_event_detector
from pypam import plots
from pypam import utils

# Apply the default theme
sns.set_theme()


class ASA:
    """
    Init a AcousticSurveyAnalysis (ASA)

    Parameters
    ----------
    hydrophone : Hydrophone class from pyhydrophone
    folder_path : string or Path
        Where all the sound files are
    zipped : boolean
        Set to True if the directory is zipped
    include_dirs : boolean
        Set to True if the folder contains other folders with sound files
    p_ref : float
        Reference pressure in uPa
    binsize : float
        Time window considered, in seconds. If set to None, only one value is returned
    nfft : int
        Samples of the fft bin used for the spectral analysis
    overlap : float [0 to 1]
        Percentage to overlap the bin windows
    period : tuple or list
        Tuple or list with two elements: start and stop. Has to be a string in the
        format YYYY-MM-DD HH:MM:SS
    calibration: float, -1 or None
        If float, it is the time ignored a the beginning of the file. If None, nothing is done. If negative,
        the function calibrate from the hydrophone is performed, and the first samples ignored (and hydrophone updated)
    dc_subtract: bool
        Set to True to subtract the dc noise (root mean squared value
    timezone: datetime.tzinfo, pytz.tzinfo.BaseTZInfo, dateutil.tz.tz.tzfile, or None
        Timezone where the data was recorded in
    """

    def __init__(self,
                 hydrophone: object,
                 folder_path,
                 zipped=False,
                 include_dirs=False,
                 p_ref=1.0,
                 binsize=None,
                 nfft=1.0,
                 overlap=0,
                 period=None,
                 timezone='UTC',
                 channel=0,
                 calibration=None,
                 dc_subtract=False,
                 extra_attrs=None):

        self.hydrophone = hydrophone
        self.acu_files = AcousticFolder(folder_path=folder_path, zipped=zipped,
                                        include_dirs=include_dirs)
        self.p_ref = p_ref
        self.binsize = binsize
        self.nfft = nfft
        self.overlap = overlap

        if period is not None:
            if not isinstance(period[0], datetime.datetime):
                start = parser.parse(period[0])
                end = parser.parse(period[1])
                period = [start, end]
        self.period = period

        self.timezone = timezone
        self.channel = channel
        self.calibration = calibration
        self.dc_subtract = dc_subtract

        if extra_attrs is None:
            self.extra_attrs = {}
        else:
            self.extra_attrs = {}

        self.file_dependent_attrs = ['hydrophone_sensitivity', 'hydrophone_preamp_gain', 'hydrophone_Vpp', 'file_path',
                                     '_start_frame']

    def _files(self):
        """
        Iterator that returns AcuFile for each wav file in the folder
        """
        for file_list in tqdm(self.acu_files):
            wav_file = file_list[0]
            print(wav_file)
            sound_file = self._hydro_file(wav_file)
            if sound_file.is_in_period(self.period) and sound_file.file.frames > 0:
                yield sound_file

    def _hydro_file(self, wav_file):
        """
        Return the AcuFile object from the wav_file
        Parameters
        ----------
        wav_file : str or Path
            Sound file

        Returns
        -------
        Object AcuFile
        """
        hydro_file = acoustic_file.AcuFile(sfile=wav_file, hydrophone=self.hydrophone, p_ref=self.p_ref,
                                           timezone=self.timezone, channel=self.channel, calibration=self.calibration,
                                           dc_subtract=self.dc_subtract)
        return hydro_file
    
    def _get_metadata_attrs(self):
        metadata_keys = [
            'binsize',
            'nfft',
            'overlap',
            'timezone',
            'p_ref',
            'hydrophone.name',
            'hydrophone.model',
            'channel',
            'dc_subtract'
        ]
        metadata_attrs = self.extra_attrs.copy()
        for k in metadata_keys:
            d = self
            for sub_k in k.split('.'):
                d = d.__dict__[sub_k]
            if isinstance(d, pathlib.Path):
                d = str(d)
            metadata_attrs[k.replace('.', '_')] = d

        return metadata_attrs

    def evolution_multiple(self, method_list: list, band_list=None, **kwargs):
        """
        Compute the method in each file and output the evolution
        Returns a xarray DataSet with datetime as index and one row for each bin of each file

        Parameters
        ----------
        method_list : string
            Method name present in AcuFile
        list of tuples, tuple or None
            Bands to filter. Can be multiple bands (all of them will be analyzed) or only one band. A band is
            represented with a tuple as (low_freq, high_freq). If set to None, the broadband up to the Nyquist
            frequency will be analyzed
        **kwargs :
            Any accepted parameter for the method_name
        """
        ds = xarray.Dataset(attrs=self._get_metadata_attrs())
        f = operator.methodcaller('_apply_multiple', method_list=method_list, binsize=self.binsize,
                                  nfft=self.nfft, overlap=self.overlap, band_list=band_list, **kwargs)
        for sound_file in self._files():
            ds_output = f(sound_file)
            ds = utils.merge_ds(ds, ds_output, self.file_dependent_attrs)
        return ds

    def evolution(self, method_name, band_list=None, **kwargs):
        """
        Evolution of only one param name

        Parameters
        ----------
        method_name : string
            Method to compute the evolution of
        band_list: list of tuples, tuple or None
            Bands to filter. Can be multiple bands (all of them will be analyzed) or only one band. A band is
            represented with a tuple as (low_freq, high_freq). If set to None, the broadband up to the Nyquist
            frequency will be analyzed
        **kwargs : any arguments to be passed to the method
        """
        return self.evolution_multiple(method_list=[method_name], band_list=band_list, **kwargs)

    def evolution_freq_dom(self, method_name, **kwargs):
        """
        Returns the evolution of frequency domain parameters
        Parameters
        ----------
        method_name : str
            Name of the method of the acoustic_file class to compute
        Returns
        -------
        A xarray DataSet with a row per bin with the method name output
        """
        ds = xarray.Dataset(attrs=self._get_metadata_attrs())
        f = operator.methodcaller(method_name, binsize=self.binsize, nfft=self.nfft, overlap=self.overlap, **kwargs)
        for sound_file in self._files():
            ds_output = f(sound_file)
            ds = utils.merge_ds(ds, ds_output, self.file_dependent_attrs)
        return ds

    def timestamps_array(self):
        """
        Return an xarray DataSet with the timestamps of each bin.
        """
        ds = xarray.Dataset(attrs=self._get_metadata_attrs())
        f = operator.methodcaller('timestamp_da', binsize=self.binsize, overlap=self.overlap)
        for sound_file in self._files():
            ds_output = f(sound_file)
            ds = utils.merge_ds(ds, ds_output, self.file_dependent_attrs)
        return ds

    def start_end_timestamp(self):
        """
        Return the start and the end timestamps
        """
        wav_file = self.acu_files[0][0]
        print(wav_file)

        sound_file = self._hydro_file(wav_file)
        start_datetime = sound_file.date

        file_list = self.acu_files[-1]
        wav_file = file_list[0]
        print(wav_file)
        sound_file = self._hydro_file(wav_file)
        end_datetime = sound_file.date + datetime.timedelta(seconds=sound_file.total_time())

        return start_datetime, end_datetime

    def apply_to_all(self, method_name, **kwargs):
        """
        Apply the method to all the files

        Parameters
        ----------
        method_name : string
            Method name present in AcuFile
        **kwargs :
            Any accepted parameter for the method_name

        """
        f = operator.methodcaller(method_name, binsize=self.binsize, nfft=self.nfft, overlap=self.overlap, **kwargs)
        for sound_file in self._files():
            f(sound_file)

    def duration(self):
        """
        Return the duration in seconds of all the survey
        """
        total_time = 0
        for sound_file in self._files():
            total_time += sound_file.total_time()

        return total_time

    def mean_rms(self, **kwargs):
        """
        Return the mean root mean squared value of the survey
        Accepts any other input than the correspondent method in the acoustic file.
        Returns the rms value of the whole survey

        Parameters
        ----------
        **kwargs :
            Any accepted arguments for the rms function of the AcuFile
        """
        rms_evolution = self.evolution('rms', **kwargs)
        return rms_evolution['rms'].mean()

    def spd(self, db=True, h=0.1, percentiles=None, min_val=None, max_val=None):
        """
        Return the empirical power density.

        Parameters
        ----------
        db : boolean
            If set to True the result will be given in db. Otherwise in uPa^2
        h : float
            Histogram bin (in the correspondent units, uPa or db)
        percentiles : list
            All the percentiles that have to be returned. If set to None, no percentiles
            is returned
        min_val : float
            Minimum value to compute the SPD histogram
        max_val : float
            Maximum value to compute the SPD histogram

        Returns
        -------
        percentiles : array like
            List of the percentiles calculated
        p : numpy matrix
            Matrix with all the probabilities
        """
        psd_evolution = self.evolution_freq_dom('psd', db=db, percentiles=percentiles)
        return acoustic_file.compute_spd(psd_evolution, h=h, percentiles=percentiles, min_val=min_val, max_val=max_val)

    def cut_and_place_files_period(self, period, folder_name, extensions=None):
        """
        Cut the files in the specified periods and store them in the right folder

        Parameters
        ----------
        period: Tuple or list
            Tuple or list with (start, stop)
        folder_name: str or Path
            Path to the location of the files to cut
        extensions: list of strings
            the extensions that want to be moved (csv will be splitted, log will just be moved)
        """
        if extensions is None:
            extensions = []
        start_date = parser.parse(period[0])
        end_date = parser.parse(period[1])
        print(start_date, end_date)
        folder_path = self.acu_files.folder_path.joinpath(folder_name)
        self.acu_files.extensions = extensions
        for file_list in tqdm(self.acu_files):
            wav_file = file_list[0]
            sound_file = self._hydro_file(wav_file)
            if sound_file.contains_date(start_date) and sound_file.file.frames > 0:
                print('start!', wav_file)
                # Split the sound file in two files
                first, second = sound_file.split(start_date)
                move_file(second, folder_path)
                # Split the metadata files
                for i, metadata_file in enumerate(file_list[1:]):
                    if extensions[i] not in ['.log.xml', '.sud', '.bcl', '.dwv']:
                        ds = pd.read_csv(metadata_file)
                        ds['datetime'] = pd.to_datetime(ds['unix time'] * 1e9)
                        ds_first = ds[ds['datetime'] < start_date]
                        ds_second = ds[ds['datetime'] >= start_date]
                        ds_first.to_csv(metadata_file)
                        new_metadata_path = second.parent.joinpath(
                            second.name.replace('.wav', extensions[i]))
                        ds_second.to_csv(new_metadata_path)
                        # Move the file
                        move_file(new_metadata_path, folder_path)
                    else:
                        move_file(metadata_file, folder_path)

            elif sound_file.contains_date(end_date):
                print('end!', wav_file)
                # Split the sound file in two files
                first, second = sound_file.split(end_date)
                move_file(first, folder_path)
                # Split the metadata files
                for i, metadata_file in enumerate(file_list[1:]):
                    if extensions[i] not in ['.log.xml', '.sud', '.bcl', '.dwv']:
                        ds = pd.read_csv(metadata_file)
                        ds['datetime'] = pd.to_datetime(ds['unix time'] * 1e9)
                        ds_first = ds[ds['datetime'] < start_date]
                        ds_second = ds[ds['datetime'] >= start_date]
                        ds_first.to_csv(metadata_file)
                        new_metadata_path = second.parent.joinpath(
                            second.name.replace('.wav', extensions[i]))
                        ds_second.to_csv(new_metadata_path)
                    # Move the file (also if log)
                    move_file(metadata_file, folder_path)

            else:
                if sound_file.is_in_period([start_date, end_date]):
                    print('moving', wav_file)
                    sound_file.file.close()
                    move_file(wav_file, folder_path)
                    for metadata_file in file_list[1:]:
                        move_file(metadata_file, folder_path)
                else:
                    pass
        return 0

    def detect_piling_events(self, min_separation, max_duration, threshold, dt=None, verbose=False, detection_band=None,
                             analysis_band=None, **kwargs):
        """
        Return a DataFrame with all the piling events and their rms, sel and peak values

        Parameters
        ----------
        min_separation : float
            Minimum separation of the event, in seconds
        max_duration : float
            Maximum duration of the event, in seconds
        threshold : float
            Threshold above ref value which one it is considered piling, in db
        detection_band : list or tuple
            Band used to detect the pulses [low_freq, high_freq]
        analysis_band : list or tuple
            Band used to analyze the pulses [low_freq, high_freq]
        dt : float
            Window size in seconds for the analysis (time resolution). Has to be smaller
            than min_duration!
        verbose : boolean
            Set to True to plot the detected events per bin
        """
        df = pd.DataFrame()
        for sound_file in self._files():
            df_output = sound_file.detect_piling_events(min_separation=min_separation,
                                                        threshold=threshold,
                                                        max_duration=max_duration,
                                                        dt=dt, binsize=self.binsize,
                                                        detection_band=detection_band,
                                                        analysis_band=analysis_band,
                                                        verbose=verbose, **kwargs)
            df = df.append(df_output)
        return df

    def detect_ship_events(self, min_duration, threshold):
        """
        Return a xarray DataSet with all the piling events and their rms, sel and peak values

        Parameters
        ----------
        min_duration : float
            Minimum separation of the event, in seconds
        threshold : float
            Threshold above ref value which one it is considered piling, in db
        """
        df = pd.DataFrame()
        last_end = None
        detector = loud_event_detector.ShipDetector(min_duration=min_duration,
                                                    threshold=threshold)
        for file_list in tqdm(self.acu_files):
            wav_file = file_list[0]
            print(wav_file)
            sound_file = self._hydro_file(wav_file)
            start_datetime = sound_file.date
            end_datetime = sound_file.date + datetime.timedelta(seconds=sound_file.total_time())
            if last_end is not None:
                if (last_end - start_datetime).total_seconds() < min_duration:
                    detector.reset()
            last_end = end_datetime
            if sound_file.is_in_period(self.period) and sound_file.file.frames > 0:
                df_output = sound_file.detect_ship_events(min_duration=min_duration,
                                                          threshold=threshold,
                                                          binsize=self.binsize, detector=detector,
                                                          verbose=True)
                df = df.append(df_output)
        return df

    def source_separation(self, window_time=1.0, n_sources=15, save_path=None, verbose=False, band=None):
        """
        Separate the signal in n_sources sources, using non negative matrix factorization
        Parameters
        ----------
        window_time: float
            Duration of the window in seconds
        n_sources: int
            Number of sources to separate the sound in
        save_path: str or Path
            Where to save the output
        verbose: bool
            Set to True to make plots of the process
        band : tuple or list
            Tuple or list with two elements: low-cut and high-cut of the band to analyze
        """
        ds = xarray.Dataset(attrs=self._get_metadata_attrs())
        for sound_file in self._files():
            nmf_ds = sound_file.source_separation(window_time, n_sources, binsize=self.binsize, band=band,
                                                  save_path=save_path, verbose=verbose)
            ds = utils.merge_ds(ds, nmf_ds, self.file_dependent_attrs)

        return ds

    def plot_rms_evolution(self, db=True, save_path=None):
        """
        Plot the rms evolution

        Parameters
        ----------
        db : boolean
            If set to True, output in db
        save_path : string or Path
            Where to save the output graph. If None, it is not saved
        """
        rms_evolution = self.evolution('rms', db=db)
        plt.figure()
        plt.plot(rms_evolution['rms'])
        plt.xlabel('Time')
        if db:
            units = r'db re 1V %s $\mu Pa$' % self.p_ref
        else:
            units = r'$\mu Pa$'
        plt.title('Evolution of the broadband rms value')  # Careful when filter applied!
        plt.ylabel('rms [%s]' % units)
        plt.tight_layout()
        if save_path is not None:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()

    def plot_rms_daily_patterns(self, db=True, save_path=None):
        """
        Plot the daily rms patterns

        Parameters
        ----------
        db : boolean
            If set to True, output in db
        save_path : string or Path
            Where to save the output graph. If None, it is not saved
        """
        rms_evolution = self.evolution('rms', db=db)
        rms_evolution['date'] = rms_evolution.datetime.date.unique()
        rms_evolution['hour'] = rms_evolution.datetime.time
        dates = rms_evolution['dates'].unique()
        hours = rms_evolution['hours'].unique()
        daily_patterns = xarray.Dataset()
        for date in dates:
            for hour in hours:
                rms = rms_evolution[(rms_evolution['date'] == date) and
                                    (rms_evolution['hour'] == hour)]['rms']
                daily_patterns.loc[date, hour] = rms

        # Plot the patterns
        plt.figure()
        im = plt.pcolormesh(daily_patterns.values)
        plt.title('Daily patterns')
        plt.xlabel('Hours of the day')
        plt.ylabel('Days')

        if db:
            units = r'db re 1V %s $\mu Pa $' % self.p_ref
        else:
            units = r'$\mu Pa $'
        cbar = plt.colorbar(im)
        cbar.set_label('rms [%s]' % units, rotation=270)
        plt.tight_layout()
        if save_path is not None:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()

    def plot_mean_power_spectrum(self, db=True, save_path=None, log=True, **kwargs):
        """
        Plot the resulting mean power spectrum

        Parameters
        ----------
        db : boolean
            If set to True, output in db
        log : boolean
            If set to True, y axis in logarithmic scale
        save_path : string or Path
            Where to save the output graph. If None, it is not saved
        **kwargs : Any accepted for the power_spectrum method
        """
        power = self.evolution_freq_dom(method_name='power_spectrum', db=db, **kwargs)
        if db:
            units = r'db re 1V %s $\mu Pa^2$' % self.p_ref
        else:
            units = r'$\mu Pa^2$'

        return plots.plot_spectrum_mean(ds=power, units=units, col_name='band_power',
                                        output_name='SPLrms', save_path=save_path, log=log)

    def plot_mean_psd(self, db=True, save_path=None, log=True, **kwargs):
        """
        Plot the resulting mean psd

        Parameters
        ----------
        db : boolean
            If set to True, output in db
        log : boolean
            If set to True, y axis in logarithmic scale
        save_path : string or Path
            Where to save the output graph. If None, it is not saved
        **kwargs : Any accepted for the psd method
        """
        psd = self.evolution_freq_dom(method_name='psd', db=db, **kwargs)
        if db:
            units = r'db re 1V %s $\mu Pa^2$' % self.p_ref
        else:
            units = r'$\mu Pa^2$'

        return plots.plot_spectrum_mean(ds=psd, units=units, col_name='band_density',
                                        output_name='PSD', save_path=save_path, log=log)

    def plot_power_ltsa(self, db=True, save_path=None, **kwargs):
        """
        Plot the evolution of the power frequency distribution (Long Term Spectrogram Analysis)

        Parameters
        ----------
        db : boolean
            If set to True, output in db
        save_path : string or Path
            Where to save the output graph. If None, it is not saved
        **kwargs : Any accepted for the power spectrum method
        """
        power_evolution = self.evolution('power_spectrum', db=db, **kwargs)
        if db:
            units = r'db re 1V %s $\mu Pa^2$' % self.p_ref
        else:
            units = r'$\mu Pa^2$'
        self._plot_ltsa(ds=power_evolution, col_name='spectrum',
                        output_name='SPLrms', units=units, save_path=save_path)

        return power_evolution

    def plot_psd_ltsa(self, db=True, save_path=None, **kwargs):
        """
        Plot the evolution of the psd power spectrum density (Long Term Spectrogram Analysis)

        Parameters
        ----------
        db : boolean
            If set to True, output in db
        save_path : string or Path
            Where to save the output graph. If None, it is not saved
        **kwargs : Any accepted for the psd method
        """
        psd_evolution = self.evolution('psd', db=db, **kwargs)
        if db:
            units = r'db re 1V %s $\mu Pa^2/Hz$' % self.p_ref
        else:
            units = r'$\mu Pa^2/Hz$'
        self._plot_ltsa(ds=psd_evolution, col_name='density',
                        output_name='PSD', units=units, save_path=save_path)

        return psd_evolution

    def _plot_ltsa(self, ds, col_name, output_name, units, save_path=None):
        """
        Plot the evolution of the ds containing percentiles and band values

        Parameters
        ----------
        ds : xarray DataSet
            Output of evolution
        units : string
            Units of the spectrum
        col_name : string
            Column name of the value to plot. Can be 'density' or 'spectrum'
        output_name : string
            Name of the label. 'PSD' or 'SPLrms'
        save_path : string or Path
            Where to save the output graph. If None, it is not saved
        """
        # Plot the evolution
        # Extra axes for the colorbar and delete the unused one
        fig, ax = plt.subplots(2, 2, sharex='col', gridspec_kw={'width_ratios': (15, 1)})
        fbands = ds['band_' + col_name].columns
        im = ax[0, 0].pcolormesh(ds.index, fbands,
                                 ds['band_' + col_name][fbands].T.to_numpy(dtype=np.float),
                                 shading='auto')
        ax[0, 0].set_title('%s evolution' % (col_name.capitalize()))
        ax[0, 0].set_xlabel('Time')
        ax[0, 0].set_ylabel('Frequency [Hz]')
        cbar = fig.colorbar(im, cax=ax[0, 1])
        cbar.set_label('%s [%s]' % (output_name, units), rotation=90)
        # Remove the unused axes
        ax[1, 1].remove()

        ax[1, 0].plot(ds['percentiles'])
        ax[1, 0].set_title('Percentiles evolution')
        ax[1, 0].set_xlabel('Time')
        ax[1, 0].set_ylabel('%s [%s]' % (output_name, units))
        ax[1, 0].legend(ds['percentiles'].columns.values)

        plt.tight_layout()
        if save_path is not None:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()

    def plot_spd(self, db=True, log=True, save_path=None, **kwargs):
        """
        Plot the the SPD graph

        Parameters
        ----------
        db : boolean
            If set to True, output in db
        log : boolean
            If set to True, y axis in logarithmic scale
        save_path : string or Path
            Where to save the output graph. If None, it is not saved
        **kwargs : Any accepted for the spd method
        """
        spd_ds = self.spd(db=db, **kwargs)
        plots.plot_spd(spd_ds, db=db, log=log, save_path=save_path, p_ref=self.p_ref)

    def save(self, file_path):
        """
        Save the ASA with all the computed values
        Returns
        -------

        """


class AcousticFolder:
    """
    Class to help through the iterations of the acoustic folder.
    """

    def __init__(self, folder_path, zipped=False, include_dirs=False, extensions=None):
        """
        Store the information about the folder.
        It will create an iterator that returns all the pairs of extensions having the same
        name than the wav file

        Parameters
        ----------
        folder_path : string or Path
            Path to the folder containing the acoustic files
        zipped : boolean
            Set to True if the subfolders are zipped
        include_dirs : boolean
            Set to True if the subfolders are included in the study
        extensions : list
            List of strings with all the extensions that will be returned (.wav is automatic)
            i.e. extensions=['.xml', '.bcl'] will return [wav, xml and bcl] files
        """
        self.folder_path = pathlib.Path(folder_path)
        self.zipped = zipped
        self.recursive = include_dirs
        if extensions is None:
            extensions = []
        self.extensions = extensions

    def __getitem__(self, n):
        """
        Get n wav file
        """
        self.__iter__()
        self.n = n
        return self.__next__()

    def __iter__(self):
        """
        Iteration
        """
        self.n = 0
        if not self.zipped:
            if self.recursive:
                self.files_list = sorted(self.folder_path.glob('**/*.wav'))
            else:
                self.files_list = sorted(self.folder_path.glob('*.wav'))
        else:
            if self.recursive:
                self.folder_list = sorted(self.folder_path.iterdir())
                self.zipped_subfolder = AcousticFolder(self.folder_list[self.n],
                                                       extensions=self.extensions,
                                                       zipped=self.zipped,
                                                       include_dirs=self.recursive)
            else:
                zipped_folder = zipfile.ZipFile(self.folder_path, 'r', allowZip64=True)
                self.files_list = zipped_folder.namelist()
        return self

    def __next__(self):
        """
        Next wav file
        """
        if self.n < len(self.files_list):
            files_list = []
            if self.zipped:
                if self.recursive:
                    try:
                        self.files_list = self.zipped_subfolder.__next__()
                    except StopIteration:
                        self.n += 1
                        self.zipped_subfolder = AcousticFolder(self.folder_list[self.n],
                                                               extensions=self.extensions,
                                                               zipped=self.zipped,
                                                               include_dirs=self.recursive)
                else:
                    file_name = self.files_list[self.n]
                    extension = file_name.split(".")[-1]
                    if extension == 'wav':
                        wav_file = self.folder_path.open(file_name)
                        files_list.append(wav_file)
                        for extension in self.extensions:
                            ext_file_name = file_name.parent.joinpath(
                                file_name.name.replace('.wav', extension))
                            files_list.append(self.folder_path.open(ext_file_name))
                    self.n += 1
                    return files_list
            else:
                wav_path = self.files_list[self.n]
                files_list.append(wav_path)
                for extension in self.extensions:
                    files_list.append(pathlib.Path(str(wav_path).replace('.wav', extension)))

                self.n += 1
                return files_list
        else:
            raise StopIteration

    def __len__(self):
        if not self.zipped:
            if self.recursive:
                n_files = len(list(self.folder_path.glob('**/*.wav')))
            else:
                n_files = len(list(self.folder_path.glob('*.wav')))
        else:
            if self.recursive:
                n_files = len(list(self.folder_path.iterdir()))
            else:
                zipped_folder = zipfile.ZipFile(self.folder_path, 'r', allowZip64=True)
                n_files = len(zipped_folder.namelist())
        return n_files


def move_file(file_path, new_folder_path):
    """
    Move the file to the new folder

    Parameters
    ----------
    file_path : string or Path
        Original file path
    new_folder_path : string or Path
        New folder destination (without the file name)
    """
    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)
    if not isinstance(new_folder_path, pathlib.Path):
        new_folder_path = pathlib.Path(new_folder_path)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    new_path = new_folder_path.joinpath(file_path.name)
    os.rename(file_path, new_path)
