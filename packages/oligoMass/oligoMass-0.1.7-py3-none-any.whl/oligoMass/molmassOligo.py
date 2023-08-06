#import molmass as mm
import pandas as pd

import oligoMass.dna as dna
import oligoMass.exModifications as exMod

from oligoMass.ElementsTable import Elements

class EmpericalFormula():

    def __init__(self, str_formula):
        self.init_str = str_formula
        self.dict_formula = self.__convert_formula()
        self.formula = self.__formuls_to_str(self.dict_formula)

    def __convert_formula(self):

        def prepare(init_list):
            ret = []
            prev = ''
            for i in init_list + ['!']:

                if not i.isdigit() and not prev.isdigit() and prev != '':
                    if i.isupper():
                        ret.append('1')

                if i != '!':
                    ret.append(i)
                else:
                    if not prev.isdigit() and prev != '':
                        ret.append('1')
                prev = i

            return ret

        #print(list(self.init_str))
        #print(prepare(list(self.init_str)))

        ret = {}
        key, val = '', ''
        #print(prepare(list(self.init_str)) + ['!'])
        for s in prepare(list(self.init_str)) + ['!']:
            if not s.isdigit():
                if val != '':
                    if key in ret.keys():
                        ret[key] += int(val)
                    else:
                        ret[key] = int(val)
                    key, val = '', ''

                if s.isupper():
                    key = s
                else:
                    key += s
            else:
                val += s
        return ret

    def __formuls_to_str(self, fdict):
        ret = ''
        for key in fdict.keys():
            if fdict[key] > 1:
                ret += key + str(fdict[key])
            else:
                ret += key
        return ret

    def mul(self, mulint):
        formula = self.__convert_formula()
        for key in formula.keys():
            formula[key] *= mulint
        return self.__formuls_to_str(formula)

    def __add__(self, other):
        for key in other.dict_formula.keys():
            if key in list(self.dict_formula.keys()):
                self.dict_formula[key] += other.dict_formula[key]
            else:
                self.dict_formula[key] = other.dict_formula[key]
        return EmpericalFormula(self.__formuls_to_str(self.dict_formula))

    def __sub__(self, other):
        for key in other.dict_formula.keys():
            if key in list(self.dict_formula.keys()):
                self.dict_formula[key] -= other.dict_formula[key]
                if self.dict_formula[key] < 0:
                    self.dict_formula[key] = 0
        return EmpericalFormula(self.__formuls_to_str(self.dict_formula))

    def __mul__(self, other):
        if type(other) == int:
            return EmpericalFormula(self.mul(other))
        else:
            return EmpericalFormula(self.formula)

    def __str__(self):
        return self.formula

    def __call__(self, *args, **kwargs):
        return self.formula

    def getAverageWeight(self):
        mass = 0.
        if self.dict_formula != {}:
            for key in self.dict_formula.keys():
                mass += self.dict_formula[key] * Elements()(key).mass
        return mass

    def getMonoWeight(self):
        mass = 0.
        if self.dict_formula != {}:
            for key in self.dict_formula.keys():
                #print(list(Elements()(key).isotopes.values())[0][0])
                mass += self.dict_formula[key] * list(Elements()(key).isotopes.values())[0][0]
        return mass


class oligoModifications():
    def __init__(self):
        self.modRead = False
        self.mod_formula = None
        self.mod_list = None

    def _add_mod(self, letter):
        pass

