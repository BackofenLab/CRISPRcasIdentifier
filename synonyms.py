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
