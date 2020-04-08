"""
    CRISPRCasIdentifier
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

import subprocess as sp
import os

def hmmsearch(hmmsearch_cmd, fasta_file, hmm_dir, hmm_sets, hmmsearch_output_dir, cutoff=1000):
    if not os.path.exists(hmmsearch_output_dir):
        os.mkdir(hmmsearch_output_dir)

    hmm_set_output_directories = []

    for hmm in hmm_sets:
        hmm_set_dir = os.path.join(hmm_dir, hmm)
        hmm_set_output_dir = os.path.join(hmmsearch_output_dir, hmm)
        hmm_set_output_directories.append(hmm_set_output_dir)

        if not os.path.exists(hmm_set_output_dir):
            os.mkdir(hmm_set_output_dir)

        hmm_files = os.listdir(hmm_set_dir)

        for hmm_f in hmm_files:
            hmm_file_path = os.path.join(hmm_set_dir, hmm_f)

            output_file_path = os.path.join(hmm_set_output_dir, hmm_f.replace('.hmm', '.tab'))
            log_file_path = os.path.join(hmm_set_output_dir, hmm_f.replace('.hmm', '.log'))

            with open(log_file_path, 'w') as log_file:
                sp.call([hmmsearch_cmd, '--tblout', output_file_path, '-E', str(cutoff), hmm_file_path, fasta_file], stdout=log_file, stderr=log_file)