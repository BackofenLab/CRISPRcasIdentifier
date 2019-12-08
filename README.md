## CRISPRcasIdentifier

CRISPRcasIdentifier is an effective machine learning approach for the identification and classification of CRISPR-Cas proteins. It consists of a holistic strategy which allows us to: (i) combine regression and classification approaches for improving the quality of the input protein cassettes and predicting their subtypes with high accuracy; (ii) to detect signature genes for the different subtypes; (iii) to extract several types of information for each protein, such as potential rules that reveal the identity of neighboring genes; and (iv) define a complete and extensible framework able to integrate newly discovered Cas proteins and CRISPR subtypes. We achieve balanced accuracy scores above 0.96 in the classification experiment of CRISPR subtypes, mean absolute error values below 0.05 for the prediction of the normalized bit-score of different Cas proteins and a balanced accuracy of 0.88 in our benchmarking agains other available tools.

### Requirements

CRISPRcasIdentifier has been tested with Python 3.5.2. For library requirements, see requirements.txt. We recommend installing the same versions listed in such a file. Since we exported our classifiers using joblib.dump, it is not guaranteed that they will work properly if loaded using other Python and libraries versions. For such, we recommend the use of virtual environments, which make it easy to install the correct Python and library dependencies without affecting the whole operating system (see below).

The easiest way to install the correct python version and its dependencies to run CRISPRcasIdentifier is by using pyenv (https://github.com/pyenv/pyenv-virtualenv).

Install pyenv

```
curl https://pyenv.run | bash
```

Add the following to ~/.bashrc

```
export PATH="/home/$USER/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Install python 3.5.2 using pyenv, create virtual environment, activate environment

```
pyenv install -v 3.5.2
pyenv virtualenv 3.5.2 crispr-cas-identifier_env
pyenv activate crispr-cas-identifier_env
```

Install library dependencies

```
pip install -r requirements.txt
```

### How to use

To list the available command line arguments type

    python CRISPRcasIdentifier.py -h

The available options are:

* `-h` : displays the help message.

* `-f path/to/fasta_file.fa` : input fasta file path (it can be either protein or DNA).

* `-r reg1 reg2 ...` : list of regressors to use (default: ERT).

* `-c clf1 clf2 ...` : list of classifiers to use (default: ERT).

* `-p` : returns class probabilities. When the probability output is not required, the ML models always return the label with the maximum probability value (independent of how high the value of this probability is). When using the `-p` option, we want CRISPRcasIdentifier to give some clues to the user about how well a test cassette agrees with different subtypes (given that some subtypes have some Cas proteins in common). If the user wants to label a test example based on the probabilities, that must be done by assigning it to the subtype with the maximum probability value returned and not by using some threshold. Finally, for a given test example, the probabilities sum up to one.

* `-s HMM1 HMM2 ...` : list of HMM models to use, from HMM1 to HMM5 (default: HMM1 HMM3 HMM5).

* `-hp` : hmmsearch binary path (default: `./software/hmmer/hmmsearch`).

* `-ho` : hmmsearch output directory (default: `./hmmsearch_output`).

* `-co` : cassette output directory (default: `./cassette`).

* `-st` : sequence type contained in input fasta file, either `protein` or `dna` (default: `protein`). If `-st` is set to `protein`, CRISPRcasIdentifier assumes that the input fasta file contains only one cassette. For such, the expected cassette length is up to 15 proteins (more than that might produce unexpected results). If `-st` is set to `dna`, CRISPRcasIdentifier tries to build the protein cassettes after extracting the protein sequences using the Prodigal software. In this case, it CRISPRcasIdentifier may produce predictions for multiple cassettes. Also note that for DNA data, the option `-sc` must also be set.

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

    CRISPRCasIdentifier
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