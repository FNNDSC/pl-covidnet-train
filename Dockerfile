# Docker file for covidnet_train ChRIS plugin app
# 
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-covidnet-train .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-covidnet-train .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-covidnet-train
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-covidnet-train
#


FROM fnndsc/ubuntu-python3:18.04
#FROM grace335/ubuntu18.04-python3
MAINTAINER fnndsc "dev@babymri.org"

ENV APPROOT="/usr/src/covidnet_train"
COPY ["covidnet_train", "${APPROOT}"]
COPY ["requirements.txt", "${APPROOT}"]

WORKDIR $APPROOT

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y keyboard-configuration \
  && apt-get install -y wget git nvidia-361-dev \
  && pip install setuptools --upgrade \
  && pip3 install --upgrade pip \
  && pip install lxml requests bs4 pillow xlrd pydicom pandas wheel opencv-python==4.2.0.34 numpy matplotlib \
  && pip install -U scikit-learn \
  && apt-get install -y libsm6 libxext6 libxrender-dev libglib2.0-0 \
  && mkdir -p /usr/local/cuda/lib \
  && cp /usr/lib/x86_64-linux-gnu/libcuda.so.1 /usr/local/cuda/lib/ \
  && git clone https://github.com/lindawangg/COVID-Net.git COVIDNet \
  && wget https://raw.githubusercontent.com/grace335/pl-covidnet-train/master/create_COVIDx_v3.py -P ./COVIDNet/

RUN pip3 install -r requirements.txt

CMD ["covidnet_train.py", "--help"]
