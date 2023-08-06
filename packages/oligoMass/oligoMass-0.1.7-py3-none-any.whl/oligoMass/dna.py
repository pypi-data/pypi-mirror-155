import molmass as mm

extinction_labels = 'pdA pdC pdG pdT dApdA dApdC dApdG dApdT dCpdA dCpdC dCpdG dCpdT dGpdA dGpdC dGpdG dGpdT dTpdA dTpdC dTpdG dTpdT'
extinction_list = '15400 7400 11500 8700 27400 21200 25000 22800 21200 14600 18000 15200 25200 17600 21600 20000 23400 16200 19000 16800'


def get_extinction_dict():
    out = {}
    lbs = extinction_labels.split(' ')
    cfs = extinction_list.split(' ')
    for i, e in enumerate(cfs):
        seq = ''
        for j in lbs[i]:
            if j in 'A T G C'.split(' '):
                seq += j
        out[seq] = float(e)

    return out


def string2seq(string):
    seq = ''
    for l in string:
        if l in 'A C G T'.split(' '):
            seq += l
    return seq


def get_simple_ssdna_extinction(string, ext_tab):
    seq = list(string2seq(string))
    s = 0
    for i in range(len(seq) - 1):
        key = seq[i] + seq[i + 1]
        s += ext_tab[key]
    for i in range(1, len(seq) - 1):
        key = seq[i]
        s -= ext_tab[key]
    return int(round(s, 0))


def melting_temp(string):
    tm = 0
    seq = list(string2seq(string))
    nts = {}
    nts['A'], nts['T'], nts['C'], nts['G'] = 0, 0, 0, 0
    for s in seq:
        nts[s] += 1
    if len(seq) < 14:
        tm = (nts['A'] + nts['T']) * 2 + (nts['C'] + nts['G']) * 4
    else:
        tm = 64.9 + 41 * (nts['C'] + nts['G'] - 16.4) / len(seq)
    return tm

class nucleoside():
    def __init__(self):
        self.name = ''
        self.formula = ''
        self.symbol = ''

class deoxynusleosideDB():
    def __init__(self):

        self.dA = nucleoside()
        self.dA.name = 'deoxyAdenosin'
        self.dA.symbol = 'A'
        self.dA.formula = 'C10H13N5O3'
        self.dA.seqformula = 'C10H11N5O3'

        self.dT = nucleoside()
        self.dT.name = 'Thymidine'
        self.dT.symbol = 'T'
        self.dT.formula = 'C10H14N2O5'
        self.dT.seqformula = 'C10H12N2O5'

        self.dG = nucleoside()
        self.dG.name = 'Deoxyguanosine'
        self.dG.symbol = 'G'
        self.dG.formula = 'C10H13N5O4'
        self.dG.seqformula = 'C10H11N5O4'

        self.dC = nucleoside()
        self.dC.name = 'Deoxycytidine'
        self.dC.symbol = 'C'
        self.dC.formula = 'C9H13N3O4'
        self.dC.seqformula = 'C9H11N3O4'

        self.dU = nucleoside()
        self.dU.name = 'Deoxyuridine'
        self.dU.symbol = 'U'
        self.dU.formula = 'C9H12N2O5'
        self.dU.seqformula = 'C9H10N2O5'

        self.Nsymbol = {'A': self.dA, 'T': self.dT, 'G': self.dG, 'C': self.dC, 'U': self.dU}

    def __call__(self, symbol):
        return self.Nsymbol[symbol]

class oligoSeq():
    def __init__(self, s):
        self.init_str = s
        self.seq = None
        self.modifications_dict = None
        self.mod_formula = None
        self.modifications = None

        self.dnaDB = deoxynusleosideDB()
        self.set_modifications()
        self.seq = self.string2seq(s)


    def set_modifications(self):
        self.modifications_dict = {}
        self.modifications_dict['LNA'] = '+ '
        self.modifications_dict['tio'] = '* '
        self.modifications_dict['methyl'] = 'm '
        self.modifications_dict['ribo'] = 'r '

        self.mod_formula = {}
        self.mod_formula['LNA'] = ['CO', '']
        self.mod_formula['tio'] = ['S', 'O']
        self.mod_formula['methyl'] = ['OCH2', '']
        self.mod_formula['ribo'] = ['O', '']

        self.modifications = {}
        for k in self.modifications_dict.keys():
            self.modifications[k] = 0

    def string2seq(self, s):
        ll = list(s)
        out = ''
        for l in ll:
            if l in 'A C G T U a c g t u'.split(' '):
                out += l.upper()
            for k in self.modifications_dict.keys():
                if l in self.modifications_dict[k].split(' '):
                    self.modifications[k] += 1
        return out

    def string2seq_alpha(self, s, alpha='A C G T U a c g t u'):
        ll = list(s)
        out = ''
        for l in ll:
            if l in alpha.split(' '):
                out += l.upper()
            for k in self.modifications_dict.keys():
                if l in self.modifications_dict[k].split(' '):
                    self.modifications[k] += 1
        return out

    def seq_end_cut(self, s, cut_number=1, end_type="5'"):
        seq = list(self.string2seq_alpha(s, alpha='A C G T a c g t +'))
        if end_type == "5'":
            for i in range(cut_number):
                if seq[0] in ['+']:
                    seq.pop(0)
                if seq[0] in 'A C G T'.split(' '):
                    seq.pop(0)

        if end_type == "3'":
            for i in range(cut_number):
                if seq[-1] in 'A C G T'.split(' '):
                    seq.pop(-1)
                if seq[-1] in ['+']:
                    seq.pop(-1)

        return ''.join(seq)

    def __get_mod_formula(self, formula):
        f_mod, f_ = '', ''
        for k in self.modifications.keys():
            for i in range(self.modifications[k]):
                f_mod += self.mod_formula[k][0]
                f_ += self.mod_formula[k][1]
        if f_ != '':
            return (mm.Formula(formula) + mm.Formula(f_mod) - mm.Formula(f_)).empirical
        else:
            return (mm.Formula(formula) + mm.Formula(f_mod)).empirical

    def getBruttoFormula(self):
        f = ''
        for n in self.seq:
            f += self.dnaDB(n).seqformula
        for n in range(len(self.seq) - 1):
            f += 'HPO2'
        f += 'H2'
        return self.__get_mod_formula(f)

    def getMolecularFormula(self):
        f = mm.Formula(self.seq) - mm.Formula('HPO3')
        f = f.empirical
        return self.__get_mod_formula(f)

    def getMolMass(self):
        return mm.Formula(self.getBruttoFormula()).mass

    def getMonoMass(self):
        return mm.Formula(self.getMolecularFormula()).isotope

    def getAvgMass(self):
        return mm.Formula(self.getMolecularFormula()).mass



def test():

    f = mm.Formula('CO') + mm.Formula('CO')
    print(f.empirical)

    seq = oligoSeq('AAAU')
    print(seq.getMolMass())
    print(seq.getBruttoFormula())

    #f = mm.Formula('ACTGGGTC')
    #print(f.empirical)
    #print(f.mass)

    #dna = osa.dnaSeq('ACT+GGG+TC')
    #print(dna.getBruttoFormula())
    #print(dna.getMolMass())

def test1():
    extinction = get_simple_ssdna_extinction("CGAAGGTGTGACTTCCATG", get_extinction_dict())
    print(extinction)

if __name__ == '__main__':
    test1()