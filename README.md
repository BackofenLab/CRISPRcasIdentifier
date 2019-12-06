## CRISPR-Cas-Identifier

It's an effective machine learning approach for the identification and classification of CRISPR-Cas proteins. A holistic strategy allows us to: (i) combine regression and classification approaches for improving the quality of the input protein cascades and predicting their subtypes with high accuracy; (ii) to detect signature genes for the different subtypes; (iii) to extract several types of information for each protein, such as potential rules that reveal the identity of neighboring genes; and (iv) define a complete and extensible framework able to integrate newly discovered Cas proteins and CRISPR subtypes. We achieve balanced accuracy scores above 0.96 in the classification experiment of CRISPR subtypes, mean absolute error values below 0.05 for the prediction of the normalized bit-score of different Cas proteins and a balanced accuracy of 0.94 for the best real scenario that uses the whole pipeline



### Requirements

CRISPR-Cas-Identifier has been tested with Python 3.5.2. For library requirements, see requirements.txt. We recommend installing the same versions listed in such a file. Since we exported our classifiers using joblib.dump, it is not guaranteed that they will work properly if loaded using other Python and libraries versions. For such, we recommend the use of virtual environments, which make it easy to install the correct Python and library dependencies without affecting the whole operating system, Please see next section.


### Prerequisites (optional)

First you need to install Miniconda
Then create an environment and install the required libraries in it


### Creating a Miniconda environment 

First we install Miniconda for python 3.
Miniconda can be downloaded from here:

https://docs.conda.io/en/latest/miniconda.html 

Then Miniconda should be installed. On a linux machine the command is similar to this one: 

```
bash Miniconda3-latest-Linux-x86_64.sh
```

Then we create an environment. The necessary setup is provided in the "environment.yml" file inside the "for_environment" directory

In order to install the corresponding environment one can execute the following command:

```
conda env create -f environment.yml
```

### Active the environment:

 - New conda version

  conda activate crispr-cas-identifier_evn

 - Old conda version

  source activate crispr-cas-identifier_evn

 

### How to use

    python CrisprCasIdentifier.py -f examples/example1.fa

Type

    python CrisprCasIdentifier.py -h

to see the available options.
