class K_isp_ryad:
    def __init__(self, p1, p2, m):
        '''
        p1 - удельное сопротивление верхнего слоя грунта, Ом*м;
        p2 - удельное сопротивление нижнего слоя грунта, Ом*м;
        m - число вертикальных заземлителей, шт. [2, 14];
        h - толщина(мощность) верхнего слоя грунта, м.;
        l_vert - длинна вертикального заземлителя, м.;
        t - глубина укладки горизонтального заземлителя, м.;
        a_middle - среднее расстояние между вертикальными заземлителями, м.;
        '''
        self.m = m
        self.p1 = p1
        self.p2 = p2
        self.p = self.p1 / self.p2

    def get_K_isp(self) -> tuple:
        '''См. стр. 238.'''
        if self.p > 10:
            B_1 = 0.88 * 10 ** 0.0645
            b_1 = 0.242 * 10 ** -0.083
            return round(B_1 / (self.m ** b_1), 3)
        else:
            B_1 = 0.88 * self.p ** 0.0645
            b_1 = 0.242 * self.p ** -0.083
            return round(B_1 / (self.m ** b_1), 3)



class K_isp_contur:
    tabl_05 = {
        2: [0.490, 0.483, 0.524, 0.504, 0.484, 0.512, 0.528, 0.500, 0.518],
        4: [0.436, 0.438, 0.476, 0.439, 0.439, 0.466, 0.454, 0.443, 0.466],
        6: [0.407, 0.385, 0.461, 0.396, 0.389, 0.442, 0.380, 0.388, 0.436],
        8: [0.357, 0.390, 0.454, 0.367, 0.375, 0.432, 0.350, 0.370, 0.419],
        12: [0.322, 0.370, 0.444, 0.310, 0.349, 0.419, 0.304, 0.335, 0.399],
        '12*': [0.311, 0.368, 0.442, 0.308, 0.347, 0.417, 0.303, 0.335, 0.397]}
    tabl_1 = {
        2: [0.571, 0.554, 0.587, 0.571, 0.554, 0.587, 0.571, 0.554, 0.587],
        4: [0.505, 0.505, 0.540, 0.505, 0.505, 0.540, 0.505, 0.505, 0.540],
        6: [0.468, 0.443, 0.516, 0.468, 0.443, 0.516, 0.468, 0.443, 0.516],
        8: [0.410, 0.442, 0.505, 0.410, 0.442, 0.505, 0.410, 0.442, 0.505],
        12: [0.369, 0.415, 0.490, 0.369, 0.415, 0.490, 0.369, 0.415, 0.490],
        '12*': [0.366, 0.412, 0.487, 0.366, 0.412, 0.487, 0.366, 0.413, 0.487]}
    tabl_3 = {
        2: [0.702, 0.681, 0.701, 0.694, 0.982, 0.710, 0.634, 0.639, 0.689],
        4: [0.603, 0.616, 0.652, 0.613, 0.631, 0.670, 0.587, 0.607, 0.655],
        6: [0.586, 0.526, 0.615, 0.599, 0.545, 0.640, 0.601, 0.536, 0.643],
        8: [0.485, 0.529, 0.597, 0.509, 0.557, 0.625, 0.512, 0.567, 0.641],
        12: [0.435, 0.491, 0.571, 0.463, 0.524, 0.603, 0.483, 0.598, 0.632],
        '12*': [0.431, 0.487, 0.586, 0.459, 0.520, 0.601, 0.479, 0.546, 0.360]}
    tabl_10 = {
        2: [0.802, 0.800, 0.818, 0.806, 0.809, 0.829, 0.707, 0.731, 0.776],
        4: [0.665, 0.708, 0.762, 0.696, 0.739, 0.790, 0.667, 0.722, 0.761],
        6: [0.636, 0.583, 0.640, 0.622, 0.754, 0.754, 0.643, 0.636, 0.758],
        8: [0.536, 0.605, 0.693, 0.583, 0.600, 0.733, 0.621, 0.695, 0.700],
        12: [0.251, 0.560, 0.660, 0.533, 0.671, 0.710, 0.604, 0.689, 0.754],
        '12*': [0.479, 0.555, 0.656, 0.529, 0.615, 0.707, 0.598, 0.682, 0.752]}

    def __init__(self, p1, p2, h, l_vert, a1, a2):
        '''
        m - число вертикальных заземлителей, шт. [2, 12];
        p1 - удельное сопротивление верхнего слоя грунта, Ом*м;
        p2 - удельное сопротивление нижнего слоя грунта, Ом*м;
        h - толщина(мощность) верхнего слоя грунта, м.;
        l_vert - длинна вертикального заземлителя, м.;
        a1 - длинна горизонтального заземлителя, сторона 1, м.;
        a2 - длинна горизонтального заземлителя, сторона 2, м.;;
        a_middle - среднее расстояние между вертикальными заземлителями, м.;
        '''

        self.p1 = p1
        self.p2 = p2
        self.p = self.p1 / self.p2
        self.h = h
        self.l_vert = l_vert
        self.a1 = a1
        self.a2 = a2
        self.tab1 = None
        self.tab2 = None
        self.tab_out = {}
        self.tab_out1 = {}

    @staticmethod
    def lin_interpol(x: float, x1: float, x2: float, f_x1: float, f_x2: float) -> float:
        '''Линейная интерполяция, f(X) = f(X1)+(f(X2) - f(X1))*(X - X1)/(X2 - X1)
        1. Значение Х должно лежать в диапазоне от X1 до X2;
        2. X1 < X2'''
        return round(f_x1 + (f_x2 - f_x1) * (x - x1) / (x2 - x1), 3)

    @staticmethod
    def min_max(value, list_in: list) -> tuple:
        '''Определение ближнего макс. и мин. значения'''
        for i in range(len(list_in)):
            if value in list_in:
                min_v = max_v = value
                return min_v, max_v
            elif value <= list_in[0]:
                min_v, max_v = list_in[0], list_in[0]
                return min_v, max_v
            elif value < list_in[i] and list_in[-1] > value > list_in[0]:
                min_v, max_v = list_in[i - 1], list_in[i]
                return min_v, max_v
            elif value >= list_in[-1]:
                min_v, max_v = list_in[-1], list_in[-1]
                return min_v, max_v

    def get_tabl(self) -> None:
        '''Получаем таблицы для соответствующего p1/p2'''
        if self.p <= 0.5:
            self.tab_out = self.tabl_05
        elif 0.5 < self.p < 1:
            self.tab1, self.tab2 = self.tabl_05, self.tabl_1
            self.get_interpol_for_p()
        elif self.p == 1:
            self.tab_out = self.tabl_1
        elif 1 < self.p < 3:
            self.tab1, self.tab2 = self.tabl_1, self.tabl_3
            self.get_interpol_for_p()
        elif self.p == 3:
            self.tab_out = self.tabl_3
        elif 3 < self.p < 10:
            self.tab1, self.tab2 = self.tabl_3, self.tabl_10
            self.get_interpol_for_p()
        elif self.p >= 10:
            self.tab_out = self.tabl_10
        self.interpol_dict_for_h_lvert()

    def get_interpol_for_p(self) -> None:
        '''Интерполяция по p1/p2'''
        min_p, max_p = self.min_max(self.p, [0.5, 1, 3, 10])
        for key in self.tab1.keys():
            list_interpol = [self.lin_interpol(self.p, min_p, max_p, self.tab1[key][i], self.tab2[key][i]) for i in
                             range(9)]
            self.tab_out.update({key: list_interpol})

    def interpol_dict_for_h_lvert(self):
        '''Интерполяция по h/lvert'''
        result = self.h / self.l_vert
        for key in self.tab_out.keys():
            if result <= 0.2:
                res = self.tab_out[key][0:3]
            elif 0.5 > result > 0.2:
                res = [(self.lin_interpol(result, 0.2, 0.5, self.tab_out[key][0:3][i], self.tab_out[key][3:6][i])) for i
                       in range(3)]
            elif result == 0.5:
                res = self.tab_out[key][3:6]
            elif 1 > result > 0.5:
                res = [(self.lin_interpol(result, 0.5, 1, self.tab_out[key][3:6][i], self.tab_out[key][6:9][i])) for i
                       in range(3)]
            elif result >= 1:
                res = self.tab_out[key][6:9]
            self.tab_out1.update({key: res})

    def get_interpol_for_m(self, m):
        '''Интерполяция по m'''
        min_m, max_m = self.min_max(m, [2, 4, 6, 8, 12])
        if m == 1:
            list_out = self.tab_out1[2]
        elif m == 2 or m == 4 or m == 2 or m == 6 or m == 8:
            list_out = self.tab_out1[m]
        elif m == 10:
            list_out = [self.lin_interpol(m, min_m, max_m, self.tab_out1[min_m][i], self.tab_out1[max_m][i]) for i in
                        range(3)]
        elif m == 12 and self.a1 / self.a2 != 0.5:
            list_out = self.tab_out1[m]
        elif m == 12 and self.a1 / self.a2 == 0.5:
            list_out = self.tab_out1['12*']
        elif m != 1 and m % 2 != 0 and m < 12:
            list_out = [self.lin_interpol(m, min_m, max_m, self.tab_out1[min_m][i], self.tab_out1[max_m][i]) for i in
                        range(3)]
        elif m > 12:
            list_out = self.tab_out1[12]
        return self.interpol_dict_for_a_lvert(list_out, (self.a1 + self.a2) * 2 / m)

    def interpol_dict_for_a_lvert(self, list_in: list, a_middle):
        '''Интерполяция по a/lvert'''
        a_middle = a_middle / self.l_vert
        min_a_lvert, max_a_lvert = self.min_max(a_middle, [0.5, 1, 2])
        if a_middle <= 0.5:
            return list_in[0]
        elif 1 > a_middle > 0.5:
            return self.lin_interpol(a_middle, min_a_lvert, max_a_lvert, list_in[0], list_in[1])
        elif a_middle == 1:
            return list_in[1]
        elif 2 > a_middle > 1:
            return self.lin_interpol(a_middle, min_a_lvert, max_a_lvert, list_in[1], list_in[2])
        elif a_middle >= 2:
            return list_in[2]
