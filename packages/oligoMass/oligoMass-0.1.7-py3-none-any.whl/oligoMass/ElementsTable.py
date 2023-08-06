
from collections import namedtuple

class Elements():
    def __init__(self):
        elem = namedtuple('Element', 'name number mass isotopes')
        Isotope = namedtuple('Isotope', 'mass freq nuclons')

        self.elements = {}
        self.elements['H'] = elem('Hydrogen', 1, 1.007941,
                                  {1: Isotope(1.00782503223, 0.999885, 1), 2: Isotope(2.01410177812, 0.000115, 2)})
        self.elements['He'] = elem('Helium', 2, 4.002602,
                                   {3: Isotope(3.0160293201, 1.34e-06, 3), 4: Isotope(4.00260325413, 0.99999866, 4)})
        self.elements['Li'] = elem('Lithium', 3, 6.94,
                                   {6: Isotope(6.0151228874, 0.0759, 6), 7: Isotope(7.0160034366, 0.9241, 7)})
        self.elements['Be'] = elem('Beryllium', 4, 9.0121831, {9: Isotope(9.012183065, 1.0, 9)})
        self.elements['B'] = elem('Boron', 5, 10.811,
                                  {10: Isotope(10.01293695, 0.199, 10), 11: Isotope(11.00930536, 0.801, 11)})
        self.elements['C'] = elem('Carbon', 6, 12.01074,
                                  {12: Isotope(12.0, 0.9893, 12), 13: Isotope(13.00335483507, 0.0107, 13)})
        self.elements['N'] = elem('Nitrogen', 7, 14.006703,
                                  {14: Isotope(14.00307400443, 0.99636, 14), 15: Isotope(15.00010889888, 0.00364, 15)})
        self.elements['O'] = elem('Oxygen', 8, 15.999405,
                                  {16: Isotope(15.99491461957, 0.99757, 16), 17: Isotope(16.9991317565, 0.00038, 17),
                                   18: Isotope(17.99915961286, 0.00205, 18)})
        self.elements['F'] = elem('Fluorine', 9, 18.998403163, {19: Isotope(18.99840316273, 1.0, 19)})
        self.elements['Ne'] = elem('Neon', 10, 20.1797,
                                   {20: Isotope(19.9924401762, 0.9048, 20), 21: Isotope(20.993846685, 0.0027, 21),
                                    22: Isotope(21.991385114, 0.0925, 22)})
        self.elements['Na'] = elem('Sodium', 11, 22.98976928, {23: Isotope(22.989769282, 1.0, 23)})
        self.elements['Mg'] = elem('Magnesium', 12, 24.3051,
                                   {24: Isotope(23.985041697, 0.7899, 24), 25: Isotope(24.985836976, 0.1, 25),
                                    26: Isotope(25.982592968, 0.1101, 26)})
        self.elements['Al'] = elem('Aluminium', 13, 26.9815385, {27: Isotope(26.98153853, 1.0, 27)})
        self.elements['Si'] = elem('Silicon', 14, 28.0855,
                                   {28: Isotope(27.97692653465, 0.92223, 28), 29: Isotope(28.9764946649, 0.04685, 29),
                                    30: Isotope(29.973770136, 0.03092, 30)})
        self.elements['P'] = elem('Phosphorus', 15, 30.973761998, {31: Isotope(30.97376199842, 1.0, 31)})
        self.elements['S'] = elem('Sulfur', 16, 32.0648,
                                  {32: Isotope(31.9720711744, 0.9499, 32), 33: Isotope(32.9714589098, 0.0075, 33),
                                   34: Isotope(33.967867004, 0.0425, 34), 36: Isotope(35.96708071, 0.0001, 36)})
        self.elements['Cl'] = elem('Chlorine', 17, 35.4529,
                                   {35: Isotope(34.968852682, 0.7576, 35), 37: Isotope(36.965902602, 0.2424, 37)})
        self.elements['Ar'] = elem('Argon', 18, 39.948,
                                   {36: Isotope(35.967545105, 0.003336, 36), 38: Isotope(37.96273211, 0.000629, 38),
                                    40: Isotope(39.9623831237, 0.996035, 40)})
        self.elements['K'] = elem('Potassium', 19, 39.0983,
                                  {39: Isotope(38.9637064864, 0.932581, 39), 40: Isotope(39.963998166, 0.000117, 40),
                                   41: Isotope(40.9618252579, 0.067302, 41)})
        self.elements['Ca'] = elem('Calcium', 20, 40.078,
                                   {40: Isotope(39.962590863, 0.96941, 40), 42: Isotope(41.95861783, 0.00647, 42),
                                    43: Isotope(42.95876644, 0.00135, 43), 44: Isotope(43.95548156, 0.02086, 44),
                                    46: Isotope(45.953689, 4e-05, 46), 48: Isotope(47.95252276, 0.00187, 48)})
        self.elements['Sc'] = elem('Scandium', 21, 44.955908, {45: Isotope(44.95590828, 1.0, 45)})
        self.elements['Ti'] = elem('Titanium', 22, 47.867,
                                   {46: Isotope(45.95262772, 0.0825, 46), 47: Isotope(46.95175879, 0.0744, 47),
                                    48: Isotope(47.94794198, 0.7372, 48), 49: Isotope(48.94786568, 0.0541, 49),
                                    50: Isotope(49.94478689, 0.0518, 50)})
        self.elements['V'] = elem('Vanadium', 23, 50.9415,
                                  {50: Isotope(49.94715601, 0.0025, 50), 51: Isotope(50.94395704, 0.9975, 51)})
        self.elements['Cr'] = elem('Chromium', 24, 51.9961,
                                   {50: Isotope(49.94604183, 0.04345, 50), 52: Isotope(51.94050623, 0.83789, 52),
                                    53: Isotope(52.94064815, 0.09501, 53), 54: Isotope(53.93887916, 0.02365, 54)})
        self.elements['Mn'] = elem('Manganese', 25, 54.938044, {55: Isotope(54.93804391, 1.0, 55)})
        self.elements['Fe'] = elem('Iron', 26, 55.845,
                                   {54: Isotope(53.93960899, 0.05845, 54), 56: Isotope(55.93493633, 0.91754, 56),
                                    57: Isotope(56.93539284, 0.02119, 57), 58: Isotope(57.93327443, 0.00282, 58)})
        self.elements['Co'] = elem('Cobalt', 27, 58.933194, {59: Isotope(58.93319429, 1.0, 59)})
        self.elements['Ni'] = elem('Nickel', 28, 58.6934,
                                   {58: Isotope(57.93534241, 0.68077, 58), 60: Isotope(59.93078588, 0.26223, 60),
                                    61: Isotope(60.93105557, 0.011399, 61), 62: Isotope(61.92834537, 0.036346, 62),
                                    64: Isotope(63.92796682, 0.009255, 64)})
        self.elements['Cu'] = elem('Copper', 29, 63.546,
                                   {63: Isotope(62.92959772, 0.6915, 63), 65: Isotope(64.9277897, 0.3085, 65)})
        self.elements['Zn'] = elem('Zinc', 30, 65.38,
                                   {64: Isotope(63.92914201, 0.4917, 64), 66: Isotope(65.92603381, 0.2773, 66),
                                    67: Isotope(66.92712775, 0.0404, 67), 68: Isotope(67.92484455, 0.1845, 68),
                                    70: Isotope(69.9253192, 0.0061, 70)})
        self.elements['Ga'] = elem('Gallium', 31, 69.723,
                                   {69: Isotope(68.9255735, 0.60108, 69), 71: Isotope(70.92470258, 0.39892, 71)})
        self.elements['Ge'] = elem('Germanium', 32, 72.63,
                                   {70: Isotope(69.92424875, 0.2057, 70), 72: Isotope(71.922075826, 0.2745, 72),
                                    73: Isotope(72.923458956, 0.0775, 73), 74: Isotope(73.921177761, 0.365, 74),
                                    76: Isotope(75.921402726, 0.0773, 76)})
        self.elements['As'] = elem('Arsenic', 33, 74.921595, {75: Isotope(74.92159457, 1.0, 75)})
        self.elements['Se'] = elem('Selenium', 34, 78.971,
                                   {74: Isotope(73.922475934, 0.0089, 74), 76: Isotope(75.919213704, 0.0937, 76),
                                    77: Isotope(76.919914154, 0.0763, 77), 78: Isotope(77.91730928, 0.2377, 78),
                                    80: Isotope(79.9165218, 0.4961, 80), 82: Isotope(81.9166995, 0.0873, 82)})
        self.elements['Br'] = elem('Bromine', 35, 79.9035,
                                   {79: Isotope(78.9183376, 0.5069, 79), 81: Isotope(80.9162897, 0.4931, 81)})
        self.elements['Kr'] = elem('Krypton', 36, 83.798,
                                   {78: Isotope(77.92036494, 0.00355, 78), 80: Isotope(79.91637808, 0.02286, 80),
                                    82: Isotope(81.91348273, 0.11593, 82), 83: Isotope(82.91412716, 0.115, 83),
                                    84: Isotope(83.9114977282, 0.56987, 84), 86: Isotope(85.9106106269, 0.17279, 86)})
        self.elements['Rb'] = elem('Rubidium', 37, 85.4678,
                                   {85: Isotope(84.9117897379, 0.7217, 85), 87: Isotope(86.909180531, 0.2783, 87)})
        self.elements['Sr'] = elem('Strontium', 38, 87.62,
                                   {84: Isotope(83.9134191, 0.0056, 84), 86: Isotope(85.9092606, 0.0986, 86),
                                    87: Isotope(86.9088775, 0.07, 87), 88: Isotope(87.9056125, 0.8258, 88)})
        self.elements['Y'] = elem('Yttrium', 39, 88.90584, {89: Isotope(88.9058403, 1.0, 89)})
        self.elements['Zr'] = elem('Zirconium', 40, 91.224,
                                   {90: Isotope(89.9046977, 0.5145, 90), 91: Isotope(90.9056396, 0.1122, 91),
                                    92: Isotope(91.9050347, 0.1715, 92), 94: Isotope(93.9063108, 0.1738, 94),
                                    96: Isotope(95.9082714, 0.028, 96)})
        self.elements['Nb'] = elem('Niobium', 41, 92.90637, {93: Isotope(92.906373, 1.0, 93)})
        self.elements['Mo'] = elem('Molybdenum', 42, 95.95,
                                   {92: Isotope(91.90680796, 0.1453, 92), 94: Isotope(93.9050849, 0.0915, 94),
                                    95: Isotope(94.90583877, 0.1584, 95), 96: Isotope(95.90467612, 0.1667, 96),
                                    97: Isotope(96.90601812, 0.096, 97), 98: Isotope(97.90540482, 0.2439, 98),
                                    100: Isotope(99.9074718, 0.0982, 100)})
        self.elements['Tc'] = elem('Technetium', 43, 97.9072, {98: Isotope(97.9072124, 1.0, 98)})
        self.elements['Ru'] = elem('Ruthenium', 44, 101.07,
                                   {96: Isotope(95.90759025, 0.0554, 96), 98: Isotope(97.9052868, 0.0187, 98),
                                    99: Isotope(98.9059341, 0.1276, 99), 100: Isotope(99.9042143, 0.126, 100),
                                    101: Isotope(100.9055769, 0.1706, 101), 102: Isotope(101.9043441, 0.3155, 102),
                                    104: Isotope(103.9054275, 0.1862, 104)})
        self.elements['Rh'] = elem('Rhodium', 45, 102.9055, {103: Isotope(102.905498, 1.0, 103)})
        self.elements['Pd'] = elem('Palladium', 46, 106.42,
                                   {102: Isotope(101.9056022, 0.0102, 102), 104: Isotope(103.9040305, 0.1114, 104),
                                    105: Isotope(104.9050796, 0.2233, 105), 106: Isotope(105.9034804, 0.2733, 106),
                                    108: Isotope(107.9038916, 0.2646, 108), 110: Isotope(109.9051722, 0.1172, 110)})
        self.elements['Ag'] = elem('Silver', 47, 107.8682,
                                   {107: Isotope(106.9050916, 0.51839, 107), 109: Isotope(108.9047553, 0.48161, 109)})
        self.elements['Cd'] = elem('Cadmium', 48, 112.414,
                                   {106: Isotope(105.9064599, 0.0125, 106), 108: Isotope(107.9041834, 0.0089, 108),
                                    110: Isotope(109.90300661, 0.1249, 110), 111: Isotope(110.90418287, 0.128, 111),
                                    112: Isotope(111.90276287, 0.2413, 112), 113: Isotope(112.90440813, 0.1222, 113),
                                    114: Isotope(113.90336509, 0.2873, 114), 116: Isotope(115.90476315, 0.0749, 116)})
        self.elements['In'] = elem('Indium', 49, 114.818,
                                   {113: Isotope(112.90406184, 0.0429, 113), 115: Isotope(114.903878776, 0.9571, 115)})
        self.elements['Sn'] = elem('Tin', 50, 118.71,
                                   {112: Isotope(111.90482387, 0.0097, 112), 114: Isotope(113.9027827, 0.0066, 114),
                                    115: Isotope(114.903344699, 0.0034, 115), 116: Isotope(115.9017428, 0.1454, 116),
                                    117: Isotope(116.90295398, 0.0768, 117), 118: Isotope(117.90160657, 0.2422, 118),
                                    119: Isotope(118.90331117, 0.0859, 119), 120: Isotope(119.90220163, 0.3258, 120),
                                    122: Isotope(121.9034438, 0.0463, 122), 124: Isotope(123.9052766, 0.0579, 124)})
        self.elements['Sb'] = elem('Antimony', 51, 121.76,
                                   {121: Isotope(120.903812, 0.5721, 121), 123: Isotope(122.9042132, 0.4279, 123)})
        self.elements['Te'] = elem('Tellurium', 52, 127.6,
                                   {120: Isotope(119.9040593, 0.0009, 120), 122: Isotope(121.9030435, 0.0255, 122),
                                    123: Isotope(122.9042698, 0.0089, 123), 124: Isotope(123.9028171, 0.0474, 124),
                                    125: Isotope(124.9044299, 0.0707, 125), 126: Isotope(125.9033109, 0.1884, 126),
                                    128: Isotope(127.90446128, 0.3174, 128), 130: Isotope(129.906222748, 0.3408, 130)})
        self.elements['I'] = elem('Iodine', 53, 126.90447, {127: Isotope(126.9044719, 1.0, 127)})
        self.elements['Xe'] = elem('Xenon', 54, 131.293,
                                   {124: Isotope(123.905892, 0.000952, 124), 126: Isotope(125.9042983, 0.00089, 126),
                                    128: Isotope(127.903531, 0.019102, 128),
                                    129: Isotope(128.9047808611, 0.264006, 129),
                                    130: Isotope(129.903509349, 0.04071, 130),
                                    131: Isotope(130.90508406, 0.212324, 131),
                                    132: Isotope(131.9041550856, 0.269086, 132),
                                    134: Isotope(133.90539466, 0.104357, 134),
                                    136: Isotope(135.907214484, 0.088573, 136)})
        self.elements['Cs'] = elem('Caesium', 55, 132.90545196, {133: Isotope(132.905451961, 1.0, 133)})
        self.elements['Ba'] = elem('Barium', 56, 137.327,
                                   {130: Isotope(129.9063207, 0.00106, 130), 132: Isotope(131.9050611, 0.00101, 132),
                                    134: Isotope(133.90450818, 0.02417, 134), 135: Isotope(134.90568838, 0.06592, 135),
                                    136: Isotope(135.90457573, 0.07854, 136), 137: Isotope(136.90582714, 0.11232, 137),
                                    138: Isotope(137.905247, 0.71698, 138)})
        self.elements['La'] = elem('Lanthanum', 57, 138.90547, {138: Isotope(137.9071149, 0.0008881, 138),
                                                                139: Isotope(138.9063563, 0.9991119, 139)})
        self.elements['Ce'] = elem('Cerium', 58, 140.116,
                                   {136: Isotope(135.90712921, 0.00185, 136), 138: Isotope(137.905991, 0.00251, 138),
                                    140: Isotope(139.9054431, 0.8845, 140), 142: Isotope(141.9092504, 0.11114, 142)})
        self.elements['Pr'] = elem('Praseodymium', 59, 140.90766, {141: Isotope(140.9076576, 1.0, 141)})
        self.elements['Nd'] = elem('Neodymium', 60, 144.242,
                                   {142: Isotope(141.907729, 0.27152, 142), 143: Isotope(142.90982, 0.12174, 143),
                                    144: Isotope(143.910093, 0.23798, 144), 145: Isotope(144.9125793, 0.08293, 145),
                                    146: Isotope(145.9131226, 0.17189, 146), 148: Isotope(147.9168993, 0.05756, 148),
                                    150: Isotope(149.9209022, 0.05638, 150)})
        self.elements['Pm'] = elem('Promethium', 61, 144.9128, {145: Isotope(144.9127559, 1.0, 145)})
        self.elements['Sm'] = elem('Samarium', 62, 150.36,
                                   {144: Isotope(143.9120065, 0.0307, 144), 147: Isotope(146.9149044, 0.1499, 147),
                                    148: Isotope(147.9148292, 0.1124, 148), 149: Isotope(148.9171921, 0.1382, 149),
                                    150: Isotope(149.9172829, 0.0738, 150), 152: Isotope(151.9197397, 0.2675, 152),
                                    154: Isotope(153.9222169, 0.2275, 154)})
        self.elements['Eu'] = elem('Europium', 63, 151.964,
                                   {151: Isotope(150.9198578, 0.4781, 151), 153: Isotope(152.921238, 0.5219, 153)})
        self.elements['Gd'] = elem('Gadolinium', 64, 157.25,
                                   {152: Isotope(151.9197995, 0.002, 152), 154: Isotope(153.9208741, 0.0218, 154),
                                    155: Isotope(154.9226305, 0.148, 155), 156: Isotope(155.9221312, 0.2047, 156),
                                    157: Isotope(156.9239686, 0.1565, 157), 158: Isotope(157.9241123, 0.2484, 158),
                                    160: Isotope(159.9270624, 0.2186, 160)})
        self.elements['Tb'] = elem('Terbium', 65, 158.92535, {159: Isotope(158.9253547, 1.0, 159)})
        self.elements['Dy'] = elem('Dysprosium', 66, 162.5,
                                   {156: Isotope(155.9242847, 0.00056, 156), 158: Isotope(157.9244159, 0.00095, 158),
                                    160: Isotope(159.9252046, 0.02329, 160), 161: Isotope(160.9269405, 0.18889, 161),
                                    162: Isotope(161.9268056, 0.25475, 162), 163: Isotope(162.9287383, 0.24896, 163),
                                    164: Isotope(163.9291819, 0.2826, 164)})
        self.elements['Ho'] = elem('Holmium', 67, 164.93033, {165: Isotope(164.9303288, 1.0, 165)})
        self.elements['Er'] = elem('Erbium', 68, 167.259,
                                   {162: Isotope(161.9287884, 0.00139, 162), 164: Isotope(163.9292088, 0.01601, 164),
                                    166: Isotope(165.9302995, 0.33503, 166), 167: Isotope(166.9320546, 0.22869, 167),
                                    168: Isotope(167.9323767, 0.26978, 168), 170: Isotope(169.9354702, 0.1491, 170)})
        self.elements['Tm'] = elem('Thulium', 69, 168.93422, {169: Isotope(168.9342179, 1.0, 169)})
        self.elements['Yb'] = elem('Ytterbium', 70, 173.054,
                                   {168: Isotope(167.9338896, 0.00123, 168), 170: Isotope(169.9347664, 0.02982, 170),
                                    171: Isotope(170.9363302, 0.1409, 171), 172: Isotope(171.9363859, 0.2168, 172),
                                    173: Isotope(172.9382151, 0.16103, 173), 174: Isotope(173.9388664, 0.32026, 174),
                                    176: Isotope(175.9425764, 0.12996, 176)})
        self.elements['Lu'] = elem('Lutetium', 71, 174.9668,
                                   {175: Isotope(174.9407752, 0.97401, 175), 176: Isotope(175.9426897, 0.02599, 176)})
        self.elements['Hf'] = elem('Hafnium', 72, 178.49,
                                   {174: Isotope(173.9400461, 0.0016, 174), 176: Isotope(175.9414076, 0.0526, 176),
                                    177: Isotope(176.9432277, 0.186, 177), 178: Isotope(177.9437058, 0.2728, 178),
                                    179: Isotope(178.9458232, 0.1362, 179), 180: Isotope(179.946557, 0.3508, 180)})
        self.elements['Ta'] = elem('Tantalum', 73, 180.94788, {180: Isotope(179.9474648, 0.0001201, 180),
                                                               181: Isotope(180.9479958, 0.9998799, 181)})
        self.elements['W'] = elem('Tungsten', 74, 183.84,
                                  {180: Isotope(179.9467108, 0.0012, 180), 182: Isotope(181.94820394, 0.265, 182),
                                   183: Isotope(182.95022275, 0.1431, 183), 184: Isotope(183.95093092, 0.3064, 184),
                                   186: Isotope(185.9543628, 0.2843, 186)})
        self.elements['Re'] = elem('Rhenium', 75, 186.207,
                                   {185: Isotope(184.9529545, 0.374, 185), 187: Isotope(186.9557501, 0.626, 187)})
        self.elements['Os'] = elem('Osmium', 76, 190.23,
                                   {184: Isotope(183.9524885, 0.0002, 184), 186: Isotope(185.953835, 0.0159, 186),
                                    187: Isotope(186.9557474, 0.0196, 187), 188: Isotope(187.9558352, 0.1324, 188),
                                    189: Isotope(188.9581442, 0.1615, 189), 190: Isotope(189.9584437, 0.2626, 190),
                                    192: Isotope(191.961477, 0.4078, 192)})
        self.elements['Ir'] = elem('Iridium', 77, 192.217,
                                   {191: Isotope(190.9605893, 0.373, 191), 193: Isotope(192.9629216, 0.627, 193)})
        self.elements['Pt'] = elem('Platinum', 78, 195.084,
                                   {190: Isotope(189.9599297, 0.00012, 190), 192: Isotope(191.9610387, 0.00782, 192),
                                    194: Isotope(193.9626809, 0.3286, 194), 195: Isotope(194.9647917, 0.3378, 195),
                                    196: Isotope(195.96495209, 0.2521, 196), 198: Isotope(197.9678949, 0.07356, 198)})
        self.elements['Au'] = elem('Gold', 79, 196.966569, {197: Isotope(196.96656879, 1.0, 197)})
        self.elements['Hg'] = elem('Mercury', 80, 200.592,
                                   {196: Isotope(195.9658326, 0.0015, 196), 198: Isotope(197.9667686, 0.0997, 198),
                                    199: Isotope(198.96828064, 0.1687, 199), 200: Isotope(199.96832659, 0.231, 200),
                                    201: Isotope(200.97030284, 0.1318, 201), 202: Isotope(201.9706434, 0.2986, 202),
                                    204: Isotope(203.97349398, 0.0687, 204)})
        self.elements['Tl'] = elem('Thallium', 81, 204.3834,
                                   {203: Isotope(202.9723446, 0.2952, 203), 205: Isotope(204.9744278, 0.7048, 205)})
        self.elements['Pb'] = elem('Lead', 82, 207.2,
                                   {204: Isotope(203.973044, 0.014, 204), 206: Isotope(205.9744657, 0.241, 206),
                                    207: Isotope(206.9758973, 0.221, 207), 208: Isotope(207.9766525, 0.524, 208)})
        self.elements['Bi'] = elem('Bismuth', 83, 208.9804, {209: Isotope(208.9803991, 1.0, 209)})
        self.elements['Po'] = elem('Polonium', 84, 208.9824, {209: Isotope(208.9824308, 1.0, 209)})
        self.elements['At'] = elem('Astatine', 85, 209.9871, {210: Isotope(209.9871479, 1.0, 210)})
        self.elements['Rn'] = elem('Radon', 86, 222.0176, {222: Isotope(222.0175782, 1.0, 222)})
        self.elements['Fr'] = elem('Francium', 87, 223.0197, {223: Isotope(223.019736, 1.0, 223)})
        self.elements['Ra'] = elem('Radium', 88, 226.0254, {226: Isotope(226.0254103, 1.0, 226)})
        self.elements['Ac'] = elem('Actinium', 89, 227.0278, {227: Isotope(227.0277523, 1.0, 227)})
        self.elements['Th'] = elem('Thorium', 90, 232.0377, {232: Isotope(232.0380558, 1.0, 232)})
        self.elements['Pa'] = elem('Protactinium', 91, 231.03588, {231: Isotope(231.0358842, 1.0, 231)})
        self.elements['U'] = elem('Uranium', 92, 238.02891,
                                  {234: Isotope(234.0409523, 5.4e-05, 234), 235: Isotope(235.0439301, 0.007204, 235),
                                   238: Isotope(238.0507884, 0.992742, 238)})
        self.elements['Np'] = elem('Neptunium', 93, 237.0482, {237: Isotope(237.0481736, 1.0, 237)})
        self.elements['Pu'] = elem('Plutonium', 94, 244.0642, {244: Isotope(244.0642053, 1.0, 244)})
        self.elements['Am'] = elem('Americium', 95, 243.0614, {243: Isotope(243.0613813, 1.0, 243)})
        self.elements['Cm'] = elem('Curium', 96, 247.0704, {247: Isotope(247.0703541, 1.0, 247)})
        self.elements['Bk'] = elem('Berkelium', 97, 247.0703, {247: Isotope(247.0703073, 1.0, 247)})
        self.elements['Cf'] = elem('Californium', 98, 251.0796, {251: Isotope(251.0795886, 1.0, 251)})
        self.elements['Es'] = elem('Einsteinium', 99, 252.083, {252: Isotope(252.08298, 1.0, 252)})
        self.elements['Fm'] = elem('Fermium', 100, 257.0951, {257: Isotope(257.0951061, 1.0, 257)})
        self.elements['Md'] = elem('Mendelevium', 101, 258.0984, {258: Isotope(258.0984315, 1.0, 258)})
        self.elements['No'] = elem('Nobelium', 102, 259.101, {259: Isotope(259.10103, 1.0, 259)})
        self.elements['Lr'] = elem('Lawrencium', 103, 262.1096, {262: Isotope(262.10961, 1.0, 262)})
        self.elements['Rf'] = elem('Rutherfordium', 104, 267.1218, {267: Isotope(267.12179, 1.0, 267)})
        self.elements['Db'] = elem('Dubnium', 105, 268.1257, {268: Isotope(268.12567, 1.0, 268)})
        self.elements['Sg'] = elem('Seaborgium', 106, 271.1339, {271: Isotope(271.13393, 1.0, 271)})
        self.elements['Bh'] = elem('Bohrium', 107, 272.1383, {272: Isotope(272.13826, 1.0, 272)})
        self.elements['Hs'] = elem('Hassium', 108, 270.1343, {270: Isotope(270.13429, 1.0, 270)})
        self.elements['Mt'] = elem('Meitnerium', 109, 276.1516, {276: Isotope(276.15159, 1.0, 276)})

    def __call__(self, symbol):
        return self.elements[symbol]


def test2():

    print(Elements()('C'))

if __name__ == '__main__':
    test2()