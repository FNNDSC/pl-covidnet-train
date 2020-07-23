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

run a COVID-NET training session


Synopsis
--------

.. code::

    python covidnet_train.py                                           \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>
        <outputDir> 

Description
-----------

``covidnet_train.py`` is a ChRIS plugin for COVID-Net, a neural network for identifying COVID-19 using chest X-ray images. This plugin runs the COVID-Net training process.

For more detailed information about COVID-Net, refer the github repo [here](https://github.com/lindawangg/COVID-Net).

Agruments
---------

.. code::

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number. 
    
    [--man]
    If specified, print (this) man page.

    [--meta]
    If specified, print plugin meta data.
    
    [--mode]
    Required flag, specify which mode to run.


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

    docker run --rm -it -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing \
    local/pl-cn-covidx covidnet_train.py --mode covidx \
    /incoming /outgoing

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

    docker build -t local/pl-cn-covidx .
    
    docker run --rm -it -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing \
    local/pl-cn-covidx covidnet_train.py --mode covidx \
    /incoming /outgoing


