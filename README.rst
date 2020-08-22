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

To pull the docker image from dockerhub:

.. code:: bash

    docker pull grace335/pl-covidnet-train

Now, prefix all calls with 

.. code:: bash

    docker run --rm -it -v /root/pl-covidnet-generate-dataset/out/:/incoming \
    -v $(pwd)/out:/outgoing grace335/pl-covidnet-train covidnet_train.py /incoming /outgoing

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v /root/pl-covidnet-generate-dataset/out/:/incoming -v $(pwd)/out:/outgoing      \
            grace335/pl-covidnet-train covidnet_train.py                  \
            --man                                                       \
            /incoming /outgoing
    

Examples
--------

.. code:: bash

    docker pull grace335/pl-covidnet-train
    
    docker run --rm -it -v /root/pl-covidnet-generate-dataset/out/:/incoming \
    -v $(pwd)/out:/outgoing grace335/pl-covidnet-train covidnet_train.py /incoming /outgoing


Combined run with pl-covidnet-generate-dataset and pl-covidnet-train
================================

The covidnet-train plugin relies on the output from the covidnet-generate-dataset plugin. 

The two plugins have been tested on Ubuntu 18.04.

This part explains the complete workflow to run the two steps:

1) Run the pl-covidnet-generate-dataset plugin, which automatically retrieve the datasets 
(currently five datasets are needed), and combine the datasets into a single dataset called 
the COVIDx dataset. The detailed description of the COVIDx dataset can be found here:
https://github.com/lindawangg/COVID-Net/blob/master/docs/COVIDx.md

2) Run the pl-covidnet-train plugin, which uses the COVIDx dataset (output of previous step) 
as input, and run the COVID-Net training process.

The general workflow is like this:

::

                  ┌──────────────────────────────────┐  ┌─►/outputdir (COVIDx dataset)     ┌──────────────────────┐  
    /inputdir ───►│ covidnet-generate-dataset plugin ├──┘         |                    ┌──►│ covidnet-train plugin├───► /outputdir
                  └──────────────────────────────────┘        /inputdir────────────────┘   └──────────────────────┘     

Prerequisites
--------
First, make sure to have docker installed on your computer. Install docker if needed.
For example, for Ubuntu, run:

.. code:: bash

    sudo apt-get install docker.io


1. Run the pl-covidnet-generate-dataset plugin
--------

.. code:: bash
    
    # Create dir for pl-covidnet-generate-dataset
    mkdir pl-covidnet-generate-dataset
    
    # Enter dir for pl-covidnet-generate-dataset
    cd pl-covidnet-generate-dataset
    
    # Pull docker image
    docker pull grace335/pl-covidnet-generate-dataset
    
    # Run the generate dataset plugin
    docker run --rm -it -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing grace335/pl-covidnet-generate-dataset covidnet_generate_dataset.py --mode covidx /incoming /outgoing
    
Now the plugin should start to run. A sample output will be like this:

