"""
    CRISPRcasIdentifier
    Copyright (C) 2019 Victor Alexandre Padilha <victorpadilha@usp.br>,
                       Omer Salem Alkhnbashi <alkhanbo@informatik.uni-freiburg.de>,
                       Shiraz Ali Shah <shiraz.shah@dbac.dk>,
                       André Carlos Ponce de Leon Ferreira de Carvalho <andre@icmc.usp.br>,
                       Rolf Backofen <backofen@informatik.uni-freiburg.de>

    This file is part of CRISPRcasIdentifier.

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
"""

import os, tarfile, glob
import subprocess as sp
import joblib
import numpy as np
import pandas as pd
import itertools

from collections import defaultdict

# Project imports
from prodigal import prodigal
from hmmsearch import hmmsearch
from cas import CAS_SYNONYM_LIST, CORE

SEQUENCE_TYPES = {'dna', 'protein'}
SEQUENCE_COMPLETENESS = {'complete', 'partial'}
RUN_MODES = {'classification', 'regression', 'mixed'}
REGRESSORS = {'CART' : 'DecisionTreeRegressor', 'ERT' : 'ExtraTreesRegressor', 'SVM' : 'SVR'}
CLASSIFIERS = {'CART' : 'DecisionTreeClassifier', 'ERT' : 'ExtraTreesClassifier', 'SVM' : 'SVC'}
CLASSIFIERS_INV = {v : k for k, v in CLASSIFIERS.items()}
N_HMM_SETS = 5
HMM_SETS = {'HMM' + str(i + 1) for i in range(N_HMM_SETS)}
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
HMM_DIR = BASE_DIR + '/HMM_sets'
HMM_SEARCH = BASE_DIR + '/software/hmmer/hmmsearch'
PRODIGAL = BASE_DIR + '/software/prodigal/prodigal'
MODELS_DIR = BASE_DIR + '/trained_models_2015'
MODELS_TAR_GZ = BASE_DIR + '/trained_models_2015.tar.gz'
HMM_TAR_GZ = BASE_DIR + '/HMM_sets.tar.gz'
MAX_N_MISS = 2

def cmd_exists(cmd):
    return sp.call(['type', cmd], shell=True, stdout=sp.PIPE, stderr=sp.PIPE) == 0

def validate_args(args):
    if not os.path.exists(args.fasta_file):
        raise ValueError('{} does not exist'.format(args.fasta_file))

    if type(args.regressors) == str:
        args.regressors = [args.regressors]

    for reg in args.regressors:
        if reg not in REGRESSORS:
            raise ValueError('{} not a valid regressor, must be one of {}'.format(reg, tuple(REGRESSORS.keys())))

    if type(args.classifiers) == str:
        args.classifiers = [args.classifiers]

    for clf in args.classifiers:
        if clf not in CLASSIFIERS:
            raise ValueError('{} not a valid classifier, must be one of {}'.format(clf, tuple(CLASSIFIERS.keys())))

    if type(args.hmm_sets) == str:
        args.hmm_sets = [args.hmm_sets]

    for hmm in args.hmm_sets:
        if hmm not in HMM_SETS:
            raise ValueError('{} not a valid HMM set, must be one of {}'.format(hmm, HMM_SETS))

    if not cmd_exists(args.hmmsearch_cmd):
        raise ValueError('{} not found or not in PATH'.format(args.hmmsearch_cmd))
    
    if args.sequence_type not in SEQUENCE_TYPES:
        raise ValueError('{} not a valid sequence type, must be one of {}'.format(SEQUENCE_TYPES))
    
    if args.run_mode not in RUN_MODES:
        raise ValueError('{} not a valid run mode, must be one of {}'.format(RUN_MODES))
    
    if args.sequence_completeness not in SEQUENCE_COMPLETENESS:
        raise ValueError('{} not a valid sequence completeness option, must be one of {}'.format(SEQUENCE_COMPLETENESS))

def parse_protein_id_from_dna(line):
    # print(line)
    id_first_part, start, end, strand, id_second_part = line.split('#')
    id_first_part = id_first_part.replace('>', '').strip()
    start = int(start.strip())
    end = int(end.strip())
    strand = int(strand)
    id_second_part = id_second_part.strip().split(';')[0]
    id_ = id_first_part + '_' + id_second_part
    return id_, start, end, strand

