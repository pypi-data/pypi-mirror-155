import pandas as pd
import pkg_resources
from subprocess import call
from datetime import datetime

def csv_to_utf8(file):
    """Converts a csv file to utf-8 encoding

    Parameters
    ----------
    file: String
        Path to file to be encoded 

    Returns
    -------
    fName:
        String of path to reformatted file
    """
    df = pd.read_csv(
        file,
        encoding = 'latin'
    )

    fName = file[:-4] + '-reformatted.csv'

    df.to_csv(
        fName,
        index=False
    )

    print(f'{fName} created')

    return fName

def upgradeAllPackages():
    packages = [dist.project_name for dist in pkg_resources.working_set]

    packages_to_ignore = [
        'pycurl',
        'pywin32'
    ]

    for p in packages_to_ignore:
        if (p in packages):
            packages.remove(p)
            print(f'Skipping {p}')

    call("pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade " + ' '.join(packages), shell=True)

def installPackage(package):
    try:
        call(f"pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org {package}", shell=True)
        print(f'{package} successfully installed')
    except Exception as e:
        print("Error - {}".format(e))

def getDateTimeStamp(time=True):
    """Function to generate a Date/Time stamp for the current time

    Parameters
    ----------
    time: Boolean
        Set to True to include time in Date stamp. False returns just date. Defaults to True.

    Returns
    -------
    stamp:
        String of date-time stamp
    """
    now = datetime.now()
    stamp = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2)
    if time:
        stamp = stamp + "_" + str(now.hour).zfill(2) + str(now.minute).zfill(2)
    return stamp

def continuous_logging(msg):
    """Function to print out messages that over-write each other as a new message is sent

    Parameters
    ----------
    msg: String
        the message to be printed to the console

    Returns
    -------
    None
    """

    print(f'\r{msg}\r', end='', flush=True)

    return None
