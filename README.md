# CRISPRcasIdentifier

CRISPRcasIdentifier is an effective machine learning approach for the identification and classification of CRISPR-Cas proteins. It consists of a holistic strategy which allows us to: (i) combine regression and classification approaches for improving the quality of the input protein cassettes and predicting their subtypes with high accuracy; (ii) to detect signature genes for the different subtypes; (iii) to extract several types of information for each protein, such as potential rules that reveal the identity of neighboring genes; and (iv) define a complete and extensible framework able to integrate newly discovered Cas proteins and CRISPR subtypes. We achieve balanced accuracy scores above 0.95 in the classification experiment of CRISPR subtypes, mean absolute error values below 0.05 for the prediction of the normalized bit-score of different Cas proteins and a balanced accuracy of 0.89 in our benchmarking against other available tools.

## Installation and requirements

CRISPRcasIdentifier has been tested with Python 3.7.6. To run it, we recommend installing the same library versions we used. Since we exported our classifiers using [joblib.dump](https://scikit-learn.org/stable/modules/model_persistence.html), it is not guaranteed that they will work properly if loaded using other Python and/or libraries versions. For such, we recommend the use of our ready-to-run docker image, to build the docker image from our Dockerfile or to set a conda virtual environment up. All options make it easy to install the correct Python and library dependencies without affecting the whole operating system (see below).

### If you prefer to use our ready-to-run DockerHub image

This is (probably) the easiest way to set CRISPRcasIdentifier up.

First, you need to install docker (please refer to its [installation guideline](https://docs.docker.com/get-docker/) for details).

#### Pulling and running

Pull our image from DockerHub

```
docker pull padilha/crispr-cas-identifier:0.0.1
```

Run the docker image in a new container

```
docker run -it padilha/crispr-cas-identifier:0.0.1 /bin/bash
```

#### Reusing a docker container

You can reuse the created container by using the following commands

```
docker restart CONTAINER_ID
docker exec -it CONTAINER_ID /bin/bash
```

You can obtain the CONTAINER_ID by using

```
docker ps --all
```

You can also copy a local fasta input file to CRISPRcasIdentifier's container by using

```
docker cp file.fa CONTAINER_ID:/home/CRISPRcasIdentifier
```

After this, everything should be set up and you can skip to [How to use](#how-to-use).

### If, for some reason, you do not want to use our DockerHub image

#### First step: clone this repository

```
git clone https://github.com/BackofenLab/CRISPRcasIdentifier.git
```

#### Second step: download the Hidden Markov (HMM) and Machine Learning (ML) models

Due to GitHub's file size constraints, we made our HMM and ML models available in Google Drive. You can download them [here](https://drive.google.com/file/d/166bh1sAjoB9kW5pn8YrEuEWrsM2QDV78/view?usp=sharing) and [here](https://drive.google.com/file/d/1ZOR1e-wIb_rxtCiU3OaBVdrHrup1svq3/view?usp=sharing). Save both tar.gz files inside CRISPRcasIdentifier's folder. It is not necessary to extract them, since the tool will do that the first time it is run.

Next, you can choose which third step to follow: either [building our docker image](#third-step-docker) or [setting up a conda environment](#third-step-conda).

#### Third step (docker)

First, you need to install docker (please refer to its [installation guideline](https://docs.docker.com/get-docker/) for details).

Build an image from the Dockerfile

```
cd CRISPRcasIdentifier
docker build -t crispr-cas-identifier .
```

Run the docker image in a new container

```
docker run -it crispr-cas-identifier:latest /bin/bash
```

To avoid creating multiple containers everytime you want to use CRISPRcasIdentifier, see [Reusing a docker container](#reusing-a-docker-container).

After this, everything should be set up and you can skip to [How to use](#how-to-use).

#### Third step (conda)

Another way to install the correct python version and its dependencies to run CRISPRcasIdentifier is by using [miniconda](https://docs.conda.io/en/latest/miniconda.html).

Install Miniconda

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
```

Create and activate environment for CRISPRcasIdentifier

```
conda env create -f crispr-env.yml -n crispr-env
conda activate crispr-env
```

After this, everything should be set up and you can skip to [How to use](#how-to-use).

## How to use

To list the available command line arguments type

    python CRISPRcasIdentifier.py -h

The available options are:

* `-h` : displays the help message.

* `-f path/to/fasta_file.fa` : input fasta file path (it can be either protein or DNA).

* `-r reg1 reg2 ...` : list of regressors to use (default: ERT).

* `-c clf1 clf2 ...` : list of classifiers to use (default: ERT).

* `-p` : returns class probabilities. When the probability output is not required, the ML models always return the label with the maximum probability value (independent of how high the value of this probability is). When using the `-p` option, we want CRISPRcasIdentifier to give some clues to the user about how well a test cassette agrees with different subtypes (given that some subtypes have some Cas proteins in common). _If the user wants to label a test example based on the probabilities, that must be done by assigning it to the subtype with the maximum probability value returned and not by using some threshold_. Finally, for a given test example, the probabilities sum up to one.

* `-s HMM1 HMM2 ...` : list of HMM models to use, from HMM1 to HMM5 (default: HMM3).

* `-hp` : hmmsearch binary path (default: `./software/hmmer/hmmsearch`).

* `-ho` : hmmsearch output directory (default: `./hmmsearch_output`).

* `-co` : cassette output directory (default: `./cassette`).

* `-st` : sequence type contained in input fasta file, either `protein` or `dna` (default: `protein`). If `-st` is set to `protein`, CRISPRcasIdentifier assumes that the input fasta file contains only one cassette. For such, the expected cassette length is up to 15 proteins (more than that might produce unexpected results). If `-st` is set to `dna`, CRISPRcasIdentifier tries to build the protein cassettes after extracting the protein sequences using the [Prodigal software](https://github.com/hyattpd/Prodigal) version 2.6.3 (unless the user is running our tool in a 32bit operating system, Prodigal is already included in the `software` folder and does not need to be installed by the user). In this case, CRISPRcasIdentifier may produce predictions for multiple cassettes. Also note that for DNA data, the option `-sc` _must_ also be set.

* `-sc` : sequence completeness, either `complete` or `partial` (used only when `-st` is set to `dna`).

* `-m` : run mode, either `classification`, or `regression` or `mixed`.

* `-o` : output csv file path (default: `CRISPRcasIdentifier_output.csv`).

## Examples

We provide three simple examples in the `examples` folder:

* `NC_013722.fasta` : DNA example. That must be run as `python CRISPRcasIdentifier.py -f examples/NC_013722.fasta -st dna -sc complete`

* `example1.fa` and `example2.fa` : Protein examples. Those must be run as:
    * `python CRISPRcasIdentifier.py -f examples/example1.fa`
    * `python CRISPRcasIdentifier.py -f examples/example2.fa`

## License (GPLv3)

    CRISPRcasIdentifier
    Copyright (C) 2019 Victor Alexandre Padilha <victorpadilha@usp.br>,
                       Omer Salem Alkhnbashi <alkhanbo@informatik.uni-freiburg.de>,
                       Shiraz Ali Shah <shiraz.shah@dbac.dk>,
                       André Carlos Ponce de Leon Ferreira de Carvalho <andre@icmc.usp.br>,
                       Rolf Backofen <backofen@informatik.uni-freiburg.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.