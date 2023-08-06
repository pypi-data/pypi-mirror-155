import matplotlib.pyplot as plt
import xarray
import seaborn as sns

plt.rcParams.update({'text.usetex': True})
sns.set_theme('paper')
sns.set_style('ticks')
sns.set_palette('colorblind')


def plot_spd(spd, db, p_ref, log=True, save_path=None):
    """
    Plot the the SPD graph of the bin

    Parameters
    ----------
    spd : xarray DataArray
        Data array with 2D data frequency-sound_pressure
    db : boolean
        If set to True the result will be given in db. Otherwise in upa^2/Hz
    p_ref : Float
        Reference pressure in upa
    log : boolean
        If set to True the scale of the y axis is set to logarithmic
    save_path : string or Path
        Where to save the images
    """
    if db:
        units = r'dB %s $\mu Pa^2/Hz$' % p_ref
    else:
        units = r'$\mu Pa^2/Hz$'
    # Plot the EPD
    fig, ax = plt.subplots()
    plot_2d(spd['spd'], x='frequency', y='spl', cmap='CMRmap_r', cbar_label='Empirical Probability Density', ax=ax,
            ylabel='PSD [%s]' % units, xlabel='Frequency [Hz]', title='Spectral Probability Density (SPD)')
    ax.plot(spd['value_percentiles'].frequency, spd['value_percentiles'],
            label=spd['value_percentiles'].percentiles.values)
    if log:
        plt.xscale('log')

    plt.legend(loc='upper right')
    plt.show()
    if save_path is not None:
        plt.savefig(save_path)
    plt.close()


def plot_spectrograms(ds_spectrogram, log, db, p_ref=1.0, save_path=None):
    """
    Plot the the SPD graph of the bin

    Parameters
    ----------
    ds_spectrogram : xarray DataArray
        Data array with 3D data (datetime, frequency and time_bin as dimensions)
    db : boolean
        If set to True the result will be given in db. Otherwise in upa^2/Hz
    p_ref : Float
        Reference pressure in upa
    log : boolean
        If set to True the scale of the y axis is set to logarithmic
    save_path : string or Path
        Where to save the images
    """
    if db:
        units = r'dB ' + str(p_ref) + r' $\mu Pa$'
    else:
        units = r'$\mu Pa$'

    for time_bin in ds_spectrogram.datetime:
        sxx = ds_spectrogram['spectrogram'].loc[time_bin]
        title = 'Spectrogram of bin %s' % time_bin.values
        if save_path is not None:
            save_path = save_path + time_bin.values
        # Plot the spectrogram
        plot_2d(ds=sxx, x='time', y='frequency', xlabel='Time [s]', ylabel='Frequency [Hz]',
                cbar_label=r'$L_{rms}$ [%s]' % units, ylog=log, title=title)
        plt.show()
        if save_path is not None:
            plt.savefig(save_path)
        plt.close()


def plot_spectrum(ds, col_name, ylabel, log=True, save_path=None):
    """
    Plot the spectrums contained on the dataset

    Parameters
    ----------
    ds : xarray Dataset
        Dataset resultant from psd or power spectrum calculation
    col_name : string
        Name of the column where the data is (scaling type) 'spectrum' or 'density'
    ylabel : string
        Label of the y axis (with units of the data)
    log : boolean
        If set to True the scale of the y axis is set to logarithmic
    save_path: string or Path
        Where to save the image
    """
    xscale = 'linear'
    if log:
        xscale = 'log'
    for time_bin in ds.datetime:
        ds[col_name].sel(datetime=time_bin).plot.line(xscale=xscale)
        title = '%s of bin %s' % (col_name.replace('_', ' ').capitalize(), time_bin.values)
        plt.title(title)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel(ylabel)

        # Plot the percentiles as horizontal lines
        plt.hlines(y=ds['value_percentiles'].loc[time_bin], xmin=ds.frequency.min(), xmax=ds.frequency.max(),
                   label=ds['percentiles'])

        plt.show()
        if save_path is not None:
            plt.savefig(save_path)
        plt.close()


def plot_spectrum_mean(ds, units, col_name, output_name, save_path=None, log=True):
    """
    Plot the mean spectrum

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
    log : boolean
        If set to True, y axis in logarithmic scale
    save_path : string or Path
        Where to save the output graph. If None, it is not saved
    """
    ds[col_name].mean(dim='datetime').plot.line(x='frequency')
    if len(ds['percentiles']) > 0:
        # Add the percentiles values
        ds['value_percentiles'].mean(dim='datetime').plot.line(hue='percentiles')

    plt.title(col_name.replace('_', ' ').capitalize())
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('%s [%s]' % (output_name, units))

    if log:
        plt.xscale('log')

    plt.show()
    if save_path is not None:
        plt.savefig(save_path)
    plt.close()


def plot_2d(ds, x, y, cbar_label, xlabel, ylabel, title, xlog=False, ylog=False, ax=None, **kwargs):
    xscale = 'linear'
    yscale = 'linear'
    if xlog:
        xscale = 'log'
    if ylog:
        yscale = 'log'
    if ax is None:
        _, ax = plt.subplots()
    xarray.plot.pcolormesh(ds, x=x, y=y, add_colorbar=True, xscale=xscale, yscale=yscale,
                           cbar_kwargs={'label': cbar_label}, robust=True, ax=ax,
                           extend='neither', cmap='YlGnBu_r', **kwargs)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