::

    ~/pl-covidnet-generate-dataset# docker run --rm -it -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing grace335/pl-covidnet-generate-dataset covidnet_generate_dataset.py --mode covidx /incoming /outgoing


     _____            _     _   _   _      _
    /  __ \          (_)   | | | \ | |    | |
    | /  \/ _____   ___  __| | |  \| | ___| |_
    | |    / _ \ \ / / |/ _` | | . ` |/ _ \ __|
    | \__/\ (_) \ V /| | (_| | | |\  |  __/ |_
     \____/\___/ \_/ |_|\__,_| \_| \_/\___|\__|


    Version: 0.1
    http://browsehappy.com
    https://larsjung.de/h5ai/
    ..
    /COVID-Net/data/Actualmed-COVID-chestxray-dataset.tar.gz
    /COVID-Net/data/COVID-19-Radiography-Database.tar.gz
    /COVID-Net/data/covid-chestxray-dataset.tar.gz
    /COVID-Net/data/Figure1-COVID-chestxray-dataset.tar.gz
    /COVID-Net/data/rsna-pneumonia-detection-challenge.tar.gz
    --2020-08-13 03:00:08--  http://fnndsc.childrens.harvard.edu/COVID-Net/data/Actualmed-COVID-chestxray-dataset.tar.gz
    Resolving fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)... 134.174.13.44
    Connecting to fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)|134.174.13.44|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 2821543234 (2.6G) [application/x-gzip]
    Saving to: '/incoming/data/Actualmed-COVID-chestxray-dataset.tar.gz'

    Actualmed-COVID-chestxray-dataset.tar.gz  100%[====================================================================================>]   2.63G  8.56MB/s    in 4m 27s   

    2020-08-13 03:04:35 (10.1 MB/s) - '/incoming/data/Actualmed-COVID-chestxray-dataset.tar.gz' saved [2821543234/2821543234]

    --2020-08-13 03:04:35--  http://fnndsc.childrens.harvard.edu/COVID-Net/data/COVID-19-Radiography-Database.tar.gz
    Resolving fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)... 134.174.13.44
    Connecting to fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)|134.174.13.44|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 1233053305 (1.1G) [application/x-gzip]
    Saving to: '/incoming/data/COVID-19-Radiography-Database.tar.gz'

    COVID-19-Radiography-Database.tar.gz      100%[====================================================================================>]   1.15G  13.4MB/s    in 88s     

    2020-08-13 03:06:03 (13.3 MB/s) - '/incoming/data/COVID-19-Radiography-Database.tar.gz' saved [1233053305/1233053305]

    --2020-08-13 03:06:03--  http://fnndsc.childrens.harvard.edu/COVID-Net/data/covid-chestxray-dataset.tar.gz
    Resolving fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)... 134.174.13.44
    Connecting to fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)|134.174.13.44|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 541464562 (516M) [application/x-gzip]
    Saving to: '/incoming/data/covid-chestxray-dataset.tar.gz'

    covid-chestxray-dataset.tar.gz            100%[====================================================================================>] 516.38M  14.0MB/s    in 41s     

    2020-08-13 03:06:44 (12.7 MB/s) - '/incoming/data/covid-chestxray-dataset.tar.gz' saved [541464562/541464562]

    --2020-08-13 03:06:44--  http://fnndsc.childrens.harvard.edu/COVID-Net/data/Figure1-COVID-chestxray-dataset.tar.gz
    Resolving fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)... 134.174.13.44
    Connecting to fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)|134.174.13.44|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 29629948 (28M) [application/x-gzip]
    Saving to: '/incoming/data/Figure1-COVID-chestxray-dataset.tar.gz'

    Figure1-COVID-chestxray-dataset.tar.gz    100%[====================================================================================>]  28.26M  11.2MB/s    in 2.5s    

    2020-08-13 03:06:47 (11.2 MB/s) - '/incoming/data/Figure1-COVID-chestxray-dataset.tar.gz' saved [29629948/29629948]

    --2020-08-13 03:06:47--  http://fnndsc.childrens.harvard.edu/COVID-Net/data/rsna-pneumonia-detection-challenge.tar.gz
    Resolving fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)... 134.174.13.44
    Connecting to fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)|134.174.13.44|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 3926236026 (3.7G) [application/x-gzip]
    Saving to: '/incoming/data/rsna-pneumonia-detection-challenge.tar.gz'

    rsna-pneumonia-detection-challenge.tar.gz 100%[====================================================================================>]   3.66G  8.30MB/s    in 6m 24s  

    2020-08-13 03:13:11 (9.74 MB/s) - '/incoming/data/rsna-pneumonia-detection-challenge.tar.gz' saved [3926236026/3926236026]

    Extracting dataset: Actualmed-COVID-chestxray-dataset.tar.gz
    Extracting finished.
    Extracting dataset: COVID-19-Radiography-Database.tar.gz
    Extracting finished.
    Extracting dataset: Figure1-COVID-chestxray-dataset.tar.gz
    Extracting finished.
    Extracting dataset: covid-chestxray-dataset.tar.gz
    Extracting finished.
    Extracting dataset: rsna-pneumonia-detection-challenge.tar.gz
    Extracting finished.
    Calling create_COVIDx.py
    Data distribution from covid datasets:
    {'normal': 0, 'pneumonia': 33, 'COVID-19': 390}
    Key:  pneumonia
    Test patients:  ['8', '31']
    Key:  COVID-19
    Test patients:  ['19', '20', '36', '42', '86', '94', '97', '117', '132', '138', '144', '150', '163', '169', '174', '175', '179', '190', '191COVID-00024', 'COVID-00025', 'COVID-00026', 'COVID-00027', 'COVID-00029', 'COVID-00030', 'COVID-00032', 'COVID-00033', 'COVID-00035', 'COVID-00036', 'COVID-00037', 'COVID-00038', 'ANON24', 'ANON45', 'ANON126', 'ANON106', 'ANON67', 'ANON153', 'ANON135', 'ANON44', 'ANON29', 'ANON201', 'ANON191', 'ANON234', 'ANON110', 'ANON112', 'ANON73', 'ANON220', 'ANON189', 'ANON30', 'ANON53', 'ANON46', 'ANON218', 'ANON240', 'ANON100', 'ANON237', 'ANON158', 'ANON174', 'ANON19', 'ANON195', 'COVID-19(119)', 'COVID-19(87)', 'COVID-19(70)', 'COVID-19(94)', 'COVID-19(215)', 'COVID-19(77)', 'COVID-19(213)', 'COVID-19(81)', 'COVID-19(216)', 'COVID-19(72)', 'COVID-19(106)', 'COVID-19(131)', 'COVID-19(107)', 'COVID-19(116)', 'COVID-19(95)', 'COVID-19(214)', 'COVID-19(129)']
    test count:  {'normal': 0, 'pneumonia': 5, 'COVID-19': 100}
    train count:  {'normal': 0, 'pneumonia': 28, 'COVID-19': 286}
    test count:  {'normal': 885, 'pneumonia': 594, 'COVID-19': 100}
    train count:  {'normal': 7966, 'pneumonia': 5451, 'COVID-19': 286}
    Final stats
    Train count:  {'normal': 7966, 'pneumonia': 5451, 'COVID-19': 286}
    Test count:  {'normal': 885, 'pneumonia': 594, 'COVID-19': 100}
    Total length of train:  13703
    Total length of test:  1579

