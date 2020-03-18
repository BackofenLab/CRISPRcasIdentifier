## CRISPRcasIdentifier

CRISPRcasIdentifier is an effective machine learning approach for the identification and classification of CRISPR-Cas proteins. It consists of a holistic strategy which allows us to: (i) combine regression and classification approaches for improving the quality of the input protein cassettes and predicting their subtypes with high accuracy; (ii) to detect signature genes for the different subtypes; (iii) to extract several types of information for each protein, such as potential rules that reveal the identity of neighboring genes; and (iv) define a complete and extensible framework able to integrate newly discovered Cas proteins and CRISPR subtypes. We achieve balanced accuracy scores above 0.96 in the classification experiment of CRISPR subtypes, mean absolute error values below 0.05 for the prediction of the normalized bit-score of different Cas proteins and a balanced accuracy of 0.88 in our benchmarking against other available tools.

### Requirements

CRISPRcasIdentifier has been tested with Python 3.7.6. To run it, we recommend installing the same library versions we used. Since we exported our classifiers using joblib.dump, it is not guaranteed that they will work properly if loaded using other Python and libraries versions. For such, we recommend the use of conda virtual environments, which make it easy to install the correct Python and library dependencies without affecting the whole operating system (see below).

### Setting up a virtual environment

The easiest way to install the correct python version and its dependencies to run CRISPRcasIdentifier is by using [miniconda](https://docs.conda.io/en/latest/miniconda.html).

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

### Downloading the Machine Learning (ML) models

Due to GitHub's file size constraints, we made the ML models available in Google Drive. You can download and extract them by using the following commands (save and extract them in CRISPRcasIdentifier's folder).

```
wget https://drive.google.com/file/d/1ZOR1e-wIb_rxtCiU3OaBVdrHrup1svq3/view?usp=sharing
tar -xzf trained_models_2015.tar.gz
```

### How to use

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

* `-o` : output csv file path (default: `CrisprCasIdentifier_output.csv`).

### Examples

We provide three simple examples in the `examples` folder:

* `NC_013722.fasta` : DNA example. That must be run as `python CRISPRcasIdentifier.py -f examples/NC_013722.fasta -st dna -sc complete`

* `example1.fa` and `example2.fa` : Protein examples. Those must be run as:
    * `python CRISPRcasIdentifier.py -f examples/example1.fasta`
    * `python CRISPRcasIdentifier.py -f examples/example2.fasta`

### License (GPLv3)

    CRISPRcasIdentifier
    Copyright (C) 2019 Victor Alexandre Padilha <victorpadilha@usp.br>,
                       Omer Salem Alkhnbashi <alkhanbo@informatik.uni-freiburg.de>

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