class oligoNAModifications(oligoModifications):
    def __init__(self):
        super().__init__()

        self.__set_modifications()
        self.exModDB = exMod.exModifDataFrame()

    def __set_modifications(self):
        self.mod_alphabet = '+ * m r'.split(' ')
        self.br_alphabet = '/ [ ] { }'.split(' ')
        self.ex_mod = {}
        self.ex_mod_key = ''
        self.last_mod = ''

        self.mod_formula = {}
        self.mod_formula['+'] = ['CO', '']
        self.mod_formula['*'] = ['S', 'O']
        self.mod_formula['m'] = ['OCH2', '']
        self.mod_formula['r'] = ['O', '']

        self.mod_list = {}
        for k in self.mod_formula.keys():
            self.mod_list[k] = 0

    def reset_modif(self, df):
        #add prefix modifications
        self.mod_list, self.ex_mod = {}, {}
        for m in df[df['prefix'] != '']['prefix']:
            if m in self.mod_alphabet:
                if m in list(self.mod_list.keys()):
                    self.mod_list[m] += 1
                else:
                    self.mod_list[m] = 1
            else:
                m = m[1:-1]
                if m in list(self.ex_mod.keys()):
                    self.ex_mod[m] += 1
                else:
                    self.ex_mod[m] = 1
        # add suffix modifications
        for m in df[df['suffix'] != '']['suffix']:
            if m in list(self.mod_list.keys()):
                self.mod_list[m] += 1
            else:
                self.mod_list[m] = 1


    def _add_mod(self, letter):
        if not self.modRead:
            if letter in self.mod_alphabet:
                self.modRead = False
                self.mod_list[letter] += 1
                self.last_mod = letter

            elif letter in self.br_alphabet:
                self.modRead = True
                self.ex_mod_key = ''
        else:
            if letter in self.br_alphabet:
                self.modRead = False
                if self.ex_mod_key in list(self.ex_mod.keys()):
                    self.ex_mod[self.ex_mod_key] += 1
                else:
                    self.ex_mod[self.ex_mod_key] = 1
                self.last_mod = f'[{self.ex_mod_key}]'
            else:
                self.ex_mod_key += letter


    def _get_mod_formula(self, formula):
        ff = EmpericalFormula(formula)
        for k in self.mod_list.keys():
            if self.mod_list[k] > 0:
                ff += EmpericalFormula(self.mod_formula[k][0]) * self.mod_list[k]
                if self.mod_formula[k][1] != '':
                    ff -= EmpericalFormula(self.mod_formula[k][1]) * self.mod_list[k]
        if len(list(self.ex_mod)) > 0:
            for key in self.ex_mod.keys():
                db_key = self.exModDB.get_mod_properties(key)
                if db_key['in_base']:
                    if db_key['formula-'] != '':
                        ff -= EmpericalFormula(db_key['formula-']) * self.ex_mod[key]
                    if db_key['formula+'] != '':
                        ff += EmpericalFormula(db_key['formula+']) * self.ex_mod[key]
                    if db_key['mass'] > 0:
                        mass = int(round(self.ex_mod[key] * db_key['mass'], 0))
                        delta = int(round(0.007941 * mass, 0))
                        ff += EmpericalFormula(f'H{mass - delta}')
                else:
                    try:
                        sep1, sep2 = key.find(';'), key.find('|')
                        sep = -1
                        if sep1 != -1:
                            sep = sep1
                        elif sep2 != -1:
                            sep = sep2
                        if sep != -1:
                            key_p, key_m = key[: sep], key[sep+1 :]
                            if key_p != '':
                                ff += EmpericalFormula(key_p) * self.ex_mod[key]
                            if key_m != '':
                                ff -= EmpericalFormula(key_m) * self.ex_mod[key]
                        else:
                            ff += EmpericalFormula(key) * self.ex_mod[key]

                    except Exception as e:
                        print(e)
        return ff()


class oligoSequence():
    def __init__(self, sequence):
        self.init_seq = sequence
        self.sequence = sequence
        self.seq = None
        self.alphabet = None

    def sequence_parser(self):
        return self.init_seq

    def size(self):
        if self.seq != None:
            return len(self.seq)