2. Run the pl-covidnet-train plugin
--------

Once the pl-covidnet-generate-dataset plugin finishes, we can use its output to run the pl-covidnet-train plugin.

.. code:: bash
    
    # Create dir for pl-covidnet-generate-dataset
    mkdir ../pl-covidnet-train
    
    # Enter dir for pl-covidnet-generate-dataset
    cd ../pl-covidnet-train
    
    # Pull docker image
    docker pull grace335/pl-covidnet-train
    
    # Run the training plugin. Please make sure to replace [PATH_TO_OUTPUT_OF_STEP_1] with the absolute path of the output folder of step 1 (pl-covidnet-generate-dataset).
    docker run --rm -it -v [PATH_TO_OUTPUT_OF_STEP_1]:/incoming -v $(pwd)/out:/outgoing grace335/pl-covidnet-train covidnet_train.py /incoming /outgoing
    
    # For example, (if pl-covidnet-generate-dataset is located at /root/pl-covidnet-generate-dataset):
    docker run --rm -it -v /root/pl-covidnet-generate-dataset/out/:/incoming -v $(pwd)/out:/outgoing grace335/pl-covidnet-train covidnet_train.py /incoming /outgoing

Now the plugin should start to run. A sample output will be like this:

::

    ~/pl-covidnet-train# docker run --rm -it -v /root/pl-covidnet-generate-dataset/out/:/incoming -v $(pwd)/out:/outgoing grace335/pl-covidnet-train covidnet_train.py /incoming /outgoing


                    _     _            _    _             _        
                   (_)   | |          | |  | |           (_)       
      ___ _____   ___  __| |_ __   ___| |_ | |_ _ __ __ _ _ _ __   
     / __/ _ \ \ / / |/ _` | '_ \ / _ \ __|| __| '__/ _` | | '_ \  
    | (_| (_) \ V /| | (_| | | | |  __/ |_ | |_| | | (_| | | | | | 
     \___\___/ \_/ |_|\__,_|_| |_|\___|\__| \__|_|  \__,_|_|_| |_| 



    Version: 0.1
    http://browsehappy.com
    https://larsjung.de/h5ai/
    ..
    /COVID-Net/models/COVIDNet-CXR3-A.tar.gz
    /COVID-Net/models/COVIDNet-CXR3-B-20200513T223127Z-001.zip
    /COVID-Net/models/COVIDNet-CXR3-B.tar.gz
    /COVID-Net/models/COVIDNet-CXR3-C.tar.gz
    --2020-08-13 03:34:47--  http://fnndsc.childrens.harvard.edu/COVID-Net/models/COVIDNet-CXR3-A.tar.gz
    Resolving fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)... 134.174.13.44
    Connecting to fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)|134.174.13.44|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 556965802 (531M) [application/x-gzip]
    Saving to: '/incoming/models/COVIDNet-CXR3-A.tar.gz'

    COVIDNet-CXR3-A.tar.gz                    100%[====================================================================================>] 531.16M  10.8MB/s    in 64s     

    2020-08-13 03:35:52 (8.24 MB/s) - '/incoming/models/COVIDNet-CXR3-A.tar.gz' saved [556965802/556965802]

    --2020-08-13 03:35:52--  http://fnndsc.childrens.harvard.edu/COVID-Net/models/COVIDNet-CXR3-B.tar.gz
    Resolving fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)... 134.174.13.44
    Connecting to fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)|134.174.13.44|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 270551447 (258M) [application/x-gzip]
    Saving to: '/incoming/models/COVIDNet-CXR3-B.tar.gz'

    COVIDNet-CXR3-B.tar.gz                    100%[====================================================================================>] 258.02M  2.85MB/s    in 29s     

    2020-08-13 03:36:21 (8.77 MB/s) - '/incoming/models/COVIDNet-CXR3-B.tar.gz' saved [270551447/270551447]

    --2020-08-13 03:36:21--  http://fnndsc.childrens.harvard.edu/COVID-Net/models/COVIDNet-CXR3-C.tar.gz
    Resolving fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)... 134.174.13.44
    Connecting to fnndsc.childrens.harvard.edu (fnndsc.childrens.harvard.edu)|134.174.13.44|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 104027203 (99M) [application/x-gzip]
    Saving to: '/incoming/models/COVIDNet-CXR3-C.tar.gz'

    COVIDNet-CXR3-C.tar.gz                    100%[====================================================================================>]  99.21M   925KB/s    in 48s     

    2020-08-13 03:37:09 (2.08 MB/s) - '/incoming/models/COVIDNet-CXR3-C.tar.gz' saved [104027203/104027203]

    Extracting models: COVIDNet-CXR3-A.tar.gz
    Extracting finished.
    Extracting models: COVIDNet-CXR3-B.tar.gz
    Extracting finished.
    Extracting models: COVIDNet-CXR3-C.tar.gz
    Extracting finished.
    Calling covid-net training.
    Output: /outgoing/outputCOVIDNet-lr0.0002
    13417 286
    WARNING:tensorflow:From /usr/src/covidnet_train/COVIDNet/train_tf.py:40: The name tf.Session is deprecated. Please use tf.compat.v1.Session instead.

    2020-08-13 03:37:27.941128: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcuda.so.1
    2020-08-13 03:37:27.948528: E tensorflow/stream_executor/cuda/cuda_driver.cc:318] failed call to cuInit: CUDA_ERROR_UNKNOWN: unknown error
    2020-08-13 03:37:27.948579: I tensorflow/stream_executor/cuda/cuda_diagnostics.cc:156] kernel driver does not appear to be running on this host (27e759db9ca3): /proc/driver/nvidia/version does not exist
    2020-08-13 03:37:27.958068: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 1999995000 Hz
    2020-08-13 03:37:27.958650: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x59ef3b0 initialized for platform Host (this does not guarantee that XLA will be used). Devices:
    2020-08-13 03:37:27.958682: I tensorflow/compiler/xla/service/service.cc:176]   StreamExecutor device (0): Host, Default Version
    WARNING:tensorflow:From /usr/src/covidnet_train/COVIDNet/train_tf.py:41: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.

    WARNING:tensorflow:From /usr/src/covidnet_train/COVIDNet/train_tf.py:42: The name tf.train.import_meta_graph is deprecated. Please use tf.compat.v1.train.import_meta_graph instead.

    WARNING:tensorflow:From /usr/src/covidnet_train/COVIDNet/train_tf.py:55: The name tf.train.AdamOptimizer is deprecated. Please use tf.compat.v1.train.AdamOptimizer instead.

    WARNING:tensorflow:From /usr/src/covidnet_train/COVIDNet/train_tf.py:59: The name tf.global_variables_initializer is deprecated. Please use tf.compat.v1.global_variables_initializer instead.

    Saved baseline checkpoint
    Baseline eval:
    [[95.  5.  0.]
     [ 5. 94.  1.]
     [ 5.  4. 91.]]
    Sens Normal: 0.950, Pneumonia: 0.940, COVID-19: 0.910
    PPV Normal: 0.905, Pneumonia 0.913, COVID-19: 0.989
    Training started
    4/1678 [..............................] - ETA: 5:42:01 
