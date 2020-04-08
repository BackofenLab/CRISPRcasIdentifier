FROM ubuntu:18.04

SHELL ["/bin/bash", "-c"]

RUN mkdir /home/CRISPRcasIdentifier
WORKDIR /home/CRISPRcasIdentifier
COPY *.py ./
COPY crispr-env.yml ./
COPY README.md ./
COPY HMM_sets.tar.gz ./
COPY trained_models_2015.tar.gz ./
ADD examples ./examples
ADD software ./software

RUN apt-get update
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH /root/miniconda3/bin:$PATH

RUN conda env create -f crispr-env.yml -n crispr-env
RUN echo "source ~/miniconda3/etc/profile.d/conda.sh && conda activate crispr-env" >> ~/.bashrc
