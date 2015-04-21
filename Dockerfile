FROM progrium/busybox
MAINTAINER Alex Brandt <alunduil@alunduil.com>

RUN opkg-install bash bzip2
ADD https://raw.githubusercontent.com/elyase/docker/master/conda/3.4/conda_install.sh /root/conda_install.sh
RUN bash /root/conda_install.sh
ENV PATH /root/miniconda3/bin:${PATH}

RUN useradd -c 'added by docker for muniments' -d / -r muniments

ENV CONFIGURATION_FILE_PATH /usr/local/src/muniments/conf/muniments.ini
ENV LOGGING_CONFIGURATION_FILE_PATH /usr/local/src/muniments/conf/logging.ini

EXPOSE 5000

RUN pip3 install -U pip
RUN pip3 install --compile -U crumbs tornado

ADD . /usr/local/src/muniments
RUN pip3 install --compile file:///usr/local/src/muniments#egg=muniments

USER muniments

ENTRYPOINT [ "/usr/local/bin/muniments" ]
CMD []