def build_initial_dataframe(fasta_file, sequence_type):
    data = defaultdict(list)
    protein_ids = []

    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                if sequence_type == 'protein':
                    id_ = line.strip().replace('>', '').split()[0]
                else:
                    id_, start, end, strand = parse_protein_id_from_dna(line)
                                
                if id_ not in protein_ids:
                    protein_ids.append(id_)

                    if sequence_type == 'dna':
                        data['start'].append(start)
                        data['end'].append(end)
                        data['strand'].append(strand)

    return pd.DataFrame(data, index=protein_ids)

def annotate_proteins(initial_protein_df, hmmsearch_output_dir, hmm_sets, sequence_type, cassette_output_dir=None, save_csv=False):
    annotated_protein_dataframes = {}

    for hmm in hmm_sets:
        protein_df = initial_protein_df.copy()
        annotated_protein_dataframes[hmm] = add_bitscores(os.path.join(hmmsearch_output_dir, hmm), protein_df, sequence_type)

        if save_csv:
            annotated_protein_dataframes[hmm].to_csv(os.path.join(cassette_output_dir, hmm + '_annotated_proteins.csv'))

    return annotated_protein_dataframes

def add_bitscores(hmm_output_dir, protein_df, sequence_type):
    protein_df = protein_df.assign(bitscore=np.repeat(-1.0, protein_df.shape[0]))
    protein_df = protein_df.assign(annotation=np.repeat('unknown', protein_df.shape[0]))

    hmm_output_files = glob.glob(hmm_output_dir + '/*.tab')

    for file_path in hmm_output_files:
        annotation = file_path.split('/')[-1].split('_')[0]
        
        if annotation in CAS_SYNONYM_LIST:
            annotation = CAS_SYNONYM_LIST[annotation]

        with open(file_path, 'r') as f:
            for line in f:
                if not line.startswith('#'):
                    hmm_result = line.strip().split()

                    id_ = hmm_result[0]
                    bitscore = float(hmm_result[5])

                    if sequence_type == 'dna':
                        id_second_part = hmm_result[-1].strip().split(';')[0]
                        id_ += '_' + id_second_part
                    
                    if bitscore > protein_df.at[id_, 'bitscore']:
                        protein_df.at[id_, 'bitscore'] = bitscore
                        protein_df.at[id_, 'annotation'] = annotation
    
    return protein_df

def build_cassettes(annotated_protein_dataframes, sequence_type, max_gap=2, min_proteins=2, max_nt_diff=500, cassette_output_dir=None, save_csv=False):
    cassette_dataframes = {}

    for hmm, protein_df in annotated_protein_dataframes.items():

        if sequence_type == 'protein':
            cassette_ids = np.ones(protein_df.shape[0], dtype=np.int)
            cassette_df = protein_df
        
        else:
            cassettes = []
            indices_cassette = []
            gap = 0
            cas_count = 0
            
            for i, (idx, row) in enumerate(protein_df.iterrows()):
                nt_diff = row['start'] - protein_df.iloc[i - 1]['end'] if i > 0 else 0

                if ((row['annotation'] != 'unknown' and len(indices_cassette) == 0) or \
                    (row['annotation'] != 'unknown' and nt_diff <= max_nt_diff)) and \
                    gap <= max_gap:
                    indices_cassette.append(idx)
                    gap = 0
                    cas_count += 1

                elif i > 0 and len(indices_cassette) > 0 and row['annotation'] == 'unknown' and nt_diff <= max_nt_diff and gap < max_gap:
                    indices_cassette.append(idx)
                    gap += 1

                elif len(indices_cassette) > 0 and cas_count >= min_proteins:
                    for idx2filter in list(reversed(indices_cassette)):
                        if protein_df.at[idx2filter, 'annotation'] == 'unknown':
                            indices_cassette.pop()
                        else:
                            break

                    protein_df_cassette = protein_df.loc[indices_cassette]
                    unique_cassette_proteins = set(protein_df_cassette[protein_df_cassette['annotation'] != 'unknown']['annotation'])

                    if len(unique_cassette_proteins) > 1 and len(unique_cassette_proteins.intersection(CORE)) >= 1:
                        cassettes.append(indices_cassette)

                    gap = 0
                    cas_count = 0
                    indices_cassette = []

                else:
                    gap = 0
                    cas_count = 0
                    indices_cassette = []

            cassette_ids = [[i + 1] * len(c) for i, c in enumerate(cassettes)]
            cassette_ids = list(itertools.chain.from_iterable(cassette_ids))
            cassettes = list(itertools.chain.from_iterable(cassettes))
            cassette_df = protein_df.loc[cassettes]
        
        cassette_df = cassette_df.assign(cassette_id=cassette_ids)

        if save_csv:
            cassette_df.to_csv(os.path.join(cassette_output_dir, hmm + '_cassettes.csv'))
        
        cassette_dataframes[hmm] = cassette_df.assign(cassette_id=cassette_ids)

    return cassette_dataframes

