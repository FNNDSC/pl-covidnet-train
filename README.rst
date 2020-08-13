pl-covidnet-train
================================

.. image:: https://badge.fury.io/py/covidnet_train.svg
    :target: https://badge.fury.io/py/covidnet_train

.. image:: https://travis-ci.org/FNNDSC/covidnet_train.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/covidnet_train

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-covidnet_train

.. contents:: Table of Contents


Abstract
--------

This plugin runs a COVID-NET training session.


Synopsis
--------

.. code::

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

Description
-----------

``covidnet_train.py`` is a ChRIS plugin for COVID-Net, a neural network for identifying COVID-19 using chest X-ray images. This plugin runs the COVID-Net training process.

For more detailed information about COVID-Net, refer the github repo: https://github.com/lindawangg/COVID-Net.

Arguments
---------

.. code::

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


Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install covidnet_train

and run with

.. code:: bash

    covidnet_train.py --man /tmp /tmp

to get inline help. The app should also understand being called with only two positional arguments

.. code:: bash

    covidnet_train.py /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

To build the docker image:

.. code:: bash

    docker build -t local/pl-cn-train .

Now, prefix all calls with 

.. code:: bash

    docker run --rm -it -v /root/pl-covidnet-generate-dataset/out/:/incoming \
    -v $(pwd)/out:/outgoing local/pl-cn-train covidnet_train.py --trainfile \
    train_split_v3.txt --datadir /incoming/data /incoming /outgoing

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-covidnet_train covidnet_train.py                  \
            --man                                                       \
            /incoming /outgoing
    

Examples
--------

.. code:: bash

    docker build -t local/pl-cn-train .
    
    docker run --rm -it -v /root/pl-covidnet-generate-dataset/out/:/incoming \
    -v $(pwd)/out:/outgoing local/pl-cn-train covidnet_train.py --trainfile \
    train_split_v3.txt --datadir /incoming/data /incoming /outgoing


Combined run with pl-covidnet-generate-dataset and pl-covidnet-train
================================

The covidnet-train plugin relies on the output from the covidnet-generate-dataset plugin.

This part explains the complete workflow to run the two steps:

1) Run the pl-covidnet-generate-dataset plugin, which automatically retrieve the datasets 
(currently five datasets are needed), and combine the datasets into a single dataset called 
the COVIDx dataset. The detailed description of the COVIDx dataset can be found here:
https://github.com/lindawangg/COVID-Net/blob/master/docs/COVIDx.md

2) Run the pl-covidnet-train plugin, which uses the COVIDx dataset as input, and run the 
actual COVID-Net training process.

Prerequisites
--------
First, make sure to have docker installed on your computer. Install docker if needed.
For example, for Ubuntu:
.. code:: bash
    sudo apt-get install docker.io


1. Run the pl-covidnet-generate-dataset plugin
--------

.. code:: bash
    
    git clone https://github.com/grace335/pl-covidnet-generate-dataset.git
    
    cd pl-covidnet-generate-dataset/
    
    docker pull grace335/pl-covidnet-generate-dataset
    
    docker run --rm -it -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing grace335/pl-covidnet-generate-dataset covidnet_generate_dataset.py --mode covidx /incoming /outgoing
    
Now the plugin should start to run. A sample output will be like:

2. Run the pl-covidnet-train plugin
--------

.. code:: bash
    
    git clone https://github.com/grace335/pl-covidnet-train.git
    
    cd pl-covidnet-generate-dataset/
    
    docker pull grace335/pl-covidnet-train
    
    docker run --rm -it -v [PATH_TO_OUTPUT_OF_STEP_1]:/incoming -v $(pwd)/out:/outgoing local/pl-cn-train covidnet_train.py /incoming /outgoing
    # Example:
    docker run --rm -it -v /root/pl-covidnet-generate-dataset/out/:/incoming -v $(pwd)/out:/outgoing local/pl-cn-train covidnet_train.py /incoming /outgoing
