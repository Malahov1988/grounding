class get_P_gor:
    '''За исключением t = 0.5 м'''
    tab_05 = {1: [0.63, 0.68, 0.71, 0.72, 0.74, 0.74, 0.75, 0.76, 0.76, 0.77, 0.77, 0.78, 0.78, 0.8],
              3: [0.54, 0.58, 0.61, 0.63, 0.64, 0.65, 0.66, 0.67, 0.67, 0.68, 0.68, 0.69, 0.70, 0.71],
              5: [0.53, 0.56, 0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.65, 0.66, 0.66, 0.67]}
    tab_1 = {1: [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
             3: [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
             5: [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00]}
    tab_2 = {1: [1.65, 1.53, 1.47, 1.43, 1.41, 1.39, 1.38, 1.37, 1.40, 1.36, 1.35, 1.35, 1.33, 1.33],
             3: [1.89, 1.87, 1.79, 1.76, 1.72, 1.70, 1.67, 1.64, 1.64, 1.63, 1.61, 1.60, 1.58, 1.56],
             5: [1.93, 1.92, 1.86, 1.81, 1.8, 1.77, 1.76, 1.75, 1.73, 1.72, 1.71, 1.7, 1.65, 1.63]}
    tab_5 = {1: [3.03, 2.96, 2.72, 2.60, 2.56, 2.46, 2.41, 2.39, 2.36, 2.34, 2.31, 2.28, 2.25, 2.20],
             3: [4.52, 4.31, 4.00, 3.83, 3.74, 3.66, 3.53, 3.48, 3.43, 3.41, 3.36, 3.31, 3.23, 3.18],
             5: [4.72, 4.66, 4.27, 4.23, 4.02, 3.95, 3.87, 3.83, 3.82, 3.75, 3.72, 3.56, 3.48, 3.43]}
    tab_10 = {1: [6.02, 5.29, 4.76, 4.51, 4.30, 4.19, 4.10, 4.06, 4.00, 3.89, 3.84, 3.78, 3.71, 3.64],
              3: [9.45, 8.51, 7.66, 7.33, 7.10, 6.94, 6.65, 6.57, 6.46, 6.38, 3.34, 6.11, 6.04, 5.85],
              5: [9.66, 9.26, 8.42, 8.14, 7.73, 7.56, 7.43, 7.32, 7.21, 7.10, 6.91, 6.80, 6.69, 6.50]}
    tab_20 = {1: [11.40, 10.10, 8.85, 8.26, 7.90, 7.62, 7.45, 7.23, 7.13, 7.04, 6.99, 6.79, 6.55, 6.42],
              3: [18.10, 16.80, 15.10, 14.30, 13.60, 13.00, 12.70, 12.50, 12.30, 12.10, 11.90, 11.40, 11.10],
              5: [19.8, 18.1, 16.8, 16.0, 15.4, 14.7, 14.6, 14.3, 13.9, 13.7, 13.4, 13.4, 12.9, 12.4]}

    def __init__(self, p1, p2, h, t):
        self.tabl = {}
        self.p = p1 / p2
        self.h = h
        self.t = t

    @staticmethod
    def min_max(value, list_in: list) -> tuple:
        '''Определение ближнего макс. и мин. значения'''
        for i in range(len(list_in)):
            if value in list_in:
                min_v = max_v = value
                break
            elif value <= list_in[0]:
                min_v, max_v = list_in[0], list_in[0]
                break
            elif value < list_in[i] and list_in[-1] > value > list_in[0]:
                min_v, max_v = list_in[i - 1], list_in[i]
                break
            elif value >= list_in[-1]:
                min_v, max_v = list_in[-1], list_in[-1]
                break
        return min_v, max_v

    @staticmethod
    def lin_interpol(x, x1, x2, f_x1, f_x2):
        '''Линейная интерполяция, f(X) = f(X1)+(f(X2) - f(X1))*(X - X1)/(X2 - X1)
        1. Значение Х должно лежать в диапазоне от X1 до X2;
        2. X1 < X2'''
        return round(f_x1 + (f_x2 - f_x1) * (x - x1) / (x2 - x1), 3)

    def get_tab(self, l_gor):
        if self.p <= 0.5:
            self.tabl = self.tab_05
        elif 0.5 < self.p < 1:
            self.tabl = self.interpol_for_p(self.tab_05, self.tab_1)
        elif self.p == 1:
            self.tabl = self.tab_1
        elif 1 < self.p < 2:
            self.tabl = self.interpol_for_p(self.tab_1, self.tab_2)
        elif self.p == 2:
            self.tabl = self.tab_2
        elif 2 < self.p < 5:
            self.tabl = self.interpol_for_p(self.tab_2, self.tab_5)
        elif self.p == 5:
            self.tabl = self.tab_5
        elif 5 < self.p < 10:
            self.tabl = self.interpol_for_p(self.tab_5, self.tab_10)
        elif self.p == 10:
            self.tabl = self.tab_10
        elif 10 < self.p < 20:
            self.tabl = self.interpol_for_p(self.tab_10, self.tab_20)
        elif self.p >= 20:
            self.tabl = self.tab_20
        self.interpol_for_h()
        return self.interpol_for_l(l_gor)

    def interpol_for_p(self, dict_in_1, dict_in_2):
        dict_out = {}
        min_p, max_p = self.min_max(self.p, [0.5, 1, 2, 5, 10, 20])
        for k, v in dict_in_1.items():
            list_val_aftet_interp = [self.lin_interpol(self.p, min_p, max_p, dict_in_1[k][i], dict_in_2[k][i]) for i in
                                     range(14)]
            dict_out.update({k: list_val_aftet_interp})
        return dict_out

    def interpol_for_h(self):
        min_h, max_h = self.min_max(self.h, [1, 3, 5])
        if self.h <= 1:
            self.list_out = self.tabl[1]
        elif 3 > self.h > 1:
            self.list_out = [self.lin_interpol(self.h, min_h, max_h, self.tabl[1][i], self.tabl[3][i]) for i in
                             range(14)]
        elif self.h <= 3:
            self.list_out = self.tabl[3]
        elif 5 > self.h > 5:
            self.list_out = [self.lin_interpol(self.h, min_h, max_h, self.tabl[3][i], self.tabl[5][i]) for i in
                             range(14)]
        elif self.h <= 5:
            self.list_out = self.tabl[5]

    def interpol_for_l(self, l_gor):
        '''Определение pэк.г/p2'''
        list_l = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 200]
        min_l, max_l = self.min_max(l_gor, list_l)
        index_min_l = list_l.index(min_l)
        index_max_l = list_l.index(max_l)
        value_min_l = self.list_out[index_min_l]
        value_max_l = self.list_out[index_max_l]
        if l_gor <= 5:
            p_ikviv = self.list_out[0]
        elif l_gor > 100:
            p_ikviv = self.list_out[-1]
        elif l_gor in list_l:
            p_ikviv = self.list_out[list_l.index(l_gor)]
        else:
            p_ikviv = self.lin_interpol(l_gor, min_l, max_l, value_min_l, value_max_l)
        return p_ikviv


if __name__ == '__main__':
    P = get_P_gor(250, 30, 2.5, 0.8)
    for i in range(0, 210, 3):
    #     i = i /10
    #     print(i, P.min_max(i, [0.5, 1, 3, 10]))
    # print(P.get_tab(8) * 30)
    # print(P.get_tab(14) * 30)
        print(P.get_tab(i))