def convert_cassette_dataframes_to_numpy_arrays(cassette_dataframes, models_dir, cassette_output_dir):
    hmm_cassette_arrays = {}
    hmm_features = {}
    hmm_missings = {}

    for hmm, cassette_df in cassette_dataframes.items():
        features = joblib.load(os.path.join(models_dir, hmm + '_features.joblib'))
        feature_to_idx = dict(zip(features, np.arange(len(features))))
        n_missings = []
        cassette_arrays = []

        for idx, cassette in cassette_df.groupby(by='cassette_id'):
            array = np.zeros(len(features))
            n_miss = (cassette['annotation'] == 'unknown').sum()

            for _, row in cassette.iterrows():
                if row['annotation'] != 'unknown' and row['annotation'] in feature_to_idx:
                    j = feature_to_idx[row['annotation']]
                    array[j] = max(array[j], row['bitscore'])
            
            cassette_arrays.append(array)
            n_missings.append(n_miss)
        
        if cassette_arrays:
            scaler = joblib.load(os.path.join(models_dir, hmm + '_scaler.joblib'))
            cassette_arrays = np.array(cassette_arrays)
            cassette_arrays = scaler.transform(cassette_arrays)

            cassette_header = ' '.join(features)
            cassette_file_path = os.path.join(cassette_output_dir, hmm + '_cassette_arrays.txt')
            print('Saving cassette(s) to', cassette_file_path)
            np.savetxt(os.path.join(cassette_output_dir, hmm + '_cassette_arrays.txt'), cassette_arrays, header=cassette_header)

            hmm_cassette_arrays[hmm] = cassette_arrays
            hmm_features[hmm] = features
            hmm_missings[hmm] = n_missings
        else:
            print('CRISPRcasIdentifier could not find enough hits to build one or more cassettes for the input file and ', hmm, '.', sep='')

    return hmm_features, hmm_cassette_arrays, hmm_missings

def predict_missings(models_dir, regressor, hmm_features, hmm_cassettes, hmm_missings):
    filled_cassettes = defaultdict(list)
    reg_name = REGRESSORS[regressor]

    print('\n' + '-' * 50)

    for hmm in sorted(hmm_missings):
        for id_, n_miss in enumerate(hmm_missings[hmm]):
            cassette = np.copy(hmm_cassettes[hmm][id_])

            if np.any(cassette > 0.0):
                if n_miss == 0:
                    print('There are no unlabeled proteins for cassette #', id_ + 1, 'and', hmm)
                elif n_miss == 1:
                    print('There is', n_miss, 'unlabeled protein for cassette #', id_ + 1, 'and', hmm)
                else:
                    print('There are', n_miss, 'unlabeled proteins for cassette #', id_ + 1, 'and', hmm)
                
                if n_miss > MAX_N_MISS:
                    print('More than ' + str(MAX_N_MISS) + ' missing proteins. Regression predictions will likely be weak.')

                if n_miss:
                    zeros_idx = np.where(cassette == 0.0)[0]
                    features = hmm_features[hmm]
                    features_to_test = features[zeros_idx]

                    predictions = []

                    for j, f in zip(zeros_idx, features_to_test):
                        reg = joblib.load(os.path.join(models_dir, hmm + '_' + reg_name + '_' + f + '.joblib'))
                        cassette_f = np.delete(cassette, j)
                        pred = reg.predict(np.expand_dims(cassette_f, axis=0))[0]
                        predictions.append((j, f, pred))

                    predictions = sorted(predictions, key=lambda x : -x[-1])

                    for i in range(n_miss):
                        j, f, pred = predictions[i]
                        print('{0} missing bit-score prediction for cassette #{1}, {2} and {3} ({4}/{5}): {6:.3f}'.format(regressor, id_ + 1, hmm, f, i + 1, n_miss, pred))
                        cassette[j] = pred # because cassette is a 2d 1 x m array
                
                filled_cassettes[hmm].append(cassette)
            
            else:
                print('Cassette #' + str(id_ + 1) + ' is either empty or composed only by unknown proteins for ' + hmm + '. '
                      'Regressors are not able to predict anything.')
            
            print('-' * 50)

    return filled_cassettes

