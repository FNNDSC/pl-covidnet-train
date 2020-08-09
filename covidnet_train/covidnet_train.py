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
            [--epochs <epochs>]                                         \\
            [--lr <LearningRate>]                                       \\
            [--bs <BatchSize>]                                          \\
            [--weightspath <PathToOutputFolder>]                        \\
            [--metaname <CkptMetaFile>]                                 \\
            [--ckptname <NameOfModelCkpts>]                             \\
            [--trainfile <NameOfTrainFile>]                             \\
            [--testfile <NameOfTestFile>]                               \\
            [--name <FolderNameForTrainingCheckpoints>]                 \\
            [--datadir <InputDataFolder>]                               \\
            [--covid_weight <ClassWeightingForCovid>]                   \\
            [--covid_percent <PercentageOfCovidSamples>]                \\
            [--input_size <SizeOfInput>]                                \\
            [--top_percent <PercentTopCrop>]                            \\
            [--in_tensorname <InputTensorToGraph>]                      \\
            [--out_tensorname <OutputTensorFromGraph>]                  \\
            [--logit_tensorname <LogitTensorForLoss>]                   \\
            [--label_tensorname <LabelTensorForLoss>]                   \\
            [--weights_tensorname <SampleWeightsTensorForLoss>]         \\
            [--model_url <UrlForPreTrainedModels>]                      \\
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

        [--epochs <epochs>]
        Number of epochs.
        
        [--lr <LearningRate>]
        Learning rate.
            
        [--bs <BatchSize>]
        Batch size.
        
        [--weightspath <PathToOutputFolder>]
        Path to output folder.
        
        [--metaname <CkptMetaFile>]
        Name of ckpt meta file.
        
        [--ckptname <NameOfModelCkpts>]
        Name of model ckpts.
        
        [--trainfile <NameOfTrainFile>]
        Name of train file.
        
        [--testfile <NameOfTestFile>]
        Name of test file.
        
        [--name <FolderNameForTrainingCheckpoints>]
        Name of folder to store training checkpoints.
        
        [--datadir <InputDataFolder>]
        Path to input data folder.
        
        [--covid_weight <ClassWeightingForCovid>]
        Class weighting for covid.
        
        [--covid_percent <PercentageOfCovidSamples>]
        Percentage of covid samples in batch.
        
        [--input_size <SizeOfInput>]
        Size of input (ex: if 480x480, --input_size 480).
        
        [--top_percent <PercentTopCrop>]
        Percent top crop from top of image.
        
        [--in_tensorname <InputTensorToGraph>]
        Name of input tensor to graph.
        
        [--out_tensorname <OutputTensorFromGraph>]
        Name of output tensor from graph.
        
        [--logit_tensorname <LogitTensorForLoss>]
        Name of logit tensor for loss.
        
        [--label_tensorname <LabelTensorForLoss>]
        Name of label tensor for loss.
        
        [--weights_tensorname <SampleWeightsTensorForLoss>]
        Name of sample weights tensor for loss.
        
        [--model_url <UrlForPreTrainedModels>]
        Url to download pre-trained COVID-Net model.
        
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
        """
        Download data from url and save in destination dir (dest_dir).
        """
        links = []
        html = urlopen(url).read()
        # Use beautifulsoup to parse the html page, and extract names and URLs from 
        # the HTML page
        html_page = BeautifulSoup(html, features="lxml")
        og_url = html_page.find("meta",  property = "og:url")
        base = urlparse(url)
        #print("base",base)
        
        # Find and save .tar.gz files in links list
        for link in html_page.find_all('a'):
            current_link = link.get('href')
            print(current_link)
            if current_link.endswith('.tar.gz'):
                if og_url:
                    print("currentLink",current_link)
                    links.append(og_url["content"] + current_link)
                else:
                    links.append(base.scheme + "://" + base.netloc + current_link)

        # Use wget to download url links in the links list.
        # Files saved in destination dir
        for link in links:
            os.system('wget ' + link + ' -P ' + dest_dir)

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--epochs', 
                          dest      = 'epochs', 
                          type      = int,
                          optional  = True, 
                          help      = 'Number of epochs',
                          default   = 10)

        self.add_argument('--lr',
                          dest      = 'lr',
                          type      = float,
                          optional  = True,
                          help      = 'Learning rate',
                          default   = 0.0002)

        self.add_argument('--bs',
                          dest      = 'bs',
                          type      = int,
                          optional  = True,
                          help      = 'Batch size',
                          default   = '8')

        self.add_argument('--weightspath',
                          dest      = 'weightspath',
                          type      = str,
                          optional  = True,
                          help      = 'Path to output folder',
                          default   = '/incoming/models/COVIDNet-CXR3-B')

        self.add_argument('--metaname',
                          dest      = 'metaname',
                          type      = str,
                          optional  = True,
                          help      = 'Name of ckpt meta file',
                          default   = 'model.meta')

        self.add_argument('--ckptname',
                          dest      = 'ckptname',
                          type      = str,
                          optional  = True,
                          help      = 'Name of model ckpts',
                          default   = 'model-1014')

        self.add_argument('--trainfile',
                          dest      = 'trainfile',
                          type      = str,
                          optional  = True,
                          help      = 'Name of train file',
                          default   = 'train_split_v3.txt')

        self.add_argument('--testfile',
                          dest      = 'testfile',
                          type      = str,
                          optional  = True,
                          help      = 'Name of test file',
                          default   = 'test_COVIDx3.txt')

        self.add_argument('--name',
                          dest      = 'name',
                          type      = str,
                          optional  = True,
                          help      = 'Name of folder to store training checkpoints',
                          default   = 'COVIDNet')

        self.add_argument('--datadir',
                          dest      = 'datadir',
                          type      = str,
                          optional  = True,
                          help      = 'Path to input data folder',
                          default   = '/incoming/data')

        self.add_argument('--covid_weight',
                          dest      = 'covid_weight',
                          type      = float,
                          optional  = True,
                          help      = 'Class weighting for covid',
                          default   = 4)

        self.add_argument('--covid_percent',
                          dest      = 'covid_percent',
                          type      = float,
                          optional  = True,
                          help      = 'Percentage of covid samples in batch',
                          default   = 0.3)

        self.add_argument('--input_size',
                          dest      = 'input_size',
                          type      = int,
                          optional  = True,
                          help      = 'Size of input (ex: if 480x480, --input_size 480)',
                          default   = 480)

        self.add_argument('--top_percent',
                          dest      = 'top_percent',
                          type      = float,
                          optional  = True,
                          help      = 'Percent top crop from top of image',
                          default   = 0.08)

        self.add_argument('--in_tensorname',
                          dest      = 'in_tensorname',
                          type      = str,
                          optional  = True,
                          help      = 'Name of input tensor to graph',
                          default   = 'input_1:0')

        self.add_argument('--out_tensorname',
                          dest      = 'out_tensorname',
                          type      = str,
                          optional  = True,
                          help      = 'Name of output tensor from graph',
                          default   = 'norm_dense_1/Softmax:0')

        self.add_argument('--logit_tensorname',
                          dest      = 'logit_tensorname',
                          type      = str,
                          optional  = True,
                          help      = 'Name of logit tensor for loss',
                          default   = 'norm_dense_1/MatMul:0')

        self.add_argument('--label_tensorname',
                          dest      = 'label_tensorname',
                          type      = str,
                          optional  = True,
                          help      = 'Name of label tensor for loss',
                          default   = 'norm_dense_1_target:0')

        self.add_argument('--weights_tensorname',
                          dest      = 'weights_tensorname',
                          type      = str,
                          optional  = True,
                          help      = 'Name of sample weights tensor for loss',
                          default   = 'norm_dense_1_sample_weights:0')

        self.add_argument('--model_url',
                          dest      = 'model_url',
                          type      = str,
                          optional  = True,
                          help      = 'Url to download pre-trained COVID-Net model',
                          default   = 'http://fnndsc.childrens.harvard.edu/COVID-Net/models/')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        # dirs: 
        # covid_net_dir: /usr/src/covidnet_train/COVIDNet
        # input_data_dir: /incoming/data
        # input_model_dir: /incoming/models
        covidnet_dir = os.path.join(os.getcwd(), "COVIDNet") 
        input_data_dir = os.path.join(options.inputdir, "data")
        output_data_dir = os.path.join(options.outputdir, "output")
        model_url = options.model_url
        input_model_dir = os.path.join(options.inputdir, "models")

        # create input model directory (/incoming/models) if not exist
        if not os.path.exists(input_model_dir):
            os.mkdir(input_model_dir)
        self.download_data(model_url, input_model_dir)

        # extract tarballs to their current dir
        for path, directories, files in os.walk(input_model_dir):
            for f in files:
                if f.endswith(".tar.gz"):
                    print("Extracting models: " + f)
                    tar = tarfile.open(os.path.join(path,f), 'r:gz')
                    tar.extractall(path=path)
                    tar.close()
                    print("Extracting finished.")


        print("Calling covid-net training.")
        os.chdir(covidnet_dir)
        # import and run train_tf 
        import train_tf
        train_tf.train_tf(options.epochs, options.lr, options.bs, options.weightspath, 
                options.metaname, options.ckptname, options.trainfile, options.testfile, options.name, 
                options.datadir, options.covid_weight, options.covid_percent, options.input_size, 
                options.top_percent, options.in_tensorname, options.out_tensorname, 
                options.logit_tensorname, options.label_tensorname, options.weights_tensorname,
                input_data_dir, output_data_dir)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Covidnet_train()
    chris_app.launch()
