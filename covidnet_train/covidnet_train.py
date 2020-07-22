#!/usr/bin/env python                                            
#
# covidnet_train ds ChRIS plugin app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from chrisapp.base import ChrisApp
import subprocess
from bs4 import BeautifulSoup
import requests, urllib
from urllib.request import urlopen
from urllib.parse import urlparse
import tarfile
import create_COVIDx_v3

Gstr_title = """

                _     _            _    _             _        
               (_)   | |          | |  | |           (_)       
  ___ _____   ___  __| |_ __   ___| |_ | |_ _ __ __ _ _ _ __   
 / __/ _ \ \ / / |/ _` | '_ \ / _ \ __|| __| '__/ _` | | '_ \  
| (_| (_) \ V /| | (_| | | | |  __/ |_ | |_| | | (_| | | | | | 
 \___\___/ \_/ |_|\__,_|_| |_|\___|\__| \__|_|  \__,_|_|_| |_| 


"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       covidnet_train.py 

    SYNOPSIS

        python covidnet_train.py                                         \\
            [-h] [--help]                                               \\
            [--man]                                                     \\
            [--mode <MODE>]                                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python covidnet_train.py   \\
                                in    out

    DESCRIPTION

        `covidnet_train.py` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--mode <MODE>] 
        If specify the mode to . 
        
        [--version]
        If specified, print version number and exit. 

"""


class Covidnet_train(ChrisApp):
    """
    run a COVID-NET training session.
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A ChRIS plugin to run a COVID-NET training session'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'run a COVID-NET training session'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '0.1'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def download_data(self, url, dest_dir):
        links = []
        html = urlopen(url).read()
        html_page = BeautifulSoup(html, features="lxml")
        og_url = html_page.find("meta",  property = "og:url")
        base = urlparse(url)
        print("base",base)
        for link in html_page.find_all('a'):
            current_link = link.get('href')
            print(current_link)
            if current_link.endswith('.tar.gz'):
                if og_url:
                    print("currentLink",current_link)
                    links.append(og_url["content"] + current_link)
                else:
                    links.append(base.scheme + "://" + base.netloc + current_link)

        for link in links:
            os.system('wget ' + link + ' -P ' + dest_dir)

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--mode', dest='mode', type=str,
                          optional=False, help='running mode')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        if options.mode == "covidx":
            covidnet_dir = os.path.join(os.getcwd(), "COVID-Net") 
            data_url = "http://fnndsc.childrens.harvard.edu/COVID-Net/data/"
            input_data_dir = os.path.join(options.inputdir, "data")
            if not os.path.exists(input_data_dir):
                os.mkdir(input_data_dir)
            self.download_data(data_url, input_data_dir)

            for path, directories, files in os.walk(input_data_dir):
                for f in files:
                    if f.endswith(".tar.gz"):
                        print("Extracting dataset: " + f)
                        tar = tarfile.open(os.path.join(path,f), 'r:gz')
                        tar.extractall(path=path)
                        tar.close()
                        print("Extracting finished.")

            print("Calling create_COVIDx.py")
            os.chdir(covidnet_dir)
            create_COVIDx_v3.create_covidx()
            #os.system('python create_COVIDx_v3.py')

        # WIP for this part.
        #if options.mode == "train":
        #    print("Start COVID Net training.")


    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Covidnet_train()
    chris_app.launch()
