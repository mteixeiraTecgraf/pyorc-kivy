FROM python:3.10

 RUN apt-get update && \
        apt-get install -y gcc ffmpeg libsm6 libxext6 openjdk-18-jdk-headless unzip autoconf libtool
##     apt-get install -y software-properties-common && \
##     add-apt-repository ppa:kivy-team/kivy 
    ## How to no prompt

#apt-get install ffmpeg libsm6 libxext6  -

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