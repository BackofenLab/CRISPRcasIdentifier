FROM ubuntu:18.04
LABEL maintainer="Victor A. Padilha <victorpadilha@usp.br>"
SHELL ["/bin/bash", "-c"]

# installing wget
RUN apt-get update
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN apt-get clean

# creating new user to increase container's security (for more info, see https://pythonspeed.com/articles/root-capabilities-docker-security/)
RUN useradd --create-home crispr
USER crispr
WORKDIR /home/crispr

# getting and installing miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH ~/miniconda3/bin:$PATH

# creating CRISPRcasIdentifier's env and making it active by default
# and removing additional unnecessary files (see https://jcristharif.com/conda-docker-tips.html)
ENV PYTHONDONTWRITEBYTECODE=true
COPY crispr-env.yml ./
RUN conda env create -f crispr-env.yml -n crispr-env
RUN conda clean --all --yes \
    && find ~/miniconda3/ -follow -type f -name '*.a' -delete \
    && find ~/miniconda3/ -follow -type f -name '*.pyc' -delete \
    && find ~/miniconda3/ -follow -type f -name '*.js.map' -delete
RUN rm crispr-env.yml
RUN echo "source ~/miniconda3/etc/profile.d/conda.sh && conda activate crispr-env" >> ~/.bashrc

# creating CRISPRcasIdentifier's folder and setting it as workdir
RUN mkdir CRISPRcasIdentifier
WORKDIR CRISPRcasIdentifier