class oligoNASequence(oligoSequence):
    def __init__(self, sequence):
        super().__init__(sequence)
        self.is_mixed = False
        self.alphabet = 'A G C T U a g c t u R Y M K ' \
                        'S W H B V D N'.split(' ')
        self.mixed_alphabet = 'R Y M K ' \
                        'S W H B V D N'.split(' ')

        self.modifications = oligoNAModifications()
        self.sequence_parser()

        self.dnaDB = dna.deoxynusleosideDB()
        self.molecularFormula = self.getMolecularFormula()

    def reset_sequence(self, sequence):
        self.init_seq = sequence
        self.sequence = sequence
        self.sequence_parser()
        self.molecularFormula = self.getMolecularFormula()

    def set_mixed_na(self):
        self.mixed_na = {}
        self.mixed_na['R'], self.mixed_na['Y'] = ['A', 'G'], ['C', 'T']
        self.mixed_na['M'], self.mixed_na['K'] = ['A', 'C'], ['G', 'T']
        self.mixed_na['S'], self.mixed_na['W'] = ['C', 'G'], ['A', 'T']
        self.mixed_na['H'], self.mixed_na['B'] = ['A', 'C', 'T'], ['C', 'G', 'T']
        self.mixed_na['V'], self.mixed_na['D'] = ['A', 'C', 'G'], ['A', 'G', 'T']
        self.mixed_na['N'] = ['A', 'C', 'T', 'G']

    def __getSeqFromTab(self):
        seq = ''
        if not self._seqtab.empty:
            for p in self._seqtab.values:
                seq += p[0]
                seq += p[1]
                seq += p[2]
        return seq

    def sequence_parser(self):
        self._seqtab = {'prefix': [],
                        'nt': [],
                        'suffix': [],
                        'index': []}
        seq_list = list(self.init_seq)
        self.seq = ''
        index = 1
        for letter in seq_list:
            if letter in self.alphabet and not self.modifications.modRead:
                if letter in self.mixed_alphabet:
                    self.is_mixed = True
                self.seq += letter.upper()
                self._seqtab['nt'].append(self.seq[-1])
                self._seqtab['suffix'].append('')
                self._seqtab['prefix'].append(self.modifications.last_mod)
                self._seqtab['index'].append(index)
                self.modifications.last_mod = ''
                index += 1
            else:
                self.modifications._add_mod(letter)
                if self.modifications.last_mod in ['*']:
                    self._seqtab['suffix'][-1] = self.modifications.last_mod
                    self.modifications.last_mod = ''

        self._seqtab = pd.DataFrame(self._seqtab)
        self._seqtab.set_index('index', inplace=True)
        self.sequence = self.__getSeqFromTab()

        self.modifications.reset_modif(self._seqtab)
        return self.sequence

    def __call__(self):
        return self.sequence

    def getPrefix(self, index):
        seq = ''
        if index < self._seqtab.shape[0]:
            for i in range(1, index + 1):
                seq += self._seqtab['prefix'].loc[i] + self._seqtab['nt'].loc[i] + self._seqtab['suffix'].loc[i]
        return oligoNASequence(seq)

    def getSuffix(self, index):
        seq = ''
        if index < self._seqtab.shape[0]:
            for i in range(index + 1, self._seqtab.shape[0] + 1):
                seq += self._seqtab['prefix'].loc[i] + self._seqtab['nt'].loc[i] + self._seqtab['suffix'].loc[i]
        return oligoNASequence(seq)

    def getDeletion(self, index):
        seq = ''
        if index < self._seqtab.shape[0]:
            for i in range(1, self.size() + 1):
                if i != index:
                    seq += self._seqtab['prefix'].loc[i] + self._seqtab['nt'].loc[i] + self._seqtab['suffix'].loc[i]
        return seq

    def get_3_mod_move(self, index):
        seq = ''
        if index < self._seqtab.shape[0]:
            for i in range(1, index + 1):
                if i == index:
                    seq += self._seqtab['prefix'].loc[self._seqtab.shape[0]] + self._seqtab['nt'].loc[i] + \
                           self._seqtab['suffix'].loc[i]
                else:
                    seq += self._seqtab['prefix'].loc[i] + self._seqtab['nt'].loc[i] + \
                           self._seqtab['suffix'].loc[i]
            #print(seq)
        return oligoNASequence(seq)

    def reset_modifications(self):
        self.modifications.reset_modif(self._seqtab)

    def getMolecularFormula(self):
        f = ''
        if not self.is_mixed:
            for n in self.seq:
                f += self.dnaDB(n).seqformula
            if len(self.seq) > 1:
                num = len(self.seq) - 1
                f += f'H{num + 2}P{num}O{2*num}'
            return self.modifications._get_mod_formula(EmpericalFormula(f)())
        else:
            return f

    def getMonoMass(self):
        if not self.is_mixed:
            return EmpericalFormula(self.molecularFormula).getMonoWeight()
        else:
            return 0

    def getAvgMass(self):
        if not self.is_mixed:
            return EmpericalFormula(self.molecularFormula).getAverageWeight()
        else:
            return 0

    def getExtinction(self):
        base_extinction = dna.get_simple_ssdna_extinction(''.join(list(self._seqtab['nt'])), dna.get_extinction_dict())
        for key in self.modifications.ex_mod.keys():
            base_extinction += self.modifications.exModDB.get_mod_properties(key)['ext_cf'] * \
                               self.modifications.ex_mod[key]
        return base_extinction

    def getSeqLength(self):
        if not self._seqtab.empty:
            return self._seqtab.shape[0]
        else:
            return 0

    def getSeqTabDF(self):
        return self._seqtab


