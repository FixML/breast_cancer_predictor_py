Search.setIndex({"docnames": ["breast_cancer_predictor_report"], "filenames": ["breast_cancer_predictor_report.ipynb"], "titles": ["Predicting breast cancer from digitized images of breast mass"], "terms": {"tiffani": 0, "A": 0, "timber": 0, "joel": 0, "ostblom": 0, "melissa": 0, "lee": 0, "2023": 0, "11": 0, "09": 0, "import": 0, "panda": 0, "pd": [], "myst_nb": [], "glue": [], "here": 0, "we": 0, "attempt": 0, "build": 0, "classif": 0, "model": 0, "us": 0, "k": 0, "nearest": 0, "neighbour": 0, "algorithm": 0, "which": 0, "can": 0, "tumour": 0, "measur": 0, "whether": 0, "newli": 0, "discov": 0, "benign": 0, "i": 0, "e": 0, "harm": 0, "doe": 0, "requir": 0, "treatment": 0, "malign": 0, "intervent": 0, "our": 0, "final": 0, "classifi": 0, "perform": 0, "fairli": 0, "well": 0, "an": 0, "unseen": 0, "test": 0, "set": 0, "f2": 0, "score": 0, "where": 0, "beta": 0, "2": 0, "0": 0, "96": 0, "overal": 0, "accuraci": 0, "calcul": 0, "On": 0, "171": 0, "case": 0, "correctli": 0, "168": 0, "It": 0, "incorrectli": 0, "3": 0, "were": 0, "all": 0, "fals": 0, "posit": 0, "when": 0, "fact": 0, "These": 0, "kind": 0, "incorrect": 0, "neg": 0, "context": 0, "although": 0, "thei": 0, "could": 0, "theoret": 0, "caus": 0, "patient": 0, "undergo": 0, "unnecessari": 0, "decis": 0, "tool": 0, "like": 0, "initi": 0, "screen": 0, "follow": 0, "up": 0, "appoint": 0, "further": 0, "until": 0, "commenc": 0, "As": 0, "believ": 0, "thi": 0, "close": 0, "have": 0, "clinic": 0, "util": 0, "research": 0, "improv": 0, "understand": 0, "characterist": 0, "would": 0, "still": 0, "women": 0, "12": 0, "1": 0, "lifetim": 0, "probabl": 0, "develop": 0, "ha": 0, "over": 0, "last": 0, "30": 0, "year": 0, "project": 0, "death": 0, "rate": 0, "s": 0, "22": 0, "4": 0, "per": 0, "100": 0, "000": 0, "2019": 0, "canadian": 0, "statist": 0, "advisori": 0, "committe": 0, "earli": 0, "detect": 0, "been": 0, "shown": 0, "outcom": 0, "thu": 0, "assai": 0, "technolog": 0, "help": 0, "diagnosi": 0, "mai": 0, "benefici": 0, "ask": 0, "machin": 0, "learn": 0, "given": 0, "answer": 0, "question": 0, "becaus": 0, "tradit": 0, "ar": 0, "quit": 0, "subject": 0, "depend": 0, "diagnos": 0, "physician": 0, "skill": 0, "experi": 0, "street": 0, "wolberg": 0, "mangasarian": 0, "1993": 0, "furthermor": 0, "normal": 0, "danger": 0, "cell": 0, "stai": 0, "same": 0, "place": 0, "stop": 0, "grow": 0, "befor": 0, "get": 0, "veri": 0, "larg": 0, "By": 0, "contrast": 0, "invad": 0, "surround": 0, "tissu": 0, "spread": 0, "nearbi": 0, "organ": 0, "seriou": 0, "damag": 0, "accur": 0, "effect": 0, "lead": 0, "less": 0, "more": 0, "scalabl": 0, "contribut": 0, "better": 0, "The": 0, "featur": 0, "creat": 0, "dr": 0, "william": 0, "h": 0, "w": 0, "nick": 0, "olvi": 0, "l": 0, "univers": 0, "wisconsin": 0, "madison": 0, "wa": 0, "sourc": 0, "uci": 0, "repositori": 0, "found": 0, "specif": 0, "file": 0, "each": 0, "row": 0, "repres": 0, "sampl": 0, "includ": 0, "sever": 0, "other": 0, "g": 0, "nucleu": 0, "textur": 0, "perimet": 0, "area": 0, "etc": 0, "conduct": 0, "neighbor": 0, "nn": 0, "class": 0, "column": 0, "variabl": 0, "origin": 0, "except": 0, "standard": 0, "error": 0, "fractal": 0, "dimens": 0, "smooth": 0, "symmetri": 0, "fit": 0, "split": 0, "70": 0, "being": 0, "partit": 0, "train": 0, "hyperparamet": 0, "chosen": 0, "fold": 0, "cross": 0, "valid": 0, "metric": 0, "increas": 0, "weight": 0, "recal": 0, "dure": 0, "applic": 0, "undesir": 0, "just": 0, "prior": 0, "python": 0, "program": 0, "languag": 0, "van": 0, "rossum": 0, "drake": 0, "2009": 0, "packag": 0, "request": 0, "reitz": 0, "2011": 0, "zipfil": 0, "numpi": 0, "harri": 0, "et": 0, "al": 0, "2020": 0, "mckinnei": 0, "2010": 0, "altair": 0, "vanderpla": 0, "2018": 0, "scikit": 0, "pedregosa": 0, "code": 0, "report": 0, "ttimber": 0, "breast_cancer_predictor_pi": 0, "To": 0, "look": 0, "predictor": 0, "might": 0, "plot": 0, "distribut": 0, "colour": 0, "blue": 0, "orang": 0, "figur": 0, "In": 0, "do": 0, "see": 0, "mean": 0, "max": 0, "overlap": 0, "somewhat": 0, "show": 0, "differ": 0, "centr": 0, "so": 0, "se": 0, "particular": 0, "similar": 0, "both": 0, "choos": 0, "omit": 0, "comparison": 0, "empir": 0, "between": 0, "chose": 0, "simpl": 0, "find": 0, "best": 0, "select": 0, "number": 0, "observ": 0, "optim": 0, "cancer_choose_k": 0, "vari": 0, "read_csv": [], "tabl": [], "test_scor": [], "csv": [], "962145": 0, "98": 0, "indic": 0, "come": 0, "confus": 0, "matrix": 0, "onli": 0, "made": 0, "mistak": 0, "promis": 0, "implement": 0, "than": 0, "df": [], "confusion_matrix": [], "index_col": [], "index": [], "name": [], "actual": 0, "label": 0, "107": 0, "61": 0, "while": 0, "alreadi": 0, "direct": 0, "explor": 0, "first": 0, "misclassifi": 0, "compar": 0, "them": 0, "goal": 0, "drive": 0, "misclassif": 0, "ani": 0, "engin": 0, "current": 0, "make": 0, "addition": 0, "try": 0, "One": 0, "random": 0, "forest": 0, "automat": 0, "allow": 0, "interact": 0, "also": 0, "usabl": 0, "output": 0, "estim": 0, "If": 0, "cannot": 0, "prevent": 0, "through": 0, "approach": 0, "suggest": 0, "abov": 0, "least": 0, "clinician": 0, "know": 0, "how": 0, "confid": 0, "its": 0, "abil": 0, "addit": 0, "diagnost": 0, "high": 0, "canadiancsacommittee19": 0, "societi": 0, "url": 0, "http": 0, "ca": 0, "en": 0, "tag": [], "remov": [], "input": [], "line": [], "syntaxerror": [], "invalid": [], "syntax": []}, "objects": {}, "objtypes": {}, "objnames": {}, "titleterms": {"predict": 0, "breast": 0, "cancer": 0, "from": 0, "digit": 0, "imag": 0, "mass": 0, "summari": 0, "introduct": 0, "method": 0, "data": 0, "analysi": 0, "result": 0, "discuss": 0}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 6, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.intersphinx": 1, "sphinxcontrib.bibtex": 9, "sphinx": 56}})