FROM python:3.10

 RUN apt-get update && \
        apt-get install -y gcc ffmpeg libsm6 libxext6  unzip autoconf libtool libgeos-dev libmtdev-dev
        #openjdk-18-jdk-headless problema
        ## for cartopy 
##     apt-get install -y software-properties-common && \
##     add-apt-repository ppa:kivy-team/kivy 
    ## How to no prompt

#apt-get install ffmpeg libsm6 libxext6  -
#sudo apt -y install libgeos-dev #Cartopy
RUN apt-get install -y \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good

RUN groupadd -g 1000 lyonn
RUN useradd -d /home/lyonn -s /bin/bash -m lyonn -u 1000 -g 1000

USER lyonn
ENV HOME /home/lyonn
WORKDIR /src
VOLUME [ "/src" ]


RUN python3 -m pip install --upgrade pip setuptools virtualenv

USER root
COPY docker-entrypoint.sh /usr/local/bin/
#ENTRYPOINT ["docker-entrypoint.sh"]

USER lyonn
CMD ["bash"]
#CMD ["source","kivy_venv/bin/activate"]