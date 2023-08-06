import pandas as pd
import numpy as np
import os
import iotools

"""
Tool for downloading SURFRAD data from a given site, and processing said files
into pandas DataFrame objects.

More work may be needed to create a similar format to other datafiles in other
parts of solartoolbox.

See the bottom of the file for an example of usage.
"""


URLROOT = 'https://gml.noaa.gov/aftp/data/radiation/surfrad/'


def download_surfrad(site, year, dir):
    """
    Retrieve a year's worth of files from SURFRAD

    Parameters
    ----------
    site: String
        the name of the surfrad site (e.g. 'psu')

    year : int
        The year of data to download (subdir of URL)

    dir :
        The output directory of where to save it

    Returns
    -------
    void
    """

    url = URLROOT + f'{site}/{year}/'

    iotools.ensurepath(dir)

    for i in np.arange(1, 366):
        try:
            short_year = str(year)[-2:]
            fn = 'psu{0}{1:03d}.dat'.format(short_year, i)
            iotools.download(url + fn, os.path.join(dir, fn))
        except Exception as e:
            print(e)


def read_surfrad(file):
    """
    Convert a surfrad datafile into a padas datafile for reading
    Parameters
    ----------
    file

    Returns
    -------
    DataFrame containing all fields from surfrad
    """
    surfrad_col_names = ['year', 'jday', 'month', 'day', 'hour', 'min', 'dt',
                         'zen', 'dw_solar', 'qc_dw_solar', 'uw_solar',
                         'qc_uw_solar', 'direct_n', 'qc_direct_n', 'diffuse',
                         'qc_diffuse', 'dw_ir', 'qc_dw_ir', 'dw_casetemp',
                         'qc_dw_casetemp', 'dw_dometemp', 'qc_dw_dometemp',
                         'uw_ir', 'qc_uw_ir', 'uw_casetemp', 'qc_uw_casetemp',
                         'uw_dometemp', 'qc_uw_dometemp', 'uvb', 'qc_uvb',
                         'par', 'qc_par', 'netsolar', 'qc_netsolar', 'netir',
                         'qc_netir', 'totalnet', 'qc_totalnet', 'temp',
                         'qc_temp', 'rh', 'qc_rh', 'windspd', 'qc_windspd',
                         'winddir', 'qc_winddir', 'pressure', 'qc_pressure']

    df = pd.read_csv(file, header=None, skiprows=2, names=surfrad_col_names,
                     delimiter='\s+')
    df.index = pd.to_datetime(df[['year', 'month', 'day', 'hour']]) + pd.to_timedelta(df['min'],'m')
    df.dt = np.arange(0,24,1/60)
    return df


if __name__ == "__main__":
    download_surfrad('psu', 2020, 'C:\\Users\\jar339\\Desktop\\SURFRAD')

    import matplotlib.pyplot as plt
    dat = read_surfrad('c:\\Users\\jar339\\Desktop\\SURFRAD\\psu20001.dat')
    plt.plot(dat['dw_solar'])
    plt.show()