def test():
    olig1 = oligoNASequence('+a+c*grT*mTTuUrurU')
    print(olig1.seq)
    print(olig1.modifications.mod_list)
    print(olig1.getMolecularFormula())
    print(olig1.getAvgMass())

    sequence = '+A*AAUut+tcrgmG*'

    olig2 = oligoNASequence(sequence)
    print(olig2.seq)
    print(olig2.modifications.mod_list)
    print(olig2.getMolecularFormula())
    #print(olig2.getMonoMass())
    print(olig2.getAvgMass())

    seq = dna.oligoSeq(sequence)
    print(seq.getBruttoFormula())
    print(seq.getMolMass())

    print(seq.getMolMass() - olig2.getAvgMass())

    o1 = oligoNASequence('GTA/iFluorT/G')
    print(o1.getMolecularFormula())
    print(o1.getAvgMass())
    print(o1.modifications.ex_mod)

    o2 = oligoNASequence('GTAG')
    print(o2.getMolecularFormula())
    print(o2.getAvgMass())
    print(o2.modifications.ex_mod)

    print(o1.getAvgMass() - o2.getAvgMass())

def test2():
    o1 = oligoNASequence('+G*TrCmA+TTTGGG{iFluorT}+CC*++AA*')

    print(o1._seqtab)
    print(o1.sequence)
    print(o1.init_seq)
    print(o1.seq)

    print(o1.getAvgMass())
    print(o1.modifications.mod_list)
    o1.reset_modifications()
    print(o1.modifications.mod_list)
    print(o1.getAvgMass())

def test3():
    o1 = oligoNASequence('AG+TrCATTT/iFluorT/GGGC')
    print(o1())
    for i in range(1, o1.size()):
        p = o1.getPrefix(i)
        s = o1.getSuffix(i)
        print(p(), s(), p.getAvgMass(), s.getAvgMass())

def test4():
    o1 = oligoNASequence('CGTCTAG[+m]CCATGG[+m]CGTTA')
    print(o1.getAvgMass())
    print(o1.sequence)
    print(o1.getMolecularFormula())

    o2 = oligoNASequence('CGTCTAGCCATGGCGTTA')
    print(o2.getAvgMass())
    print(o2.sequence)
    print(o2.getMolecularFormula())

    o3 = oligoNASequence('CGTCT{C2H2O}AGCC{C2H2O}ATGGCGTTA')
    print(o3.getAvgMass())
    print(o3.sequence)
    print(o3.getMolecularFormula())

    o4 = oligoNASequence('ATGC')
    print(o4.getAvgMass())
    print(o4.sequence)
    print(o4.getMolecularFormula())

    o4 = oligoNASequence('ATG*C')
    print(o4.getAvgMass())
    print(o4.sequence)
    print(o4.getMolecularFormula())

    o5 = oligoNASequence('AT[Se;]GC')
    print(o5.getAvgMass())
    print(o5.sequence)
    print(o5.getMolecularFormula())

def test5():
    o1 = oligoNASequence('GGAAGGATCTGTATCAAGCCGT')
    o2 = oligoNASequence('GGAAGG*ATCTGTATCAAGCCGT')
    o3 = oligoNASequence('GGAAGGA{S|O}TC{S|O}TG{S|O}TATCAAGCCGT')
    o4 = oligoNASequence('GAGCGG')

    #o5 = oligoNASequence('GCATGGTCT{C5N3H10PO}CCCGUAGUGAGUrGrUrUrUrUrArGrUrGrCrUrArGrA')
    o5 = oligoNASequence('GCATGGTCTCCCGUAGUGAGUrGrUrUrUrUrArGrUrGrCrUrArGrA')
    o6 = oligoNASequence('rGrCrA rUrGrG rUrCrU rCrCrC rGrUrA rGrUrG rArGrU rGrUrU rUrUrArGrUrGrCrUrArGrA')

    print(o1.getAvgMass())
    print(o2.getAvgMass())
    print(o3.getAvgMass())

    print(o4.getAvgMass())

    print(o5.getAvgMass())# - 11080)

    print(o6.getAvgMass())


    #print(EmpericalFormula('C10N5OH10').formula)

    #print(EmpericalFormula('C10NO15H10N8C18').formula)

    #print(mm.Formula('C5N3H10PO').mass)

