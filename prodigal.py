"""
    CRISPRCasIdentifier
    Copyright (C) 2020 Victor Alexandre Padilha <victorpadilha@usp.br>,
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

def prodigal(prodigal_cmd, fasta_file, completeness):
    meta = '-p meta' if completeness == 'partial' else ''
    fasta_file_preffix = fasta_file.rsplit('.', 1)[0]
    output_fasta_file = fasta_file_preffix + '_proteins.fa'
    log_file = fasta_file_preffix + '_prodigal.log'
    prodigal_cmd += ' -i {input_fasta}  -c -m -g 11 -p single -a {output_fasta} -q' + meta
    prodigal_cmd = prodigal_cmd.format(prodigal=prodigal_cmd, input_fasta=fasta_file, output_fasta=output_fasta_file)
    
    with open(log_file, 'w') as lf:
        sp.call(prodigal_cmd.split(), stdout=lf)
    
    return output_fasta_file