def classify(models_dir, regressor_name, classifiers, hmm_cassettes, return_probability, hmm_missings, output_defaultdict):
    for hmm in sorted(hmm_cassettes):
        cassette = hmm_cassettes[hmm]
        encoder = joblib.load(os.path.join(models_dir, hmm + '_encoder.joblib'))

        if regressor_name:
            print('Predictions for', hmm, 'and', regressor_name, 'regressor\n')
        else:
            print('Predictions for', hmm, 'without regression\n')

        for ci, casc in enumerate(cassette):
            if np.any(casc > 0.0):
                if not regressor_name and hmm_missings[hmm][ci] > MAX_N_MISS:
                    print('More than ' + str(MAX_N_MISS) + ' missing proteins. Classification predictions will likely be weak.')

                casc = np.expand_dims(casc, axis=0)
                
                for clf_name in classifiers:
                    # saving output information ------------------------
                    output_defaultdict['HMM'].append(hmm)
                    output_defaultdict['cassette_id'].append(ci + 1)
                    output_defaultdict['classifier'].append(CLASSIFIERS_INV[clf_name])

                    if regressor_name:
                        output_defaultdict['regressor'].append(regressor_name)
                    # --------------------------------------------------

                    clf = joblib.load(os.path.join(models_dir, hmm + '_' + clf_name + '.joblib'))

                    if return_probability:
                        pred = clf.predict_proba(casc)
                        pred_class_idx = np.where(pred > 0.0)
                        pred_class_names = encoder.inverse_transform(pred_class_idx[1])
                        pred_probs = pred[pred_class_idx]
                        sorted_idx = np.argsort(-pred_probs)
                        prob_str = ', '.join('{0} ({1:.3f})'.format(name, prob) for name, prob in zip(pred_class_names[sorted_idx], pred_probs[sorted_idx]))
                        print('Cassette #{} -- {}: {}'.format(ci + 1, CLASSIFIERS_INV[clf_name], prob_str))

                        pred_label = list(zip(pred_class_names[sorted_idx], pred_probs[sorted_idx]))
                    else:
                        pred = clf.predict(casc)
                        pred_label = encoder.inverse_transform(pred)[0]
                        print('Cassette #{} -- {}: {}'.format(ci + 1, CLASSIFIERS_INV[clf_name], pred_label))
                    
                    output_defaultdict['predicted_label'].append(pred_label)

                print()
            
            else:
                print('Cassette #' + str(ci + 1) + ' is either empty or composed only by unknown proteins for ' + hmm + '. '
                      'Classifiers are not able to predict anything.')

        print('-' * 50)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-f', '--fasta', dest='fasta_file', help='Fasta file path', metavar='sequences.fa')
    parser.add_argument('-r', '--regressors', nargs='+', dest='regressors', help='List of regressors (CART, ERT and SVM), default: ERT', default='ERT', metavar='reg')
    parser.add_argument('-c', '--classifiers', nargs='+', dest='classifiers', help='List of classifiers (CART, ERT and SVM), default: ERT', default='ERT', metavar='clf')
    parser.add_argument('-p', '--class-probabilities', dest='probability', action='store_true', help='Whether to return class probabilities')
    parser.add_argument('-s', '--hmm-sets', nargs='+', dest='hmm_sets', help='List of HMM sets (from HMM1 to HMM5), default: HMM3', metavar='HMM_set', default='HMM3')
    parser.add_argument('-hp', '--hmmsearch-path', nargs='?', dest='hmmsearch_cmd', help='hmmsearch binary path, default: ./software/hmmer/hmmsearch', default=HMM_SEARCH)
    parser.add_argument('-ho', '--hmmsearch-output-dir', nargs='?', dest='hmmsearch_output_dir', help='hmmsearch output folder (default: ./hmmsearch_output)', default='hmmsearch_output')
    parser.add_argument('-co', '--cassette-output-dir', nargs='?', dest='cassette_output_dir', help='cassette output folder, default: ./cassette', default='cassette')
    parser.add_argument('-st', '--sequence-type', nargs='?', dest='sequence_type', default='protein', help='Sequence type (dna or protein), default: protein', metavar='seq_type')
    parser.add_argument('-sc', '--sequence-completeness', nargs='?', dest='sequence_completeness', help='Sequence completeness (complete or partial), used only if sequence type is dna, default: complete', default='complete', metavar='seq_comp')
    parser.add_argument('-m', '--mode', nargs='?', dest='run_mode', help='Run mode (classification, regression or mixed), default: classification', default='classification', metavar='mode')
    parser.add_argument('-o', '--output-file', nargs='?', dest='output_file', help='Where to store the results, default: ./CRISPRcasIdentifier_output.csv', default='CRISPRcasIdentifier_output.csv')
    args = parser.parse_args()
    validate_args(args)

    if not os.path.exists(HMM_DIR):
        print('Extracting', HMM_TAR_GZ)
        with tarfile.open(HMM_TAR_GZ, 'r:gz') as tar:
            tar.extractall()

    if not os.path.exists(MODELS_DIR):
        print('Extracting', MODELS_TAR_GZ)
        with tarfile.open(MODELS_TAR_GZ, 'r:gz') as tar:
            tar.extractall()
    
    if not os.path.exists(args.cassette_output_dir):
        os.mkdir(args.cassette_output_dir)
    
    if not os.path.exists(args.hmmsearch_output_dir):
        os.mkdir(args.hmmsearch_output_dir)
    
    if args.sequence_type == 'dna':
        print('Running prodigal on DNA sequences')
        args.fasta_file = prodigal(PRODIGAL, args.fasta_file, args.sequence_completeness)

    print('Running hmmsearch (log and outputs stored in {})'.format(args.hmmsearch_output_dir))
    hmmsearch(args.hmmsearch_cmd, args.fasta_file, HMM_DIR, args.hmm_sets, args.hmmsearch_output_dir)

    print('Annotating proteins')
    protein_df = build_initial_dataframe(args.fasta_file, args.sequence_type)
    annotated_protein_dfs = annotate_proteins(protein_df, args.hmmsearch_output_dir, args.hmm_sets, args.sequence_type, args.cassette_output_dir, save_csv=True)

    print('Building cassettes')
    hmm_cassettes = build_cassettes(annotated_protein_dfs, args.sequence_type, cassette_output_dir=args.cassette_output_dir, save_csv=True)
    hmm_features, hmm_cassettes, hmm_missings = convert_cassette_dataframes_to_numpy_arrays(hmm_cassettes, MODELS_DIR, args.cassette_output_dir)

    classifiers = [CLASSIFIERS[clf] for clf in args.classifiers]
    output_defaultdict = defaultdict(list)

    if hmm_cassettes:
        if args.run_mode == 'classification':
            print('Loading classifiers and running classification')
            classify(MODELS_DIR, '', classifiers, hmm_cassettes, args.probability, hmm_missings, output_defaultdict)

        else:
            for reg in args.regressors:
                hmm_cassettes_reg = predict_missings(MODELS_DIR, reg, hmm_features, hmm_cassettes, hmm_missings)

                if args.run_mode == 'mixed':
                    print('Loading classifiers and running classification')
                    classify(MODELS_DIR, reg, classifiers, hmm_cassettes_reg, args.probability, hmm_missings, output_defaultdict)

        if output_defaultdict:
            print('Saving class predictions to', args.output_file)
            output_df = pd.DataFrame(output_defaultdict)
            output_df.to_csv(args.output_file, index=False)
        else:
            print('No predictions were made.')