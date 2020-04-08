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

CAS_SYNONYM_LIST = {
                 "csa1":"cas4",
                 "csa4":"cas8",
                 "csx9":"cas8",
                 "csh1":"cas8",
                 "csd1":"cas8",
                 "csp2":"cas8",
                 "GSU0054":"cas5",
                 "csc3":"cas10",
                 "csc2":"cas7",
                 "csc1":"cas5",
                 "cse1":"cas8",
                 "cse3":"cas6",
                 "cse4":"cas7",
                 "casB":"cse2",
                 "casc":"cas7",
                 "casD":"cas5",
                 "casE":"cas6",
                 "csy1":"cas8",
                 "csy2":"cas5",
                 "csy3":"cas7",
                 "csy4":"cas6",
                 "cst1":"cas8",
                 "cst2":"cas7",
                 "cst5t":"cas5",
                 "csn1":"cas9",
                 "csf4":"DinG",
                 "csf2":"cas7",
                 "csf3":"cas5",
                 "c2c2":"cas13",
                 "cpf1":"cas12",
                 "c2c1":"cas12",
                 "c2c3":"cas12",
                 "casY":"cas12",
                 "casX":"cas12",
                 "c2c6":"cas13",
                 "c2c7":"cas13",

                 "csx10":"cas5",

                 #skipping the csm/cmr proteins, as it is helpful to see them as is
                 "csm3":"cas7",
                 "csm4":"cas5",
                 "csm5":"cas7",

                 "cmr1":"cas7",
                 "cmr6":"cas7",
                 "cmr4":"cas7",
                 "cmr3":"cas5",

                 }

assert len(set(CAS_SYNONYM_LIST.keys())) == len(CAS_SYNONYM_LIST)

CAS_INVERSE_SYNONYM_LIST = {}

for k, i in CAS_SYNONYM_LIST.items():
    s = CAS_INVERSE_SYNONYM_LIST.setdefault(i, set())
    s.add(k)

CAS_PATTERN = '((cas|csa|csb|csc|cse|csy|csf|csm|csx|all|cmr|csn|cpf|c2c|csh|csd|csp)(\d+|[B,D,E,X,Y,R])|DinG|dinG|ding|Ding|GSU0054|gsu0054|cst5t)'

CORE = set('cas3,cas5,cas7,cas8,cas9,cas10,csn2,cas12,'
'cpf1,casX,c2c1,c2c3,casY,cas13,c2c2,c2c6,c2c7,csc2,csc1,cse1,cse2,cas11,'
'csy1,csy2,csy3,csf5,csf1,csf3,csm2,csm3,csm4,csm5,cmr1,cmr3,'
'cmr4,cmr5,cmr6'.split(','))