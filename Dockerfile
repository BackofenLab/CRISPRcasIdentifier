# CRISPRCasIdentifier
# Copyright (C) 2020 Victor Alexandre Padilha <victorpadilha@usp.br>,
#                    Omer Salem Alkhnbashi <alkhanbo@informatik.uni-freiburg.de>,
#                    Shiraz Ali Shah <shiraz.shah@dbac.dk>,
#                    André Carlos Ponce de Leon Ferreira de Carvalho <andre@icmc.usp.br>,
#                    Rolf Backofen <backofen@informatik.uni-freiburg.de>

# This file is part of CRISPRcasIdentifier.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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