"""
def test6():
    FII = 'CATTGAGGCTCGCTGAGAG'
    oFII = oligoNASequence(FII)
    print(oFII.getAvgMass())

    print('SIMA + seq', 7182 - 759 - oFII.getAvgMass())

    print(6424 - oFII.getAvgMass())
    print(7182 - oFII.getAvgMass())

    BHQ1 = EmpericalFormula('C21H18N6O3C4O2H9PO2')
    print('BHQ', mm.Formula(BHQ1.formula).mass)
    print('BHQf', BHQ1.formula)

    Ph = EmpericalFormula('H2PO3')
    print('Ph', mm.Formula(Ph.formula).mass)
    print('Ph + 759', mm.Formula(Ph.formula).mass + 759)

    SIMA = EmpericalFormula('C42H68N3O9')
    print('SIMA', mm.Formula(SIMA.formula).mass)

    FV = oligoNASequence('CCTGGACAGGCGAGGAATACAG')

    FAM = EmpericalFormula('C30O8NH36')
    print('FAM', mm.Formula(FAM.formula).mass)
    print('7910 - oligomass - FAM', 7910 - FV.getAvgMass() - mm.Formula(FAM.formula).mass)
    print('FAM oligos BHQ', FV.getAvgMass() + 554 + 566 - 28)
    print('oligos BHQ', FV.getAvgMass() + 554)

    FV_ = oligoNASequence('{C30O8NH36}CCTGGACAGGCGAGGAATACA{C25H27N6O7P}G')
    print(FV_.getAvgMass())

    FII_ = oligoNASequence('{C42H68N3O9}CATTGAGGCTCGCTGAGA{C25H27N6O7P}G')
    print(FII_.getAvgMass())
"""
def test7():
    f = EmpericalFormula('CP4H11O18Cl4S10Cd11NiN4O')
    print(f)
    print(f.dict_formula)

    f = EmpericalFormula('COPFLi')
    print(f)
    print(f.dict_formula)

    f = EmpericalFormula('K1Kr2')
    print(f)
    print(f.dict_formula)

    f = EmpericalFormula('KKr2KKrOOO3Li1Li2Li')
    print(f)
    print(f.dict_formula)
"""
def test8():

    import random

    elems = list(Elements().elements.keys())

    N = 500
    for tests in range(N):
        mol = ''
        for i in range(random.randint(1, 20)):
            index = random.randint(0, len(elems) - 1)
            mol += elems[index]
            count = random.randint(1, 101)
            mol += str(count) if count > 1 else ''

        ref_mass = mm.Formula(mol).mass
        mass = EmpericalFormula(mol).getAverageWeight()
        #print(mass, ref_mass)
        assert abs(mass - ref_mass) < 0.1
    print('Test Done')
    print(f'500 random molecules was tried')


    #f = EmpericalFormula('C')
    #print(f)
    #print('Avg mass', f.getAverageWeight())
    #print('Mono mass', f.getMonoWeight())

    #print(mm.Formula(f()).mass)
"""

def test9():
    o1 = oligoNASequence('GGAA{C18Cl2}GGATCTGTATCAAGCCGT')
    o2 = oligoNASequence('GGAAGGATCTGTATCAAGCCGT')
    print(o1.molecularFormula)
    print(o2.molecularFormula)

    print((EmpericalFormula('C2H8')*2)())

    print(oligoNASequence('GGAAGG+AT{O|CO2}CTGTATCAAGCCGT').getAvgMass())
    print(oligoNASequence('GGAAGGATC*TG*T*ATCAAGCCGT').getAvgMass())
    print(oligoNASequence('/56-FAM/GGA AGG ATC TGT ATC AAG CCG /3BHQ_1/ T').getAvgMass())
    print(oligoNASequence('/56-FAM/GGA AGG ATC TGT ATC AAG CCG T').getAvgMass())
    print(oligoNASequence('GGA AGG ATC TGT ATC AAG CCG /3BHQ_1/ T').getAvgMass())
    print(oligoNASequence('/SIMA/ GGA AGG ATC TGT ATC AAG CCG /3BHQ_1/ T').getAvgMass())

def test9():
    ext = dna.get_simple_ssdna_extinction("TTT TTT TTT TTT TTT TTT", dna.get_extinction_dict())
    print(ext)
    print(49*1e6 / ext)

    o1 = oligoNASequence('{6FAM}TTT TTT TTT TTT TTT TT{BHQ1}T')
    print(o1.getExtinction())

    o1 = oligoNASequence('{C30O8NH35}CCTGGACAGGCGAGGAATACA{C25H27N6O7P}G')
    print(o1.getExtinction())

def test10():
    o1 = oligoNASequence('TTCTGACCTGAAGGCTCTGCGC{BHQ2}G')
    print(o1.getExtinction())
    print(o1.getAvgMass())

    o1 = oligoNASequence('TTCTGACCTGAAGGCTCTGCGC{BHQ1}G')
    print(o1.getExtinction())
    print(o1.getAvgMass())

def test11():
    o1 = oligoNASequence('TTCTGACCTGAAGGCTCTGCGC{BHQ1}G')
    for i in range(1, o1.size()):
        print(f'{o1.size() - i}')
        print(o1.get_3_mod_move(i).sequence)

def test12():
    o1 = oligoNASequence('TTCTGACC+T*GAAGGCTCTGCGC{BHQ1}G')
    print(o1.getSeqTabDF())


if __name__ == '__main__':
    test12()